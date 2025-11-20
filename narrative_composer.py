"""
Narrative composer that transforms sub-agent outputs into a branching game spec.
"""

from __future__ import annotations

import json
import uuid
from textwrap import dedent
from typing import Any, Dict, Optional

from agents import anthropic_client, COMPOSER_MODEL  # Reuse existing Anthropic client
from models import GameSpec


class NarrativeComposerError(Exception):
    """Raised when the narrative composer cannot produce a valid game spec."""


class NarrativeComposer:
    """
    Converts agent outputs into a branching narrative `GameSpec` using Anthropic.
    """

    MODE_STAT_PRESETS: Dict[str, list[str]] = {
        "Funny": ["Humor", "Chaos", "Confidence"],
        "Relaxing": ["Peace", "Harmony", "Zen"],
        "Challenge": ["Courage", "Skill", "Wisdom"],
        "Chaotic": ["Speed", "Luck", "Mayhem"],
        "Surprise Me": ["Spark", "Curiosity", "Chaos"],
    }

    DEFAULT_RISK_LEGEND: Dict[str, str] = {
        "safe": "🟢 low risk / modest reward",
        "risky": "🟡 medium risk / swingy rewards",
        "chaotic": "🔴 unpredictable or wild outcome",
    }

    def __init__(self, client=anthropic_client, model: str = COMPOSER_MODEL):
        self.client = client
        self.model = model
        self.last_raw_response: Optional[str] = None
        self.last_json_payload: Optional[Dict[str, Any]] = None

    # --------------------------------------------------------------------- public API

    def compose(
        self,
        mode: str,
        sub_agent_outputs: Dict[str, Any],
        *,
        game_id: Optional[str] = None,
        extra_instructions: Optional[str] = None,
    ) -> GameSpec:
        """
        Produce a `GameSpec` using Anthropic Claude given the sub-agent outputs.
        """
        normalized_inputs = self._normalize_agent_outputs(sub_agent_outputs)
        prompt = self._build_prompt(mode, normalized_inputs, game_id, extra_instructions)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=5000,
            temperature=0.35,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text
        self.last_raw_response = response_text

        payload = self._extract_json(response_text)
        self.last_json_payload = payload

        game_dict = self._apply_defaults(payload, mode, game_id)

        try:
            return GameSpec.from_dict(game_dict)
        except Exception as exc:
            raise NarrativeComposerError(f"Failed to build GameSpec: {exc}") from exc

    # ------------------------------------------------------------------ prompt logic

    def _build_prompt(
        self,
        mode: str,
        normalized_inputs: Dict[str, Any],
        game_id: Optional[str],
        extra_instructions: Optional[str],
    ) -> str:
        stat_names = self.MODE_STAT_PRESETS.get(mode, ["Courage", "Wisdom", "Confidence"])
        extra = f"\nAdditional directives:\n{extra_instructions.strip()}\n" if extra_instructions else ""

        return dedent(
            f"""
            You are the NARRATIVE COMPOSER for the OMFGG project.
            Synthesize the following sub-agent outputs into a coherent branching narrative game.

            Game mode: {mode}
            Desired stat tracks: {', '.join(stat_names)}
            Desired risk legend: safe = steady, risky = high stakes, chaotic = unexpected.

            Sub-agent outputs (JSON or text):
            {json.dumps(normalized_inputs, indent=2)}

            Produce a narrative structure with these rules:
            - Create 5-8 total scenes (`Scene` objects).
            - Each non-terminal scene needs 2-4 choices.
            - Choices must include: `id`, `label`, `result_text`, `next_scene_id` (use `null` to end the game),
              `delta_score` (int), `risk_level` ("safe" | "risky" | "chaotic"), optional `loot` and `stat_changes`.
            - Use risk levels deliberately: safe = short-term reward, risky = swingy outcomes, chaotic = weird surprises.
            - Integrate loot items that align with the theme and apply stat bonuses in `stat_changes`.
            - Ensure stats align with the selected mode's track (3 stats only).
            - Create at least one winning ending (ending_tag="win") and one losing or weird ending.
            - Provide playful scene titles (emoji prefix encouraged) and descriptive bodies.
            - Weave agent insights into the narrative (character, style, conflict, level, twist).

            JSON response format:
            {{
              "id": "{game_id or "auto-generate-uuid"}",
              "title": "Short, thematic title",
              "mode": "{mode}",
              "start_scene_id": "scene_1",
              "scenes": {{
                "scene_1": {{
                  "id": "scene_1",
                  "title": "Emoji Title",
                  "body": "Narrative description",
                  "is_terminal": false,
                  "choices": [
                    {{
                      "id": "choice_1a",
                      "label": "What the player clicks",
                      "result_text": "Outcome narrative",
                      "next_scene_id": "scene_2",
                      "delta_score": 5,
                      "risk_level": "safe",
                      "loot": {{"item": "Name", "description": "Optional", "stat_bonus": "+2 Humor"}},
                      "stat_changes": {{"Humor": 2}}
                    }}
                  ]
                }},
                "...": "More scenes"
              }},
              "metadata": {{
                "summary": "One sentence pitch",
                "starting_score": 0,
                "starting_stats": {{"Humor": 0, "Chaos": 0, "Confidence": 0}},
                "stat_names": ["Humor", "Chaos", "Confidence"],
                "risk_legend": {{
                  "safe": "🟢 low risk / modest reward",
                  "risky": "🟡 high variance",
                  "chaotic": "🔴 unpredictable"
                }},
                "loot_notes": "How loot ties into stats"
              }}
            }}

            Requirements:
            - Return ONLY valid JSON. Do not wrap in markdown fences.
            - Ensure `start_scene_id` maps to a real scene key.
            - Scenes with `is_terminal=true` should have zero choices.
            - Make sure every `next_scene_id` references an actual scene or is null to end the game.
            {extra}
            """
        ).strip()

    # -------------------------------------------------------------- normalization utils

    def _normalize_agent_outputs(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        normalized: Dict[str, Any] = {}
        for key, value in outputs.items():
            if isinstance(value, str):
                stripped = value.strip()
                try:
                    normalized[key] = json.loads(stripped)
                except json.JSONDecodeError:
                    normalized[key] = stripped
            else:
                normalized[key] = value
        return normalized

    def _extract_json(self, response_text: str) -> Dict[str, Any]:
        candidate = response_text.strip()
        if candidate.startswith("```"):
            # Remove potential markdown fences
            candidate = candidate.strip("`")
            if candidate.startswith("json"):
                candidate = candidate[4:]

        # Attempt to locate JSON braces if extraneous text exists
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start != -1 and end != -1:
            candidate = candidate[start : end + 1]

        try:
            return json.loads(candidate)
        except json.JSONDecodeError as exc:
            raise NarrativeComposerError(f"Composer returned invalid JSON: {exc}\nRaw response:\n{response_text}") from exc

    def _apply_defaults(self, payload: Dict[str, Any], mode: str, explicit_game_id: Optional[str]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise NarrativeComposerError("Composer response must be a JSON object.")

        data = dict(payload)  # shallow copy
        data["mode"] = mode
        data["id"] = explicit_game_id or data.get("id") or str(uuid.uuid4())

        scenes_raw = data.get("scenes")
        if not isinstance(scenes_raw, dict) or not scenes_raw:
            raise NarrativeComposerError("Composer response must include a non-empty 'scenes' object.")

        fixed_scenes: Dict[str, Dict[str, Any]] = {}
        start_scene_id = data.get("start_scene_id")

        for index, (scene_key, scene_raw) in enumerate(scenes_raw.items()):
            if not isinstance(scene_raw, dict):
                raise NarrativeComposerError(f"Scene '{scene_key}' must be an object.")
            scene = dict(scene_raw)
            scene_id = scene.get("id") or scene_key
            scene["id"] = scene_id
            scene.setdefault("title", f"Scene {index + 1}")
            scene.setdefault("body", "")
            scene.setdefault("is_terminal", False)
            scene.setdefault("ending_tag", None)

            raw_choices = scene.get("choices", [])
            if scene.get("is_terminal"):
                raw_choices = []

            if not isinstance(raw_choices, list):
                raise NarrativeComposerError(f"Scene '{scene_id}' choices must be a list.")

            fixed_choices = []
            for choice_index, choice_raw in enumerate(raw_choices):
                if not isinstance(choice_raw, dict):
                    raise NarrativeComposerError(f"Choice #{choice_index + 1} in scene '{scene_id}' must be an object.")
                choice = dict(choice_raw)
                choice.setdefault("id", f"{scene_id}_choice_{choice_index + 1}")
                choice.setdefault("label", f"Choice {choice_index + 1}")
                choice.setdefault("result_text", "")
                choice["delta_score"] = int(choice.get("delta_score", 0) or 0)
                choice["risk_level"] = self._normalize_risk_level(choice.get("risk_level", "safe"))
                choice.setdefault("next_scene_id", None)
                choice.setdefault("loot", None)
                stat_changes = choice.get("stat_changes")
                if stat_changes is None:
                    stat_changes = {}
                if not isinstance(stat_changes, dict):
                    raise NarrativeComposerError(f"Choice '{choice['id']}' stat_changes must be an object.")
                choice["stat_changes"] = stat_changes
                fixed_choices.append(choice)

            scene["choices"] = fixed_choices

            if not start_scene_id and not scene.get("is_terminal"):
                start_scene_id = scene_id

            fixed_scenes[scene_id] = scene

        data["scenes"] = fixed_scenes
        data["start_scene_id"] = start_scene_id or next(iter(fixed_scenes))

        metadata = data.get("metadata")
        if metadata is None or not isinstance(metadata, dict):
            metadata = {}
        metadata.setdefault("mode", mode)

        stat_names = metadata.get("stat_names") or self.MODE_STAT_PRESETS.get(mode) or ["Courage", "Wisdom", "Chaos"]
        metadata["stat_names"] = stat_names
        metadata.setdefault("summary", "")
        metadata.setdefault("starting_score", metadata.get("starting_score", 0))
        starting_stats = metadata.get("starting_stats")
        if not isinstance(starting_stats, dict):
            starting_stats = {name: 0 for name in stat_names}
        else:
            # Ensure all stat names exist
            for stat in stat_names:
                starting_stats.setdefault(stat, 0)
        metadata["starting_stats"] = starting_stats
        metadata.setdefault("risk_legend", metadata.get("risk_legend") or self.DEFAULT_RISK_LEGEND)
        metadata.setdefault("loot_notes", metadata.get("loot_notes") or "Loot grants stat bonuses shown in choices.")

        data["metadata"] = metadata
        return data

    def _normalize_risk_level(self, risk_level: Any) -> str:
        if isinstance(risk_level, str):
            normalized = risk_level.strip().lower()
        else:
            normalized = "safe"

        replacements = {
            "medium": "risky",
            "moderate": "risky",
            "dangerous": "risky",
            "high": "risky",
            "low": "safe",
            "none": "safe",
            "wild": "chaotic",
            "random": "chaotic",
        }

        normalized = replacements.get(normalized, normalized)
        if normalized not in {"safe", "risky", "chaotic"}:
            normalized = "safe"
        return normalized


