"""
Interactive Gradio app to generate and play branching narrative adventures.
"""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import gradio as gr

from agents import (
    CharacterAgent,
    ConflictAgent,
    LevelAgent,
    MechanicAgent,
    StyleAgent,
    TwistAgent,
)
from engine import GameEngine, GameEngineError, InvalidChoiceError
from models import GameSpec
from narrative_composer import NarrativeComposer, NarrativeComposerError
from storage import (
    list_saved_games,
    load_game_spec,
    save_game_spec,
)

# -----------------------------------------------------------------------------
# Logging setup
# -----------------------------------------------------------------------------
LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH / "narrative_app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("narrative_app")

# -----------------------------------------------------------------------------
# Configuration constants
# -----------------------------------------------------------------------------
RISK_BADGE = {
    "safe": "🟢",
    "risky": "🟡",
    "chaotic": "🔴",
}

MODE_FIELDS: Dict[str, List[Tuple[str, str]]] = {
    "Relaxing": [
        ("Subject", "What you interact with (e.g., butterfly, cloud, leaf)"),
        ("Vibe", "Calm/zen/cozy feeling (e.g., peaceful, serene, gentle)"),
        ("Setting", "Peaceful location (e.g., garden, beach, forest)"),
        ("Wildcard", "Gentle mechanic (e.g., floating, drifting, breathing)"),
    ],
    "Funny": [
        ("Subject", "Silly character/thing (e.g., dancing pickle, confused robot)"),
        ("Action", "Absurd verb (e.g., wobbling, exploding, yodeling)"),
        ("Vibe", "Comedic tone (e.g., slapstick, witty, ridiculous)"),
        ("Setting", "Weird location (e.g., giant toilet, moon cheese factory)"),
        ("Twist", "Unexpected element (e.g., surprise mustache, gravity reversal)"),
    ],
    "Chaotic": [
        ("Subject", "Fast-moving character (e.g., caffeinated squirrel, rocket)"),
        ("Action", "Frantic verb (e.g., dodging, bouncing, spinning)"),
        ("Obstacle", "Hazard/challenge (e.g., falling pianos, laser beams)"),
        ("Chaos Modifier", "Randomness factor (e.g., screen shake, color swap)"),
        ("Setting", "Dynamic location (e.g., collapsing tower, speeding train)"),
    ],
    "Challenge": [
        ("Subject", "Player character (e.g., ninja, space explorer, chef)"),
        ("Goal", "Win condition (e.g., collect 10 stars, reach the top)"),
        ("Obstacle", "Antagonist or challenge (e.g., evil wizard, time limit)"),
        ("Setting", "Arena (e.g., volcano, underwater cave, city rooftop)"),
        ("Twist", "Power-up or mechanic (e.g., double jump, invisibility)"),
    ],
    "Surprise Me": [
        ("Vibe", "Just one word to set the mood (e.g., mysterious, explosive)"),
    ],
}

CHOICE_SEPARATOR = ":::"

# -----------------------------------------------------------------------------
# Helper functions for formatting UI content
# -----------------------------------------------------------------------------


def _format_stats_block(state: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    score = state.get("score", 0)
    stats = state.get("stats", {})
    stat_names = metadata.get("stat_names") or list(stats.keys())
    lines = [f"**Score:** {score}"]
    if stat_names:
        for name in stat_names:
            lines.append(f"- {name}: {stats.get(name, 0)}")
    elif stats:
        for name, value in stats.items():
            lines.append(f"- {name}: {value}")
    return "\n".join(lines) if lines else "Score data unavailable."


def _format_inventory_block(inventory: List[Dict[str, Any]]) -> str:
    if not inventory:
        return "_No loot collected yet._"
    lines = []
    for item in inventory:
        if not isinstance(item, dict):
            lines.append(f"- {item}")
            continue
        name = item.get("item") or item.get("name") or "Mystery Item"
        detail_parts = []
        for key in ("description", "stat", "stat_bonus", "effect"):
            value = item.get(key)
            if value:
                detail_parts.append(str(value))
        detail = " — " + "; ".join(detail_parts) if detail_parts else ""
        lines.append(f"- 🎁 **{name}**{detail}")
    return "\n".join(lines)


def _format_history_block(history: List[Dict[str, Any]]) -> str:
    if not history:
        return "_No choices made yet._"
    recent = history[-6:]  # show last up to 6 entries
    lines = []
    for entry in recent:
        label = entry.get("choice_label", "Choice")
        result = entry.get("result_text", "")
        delta = entry.get("delta_score", 0)
        badge = RISK_BADGE.get(entry.get("risk_level", "safe"), "⚪")
        delta_str = f"{'+' if delta >= 0 else ''}{delta}"
        lines.append(f"- {badge} **{label}** (Δ score {delta_str}) — {result}")
    return "\n".join(lines)


def _format_result_block(last_choice: Optional[Dict[str, Any]]) -> str:
    if not last_choice:
        return "_Make a choice to see the outcome text here._"
    result_text = last_choice.get("result_text", "")
    delta = last_choice.get("delta_score", 0)
    stat_changes = last_choice.get("stat_changes") or {}
    loot = last_choice.get("loot")

    parts = [result_text]
    effects = []
    if delta:
        effects.append(f"Score {'+' if delta >= 0 else ''}{delta}")
    if stat_changes:
        stat_bits = [f"{stat} {'+' if change >= 0 else ''}{change}" for stat, change in stat_changes.items()]
        effects.append(f"Stats: {', '.join(stat_bits)}")
    if loot:
        loot_name = loot.get("item") or loot.get("name") or "Loot"
        effects.append(f"Loot: {loot_name}")
    if effects:
        parts.append("\n\n" + " • ".join(effects))
    return "\n".join(parts)


def _format_risk_legend(metadata: Dict[str, Any]) -> str:
    legend = metadata.get("risk_legend") or {
        "safe": "🟢 low risk / modest reward",
        "risky": "🟡 swingy outcomes",
        "chaotic": "🔴 unpredictable",
    }
    lines = ["**Risk Legend**"]
    for key in ("safe", "risky", "chaotic"):
        descriptor = legend.get(key)
        if descriptor:
            lines.append(f"- {descriptor}")
    return "\n".join(lines)


def _format_game_over_text(game_over: bool, ending_tag: Optional[str]) -> str:
    if not game_over:
        return ""
    ending_map = {
        "win": "🎉 **Victory!** You reached a winning ending.",
        "lose": "💀 **Defeat!** Better luck next run.",
        "weird": "🌀 **Weird Ending!** That was unexpected.",
    }
    return ending_map.get(ending_tag, "🏁 **Game Over!** The story has concluded.")


def _build_choice_options(choices: List[Dict[str, Any]]) -> Tuple[List[str], List[Dict[str, Any]]]:
    if not choices:
        return [], []
    radio_choices: List[str] = []
    choice_payloads: List[Dict[str, Any]] = []
    for choice in choices:
        badge = RISK_BADGE.get(choice.get("risk_level", "safe"), "⚪")
        delta = choice.get("delta_score", 0)
        delta_str = f"{'+' if delta >= 0 else ''}{delta}"
        stat_changes = choice.get("stat_changes") or {}
        stat_bits = ", ".join(
            f"{stat} {'+' if change >= 0 else ''}{change}"
            for stat, change in stat_changes.items()
            if change
        )
        loot = choice.get("loot")
        loot_str = f" 🎁 {loot.get('item')}" if isinstance(loot, dict) and loot.get("item") else ""
        effect_parts = [f"Δ score {delta_str}"]
        if stat_bits:
            effect_parts.append(stat_bits)
        label = choice.get("label", "Choose")
        display = f"{badge} {label} ({'; '.join(effect_parts)}){loot_str}"
        value = f"{choice.get('id')} {CHOICE_SEPARATOR} {label}"
        radio_choices.append(value)
        choice_payloads.append({"id": choice.get("id"), "display": display, "raw": choice})
    return radio_choices, choice_payloads


def _snapshot_to_ui(snapshot: Dict[str, Any], engine: Optional[GameEngine] = None) -> Tuple[str, str, str, List[str], List[Dict[str, Any]], str, str, str, str]:
    """
    Convert an engine snapshot to the UI blocks (not including status/debug/saved-games).
    Returns tuple:
        scene_title, scene_body, result_text, radio_choices, choice_payloads,
        stats_md, inventory_md, history_md, game_over_md, risk_md
    """
    scene = snapshot.get("scene")
    state = snapshot.get("state", {})
    metadata = snapshot.get("metadata", {})
    ending_tag = snapshot.get("ending_tag") or state.get("ending_tag")
    game_over = snapshot.get("game_over", False) or state.get("is_complete")

    if scene:
        scene_title = f"### {scene.get('title', 'Current Scene')}"
        scene_body = scene.get("body", "")
        radio_choices, choice_payloads = _build_choice_options(scene.get("choices", []))
    else:
        scene_title = "### No Active Scene"
        scene_body = "_Generate or load a narrative to play._"
        radio_choices, choice_payloads = [], []

    result_md = _format_result_block(snapshot.get("last_choice"))
    stats_md = _format_stats_block(state, metadata)
    inventory_md = _format_inventory_block(state.get("inventory") or [])
    history_md = _format_history_block(state.get("history") or [])
    game_over_md = _format_game_over_text(game_over, ending_tag)
    risk_md = _format_risk_legend(metadata)

    # Disable choices if game is complete
    if game_over:
        radio_choices = []
        choice_payloads = []

    return (
        scene_title,
        scene_body,
        result_md,
        radio_choices,
        choice_payloads,
        stats_md,
        inventory_md,
        history_md,
        game_over_md,
        risk_md,
    )


def _collect_user_inputs(mode: str, field_values: List[str]) -> Dict[str, str]:
    fields = MODE_FIELDS.get(mode, [])
    collected: Dict[str, str] = {}
    for idx, raw_value in enumerate(field_values):
        if idx >= len(fields):
            break
        label = fields[idx][0]
        if raw_value and raw_value.strip():
            collected[label] = raw_value.strip()
    return collected


def _instantiate_agents() -> Dict[str, Any]:
    return {
        "character": CharacterAgent(),
        "mechanic": MechanicAgent(),
        "style": StyleAgent(),
        "conflict": ConflictAgent(),
        "level": LevelAgent(),
        "twist": TwistAgent(),
    }


async def _run_sub_agents(mode: str, provider: str, user_inputs: Dict[str, str]) -> Dict[str, Any]:
    agents = _instantiate_agents()
    tasks: List[asyncio.Future] = []
    keys: List[str] = []

    if "Subject" in user_inputs:
        tasks.append(agents["character"].generate(user_inputs["Subject"], mode, provider))
        keys.append("character")

    if any(k in user_inputs for k in ("Action", "Goal")):
        action_or_goal = user_inputs.get("Action") or user_inputs.get("Goal")
        tasks.append(agents["mechanic"].generate(action_or_goal, mode, provider))
        keys.append("mechanic")

    if "Vibe" in user_inputs:
        tasks.append(agents["style"].generate(user_inputs["Vibe"], mode, provider))
        keys.append("style")

    if "Obstacle" in user_inputs:
        tasks.append(agents["conflict"].generate(user_inputs["Obstacle"], mode, provider))
        keys.append("conflict")

    if "Setting" in user_inputs:
        tasks.append(agents["level"].generate(user_inputs["Setting"], mode, provider))
        keys.append("level")

    if any(k in user_inputs for k in ("Wildcard", "Twist", "Chaos Modifier")):
        twist_value = user_inputs.get("Wildcard") or user_inputs.get("Twist") or user_inputs.get("Chaos Modifier")
        tasks.append(agents["twist"].generate(twist_value, mode, provider))
        keys.append("twist")

    if mode == "Surprise Me":
        tasks = [
            agents["character"].generate(user_inputs.get("Vibe", "surprise"), mode, provider),
            agents["mechanic"].generate("auto-generate", mode, provider),
            agents["style"].generate(user_inputs.get("Vibe", "surprise"), mode, provider),
            agents["conflict"].generate("auto-generate", mode, provider),
            agents["level"].generate("auto-generate", mode, provider),
            agents["twist"].generate("surprise", mode, provider),
        ]
        keys = ["character", "mechanic", "style", "conflict", "level", "twist"]

    if not tasks:
        raise ValueError("No sub-agents were triggered. Please provide more inputs.")

    logger.info("Launching %d sub-agents for mode %s using %s", len(tasks), mode, provider)
    results = await asyncio.gather(*tasks)
    return {key: result for key, result in zip(keys, results)}


def _saved_game_choices() -> Tuple[List[str], List[Dict[str, Any]]]:
    games = list_saved_games()
    choices = [
        f"{game['id']} {CHOICE_SEPARATOR} {game.get('title') or 'Untitled'} ({game.get('mode') or 'Unknown'})"
        for game in games
        if game.get("id")
    ]
    return choices, games


def _empty_ui_state(status: str = "_Ready to generate a narrative adventure._") -> Tuple:
    radio_update = gr.update(choices=[], value=None, interactive=False)
    saved_choices, saved_listing = _saved_game_choices()
    return (
        status,
        "### No Game Loaded",
        "_Use the form to generate a new branching narrative or load a saved one._",
        radio_update,
        "_Make a choice to see the outcome text here._",
        "**Score:** 0",
        "_No loot collected yet._",
        "_No choices made yet._",
        "",
        _format_risk_legend({}),
        None,
        [],
        json.dumps({}, indent=2),
        gr.update(choices=saved_choices, value=None),
        saved_listing,
    )


def _build_success_outputs(
    status_lines: List[str],
    engine: GameEngine,
    snapshot: Dict[str, Any],
    saved_games_listing: List[Dict[str, Any]],
    extra_debug: Optional[Dict[str, Any]] = None,
) -> Tuple:
    scene_title, scene_body, result_md, radio_choices, choice_payloads, stats_md, inventory_md, history_md, game_over_md, risk_md = _snapshot_to_ui(snapshot, engine)

    radio_update = gr.update(
        choices=radio_choices,
        value=None,
        interactive=bool(radio_choices),
    )

    saved_choices = [
        f"{game['id']} {CHOICE_SEPARATOR} {game.get('title') or 'Untitled'} ({game.get('mode') or 'Unknown'})"
        for game in saved_games_listing
        if game.get("id")
    ]

    debug_payload = {
        "status": status_lines,
        "snapshot": snapshot,
    }
    if extra_debug:
        debug_payload.update(extra_debug)

    status_md = "\n".join(status_lines)
    return (
        status_md,
        scene_title,
        scene_body,
        radio_update,
        result_md,
        stats_md,
        inventory_md,
        history_md,
        game_over_md,
        risk_md,
        engine,
        choice_payloads,
        json.dumps(debug_payload, indent=2, ensure_ascii=False),
        gr.update(choices=saved_choices, value=None),
        saved_games_listing,
    )


def _find_choice_payload(choice_id: str, choice_payloads: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for payload in choice_payloads:
        if payload.get("id") == choice_id:
            return payload
    return None


# -----------------------------------------------------------------------------
# Event handlers
# -----------------------------------------------------------------------------


async def generate_game(
    mode: str,
    provider: str,
    field1: str,
    field2: str,
    field3: str,
    field4: str,
    field5: str,
) -> Tuple:
    field_values = [field1, field2, field3, field4, field5]
    user_inputs = _collect_user_inputs(mode, field_values)

    if not user_inputs:
        return _empty_ui_state("⚠️ Please provide at least one Mad-Lib input.")

    status_lines = [
        f"🚀 Generating new narrative in **{mode}** mode",
        f"🤖 Sub-agents powered by **{provider.upper()}**",
        f"📝 Inputs: {', '.join(f'{k}={v}' for k, v in user_inputs.items())}",
    ]

    try:
        sub_agent_outputs = await _run_sub_agents(mode, provider, user_inputs)
        status_lines.append("✅ Sub-agents completed successfully.")

        composer = NarrativeComposer()
        game_spec = composer.compose(mode, sub_agent_outputs)
        status_lines.append(f"🎼 Narrative composed: **{game_spec.title}**")

        engine = GameEngine(game_spec)
        snapshot = engine.snapshot()

        saved_path = save_game_spec(game_spec)
        status_lines.append(f"💾 Game saved to `{saved_path}`")

        _, saved_listing = _saved_game_choices()
        extra_debug = {
            "inputs": user_inputs,
            "sub_agents": sub_agent_outputs,
            "game_spec": game_spec.to_dict(),
            "saved_path": str(saved_path),
        }
        return _build_success_outputs(status_lines, engine, snapshot, saved_listing, extra_debug)

    except (NarrativeComposerError, GameEngineError, ValueError) as exc:
        logger.exception("Failed to generate narrative: %s", exc)
        return _empty_ui_state(f"❌ Generation failed: {exc}")
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Unexpected error during generation: %s", exc)
        return _empty_ui_state(f"❌ Unexpected error: {exc}")


def handle_choice(
    engine: Optional[GameEngine],
    choice_value: Optional[str],
    choice_payloads: List[Dict[str, Any]],
) -> Tuple:
    if engine is None:
        return _empty_ui_state("⚠️ No active game. Generate or load a narrative first.")

    if not choice_value:
        snapshot = engine.snapshot()
        _, saved_listing = _saved_game_choices()
        status_lines = ["⚠️ Please select a choice before continuing."]
        return _build_success_outputs(status_lines, engine, snapshot, saved_listing)

    choice_id = choice_value.split(CHOICE_SEPARATOR, 1)[0].strip()
    selected_payload = _find_choice_payload(choice_id, choice_payloads)
    chosen_label = selected_payload.get("raw", {}).get("label") if selected_payload else choice_id

    try:
        snapshot = engine.apply_choice(choice_id)
        _, saved_listing = _saved_game_choices()
        status_lines = [f"➡️ You selected **{chosen_label}**.", "✅ State updated."]

        extra_debug = {
            "last_choice": snapshot.get("last_choice"),
            "state": snapshot.get("state"),
        }
        return _build_success_outputs(status_lines, engine, snapshot, saved_listing, extra_debug)
    except InvalidChoiceError as exc:
        logger.warning("Invalid choice attempted: %s", exc)
        snapshot = engine.snapshot()
        _, saved_listing = _saved_game_choices()
        status_lines = [f"⚠️ {exc}"]
        return _build_success_outputs(status_lines, engine, snapshot, saved_listing)
    except GameEngineError as exc:
        logger.exception("Engine error while applying choice: %s", exc)
        return _empty_ui_state(f"❌ Engine error: {exc}")
    except Exception as exc:  # pragma: no cover
        logger.exception("Unexpected error applying choice: %s", exc)
        return _empty_ui_state(f"❌ Unexpected error: {exc}")


def load_saved_game(selection: Optional[str]) -> Tuple:
    if not selection:
        return _empty_ui_state("⚠️ Please pick a saved game to load.")

    game_id = selection.split(CHOICE_SEPARATOR, 1)[0].strip()
    try:
        spec = load_game_spec(game_id)
        engine = GameEngine(spec)
        snapshot = engine.snapshot()
        status_lines = [f"📂 Loaded saved narrative: **{spec.title}**"]
        _, saved_listing = _saved_game_choices()
        extra_debug = {"game_spec": spec.to_dict()}
        return _build_success_outputs(status_lines, engine, snapshot, saved_listing, extra_debug)
    except FileNotFoundError:
        logger.warning("Saved game %s not found.", game_id)
        return _empty_ui_state(f"⚠️ Saved game `{game_id}` not found.")
    except Exception as exc:
        logger.exception("Error loading saved game: %s", exc)
        return _empty_ui_state(f"❌ Failed to load saved game: {exc}")


def reset_game() -> Tuple:
    return _empty_ui_state("🔄 Game reset. Ready for a new adventure!")


def update_fields(mode: str):
    fields = MODE_FIELDS.get(mode, [])
    updates: List[Any] = []
    for index in range(5):
        if index < len(fields):
            label, placeholder = fields[index]
            updates.extend(
                [
                    gr.update(visible=True, label=label, placeholder=placeholder, value=""),
                    gr.update(visible=True),
                ]
            )
        else:
            updates.extend([gr.update(visible=False), gr.update(visible=False)])
    return updates


# -----------------------------------------------------------------------------
# Build Gradio interface
# -----------------------------------------------------------------------------


with gr.Blocks(theme=gr.themes.Soft(), title="OMFGG Narrative Adventures") as demo:
    gr.Markdown(
        """
        # 🌿 OMFGG Narrative Adventures
        Generate a branching narrative from Mad-Lib prompts, then play it out with risk, loot, and stat tracking.
        """
    )

    with gr.Row():
        mode_selector = gr.Radio(
            choices=list(MODE_FIELDS.keys()),
            value="Funny",
            label="🎯 Select Narrative Mode",
            interactive=True,
        )
        provider_selector = gr.Radio(
            choices=["openai", "anthropic"],
            value="openai",
            label="🤖 Sub-Agent Provider",
            interactive=True,
        )

    gr.Markdown("## 📝 Mad-Lib Inputs")

    with gr.Column():
        field_components = []
        for _ in range(5):
            with gr.Row(visible=False) as row:
                textbox = gr.Textbox(label="Input", placeholder="Enter your creative idea...", scale=4)
                field_components.append(textbox)
                field_components.append(row)

        field_textboxes = [field_components[i] for i in range(0, 10, 2)]
        field_rows = [field_components[i] for i in range(1, 10, 2)]

    generate_button = gr.Button("🚀 Generate Narrative", variant="primary")

    with gr.Row():
        choice_selector = gr.Radio(
            label="🎮 Choose your next action",
            choices=[],
            interactive=False,
        )
        submit_choice_button = gr.Button("➡️ Apply Choice", variant="secondary")

    with gr.Row():
        saved_games_dropdown = gr.Dropdown(label="💾 Load saved adventure", choices=[], interactive=True)
        load_button = gr.Button("📂 Load Selected", variant="secondary")
        reset_button = gr.Button("🔄 Reset", variant="secondary")

    gr.Markdown("## 🔄 Status")
    status_output = gr.Markdown()

    gr.Markdown("## 🎭 Current Scene")
    scene_title_output = gr.Markdown()
    scene_body_output = gr.Markdown()

    gr.Markdown("## ✨ Outcome")
    result_output = gr.Markdown()

    with gr.Row():
        stats_output = gr.Markdown(label="📊 Score & Stats")
        inventory_output = gr.Markdown(label="🎒 Inventory")

    gr.Markdown("## 🧭 Adventure Log")
    history_output = gr.Markdown()

    game_over_output = gr.Markdown()
    risk_legend_output = gr.Markdown()

    with gr.Accordion("Debug data", open=False):
        debug_output = gr.Code(label="Debug JSON", language="json", value="{}")

    # State holders
    engine_state = gr.State(value=None)
    choices_state = gr.State(value=[])
    saved_games_state = gr.State(value=[])

    # Wire events
    mode_selector.change(
        fn=update_fields,
        inputs=[mode_selector],
        outputs=field_components,
    )

    generate_button.click(
        fn=generate_game,
        inputs=[mode_selector, provider_selector, *field_textboxes],
        outputs=[
            status_output,
            scene_title_output,
            scene_body_output,
            choice_selector,
            result_output,
            stats_output,
            inventory_output,
            history_output,
            game_over_output,
            risk_legend_output,
            engine_state,
            choices_state,
            debug_output,
            saved_games_dropdown,
            saved_games_state,
        ],
    )

    submit_choice_button.click(
        fn=handle_choice,
        inputs=[engine_state, choice_selector, choices_state],
        outputs=[
            status_output,
            scene_title_output,
            scene_body_output,
            choice_selector,
            result_output,
            stats_output,
            inventory_output,
            history_output,
            game_over_output,
            risk_legend_output,
            engine_state,
            choices_state,
            debug_output,
            saved_games_dropdown,
            saved_games_state,
        ],
    )

    load_button.click(
        fn=load_saved_game,
        inputs=[saved_games_dropdown],
        outputs=[
            status_output,
            scene_title_output,
            scene_body_output,
            choice_selector,
            result_output,
            stats_output,
            inventory_output,
            history_output,
            game_over_output,
            risk_legend_output,
            engine_state,
            choices_state,
            debug_output,
            saved_games_dropdown,
            saved_games_state,
        ],
    )

    reset_button.click(
        fn=reset_game,
        inputs=[],
        outputs=[
            status_output,
            scene_title_output,
            scene_body_output,
            choice_selector,
            result_output,
            stats_output,
            inventory_output,
            history_output,
            game_over_output,
            risk_legend_output,
            engine_state,
            choices_state,
            debug_output,
            saved_games_dropdown,
            saved_games_state,
        ],
    )

    demo.load(
        fn=reset_game,
        inputs=[],
        outputs=[
            status_output,
            scene_title_output,
            scene_body_output,
            choice_selector,
            result_output,
            stats_output,
            inventory_output,
            history_output,
            game_over_output,
            risk_legend_output,
            engine_state,
            choices_state,
            debug_output,
            saved_games_dropdown,
            saved_games_state,
        ],
    )


if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7861)


