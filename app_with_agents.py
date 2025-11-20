import gradio as gr
import asyncio
import random
import json
import logging
import html
from datetime import datetime
from pathlib import Path
from agents import (
    CharacterAgent, MechanicAgent, StyleAgent,
    ConflictAgent, LevelAgent, TwistAgent, ComposerAgent
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('omfgg_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cache directory for persistent storage across app restarts
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
LATEST_CACHE_FILE = CACHE_DIR / "latest_cache.json"

# Template directory
TEMPLATE_DIR = Path("templates")

def render_game_iframe(game_json_str):
    """
    Load the tap_to_avoid.html template, populate it with game data,
    and return an iframe element using srcdoc.

    Args:
        game_json_str: JSON string from Composer Agent

    Returns:
        HTML string containing iframe with the game
    """
    try:
        # Parse the game JSON (handle both dict and string)
        if isinstance(game_json_str, dict):
            game_data = game_json_str
        else:
            game_data = json.loads(game_json_str)

        # Debug log the game data
        logger.info(f"Rendering game with data: {json.dumps(game_data, indent=2)}")

        # Load the template
        template_path = TEMPLATE_DIR / "tap_to_avoid.html"
        if not template_path.exists():
            return f"<p>Error: Template not found at {template_path}</p>"

        with open(template_path, 'r') as f:
            template = f.read()

        # Replace template variables with game data
        html_content = template.replace('{{player_emoji}}', game_data.get('player_emoji', '😀'))
        html_content = html_content.replace('{{obstacle_emoji}}', game_data.get('obstacle_emoji', '💣'))
        html_content = html_content.replace('{{background_color}}', game_data.get('background_color', '#87CEEB'))
        html_content = html_content.replace('{{win_message}}', game_data.get('win_message', 'You Win!'))
        html_content = html_content.replace('{{lose_message}}', game_data.get('lose_message', 'Game Over!'))

        # Escape the HTML for use in srcdoc attribute
        escaped_html = html.escape(html_content, quote=True)

        # Create iframe with srcdoc
        iframe_html = f'''
        <div style="width: 100%; max-width: 420px; margin: 0 auto;">
            <iframe
                srcdoc="{escaped_html}"
                width="100%"
                height="700px"
                style="border: none; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);"
                sandbox="allow-scripts"
            ></iframe>
        </div>
        '''

        return iframe_html

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in render_game_iframe: {str(e)}")
        return f"<p>Error: Invalid game JSON - {str(e)}</p>"
    except Exception as e:
        logger.error(f"Error rendering game iframe: {str(e)}", exc_info=True)
        return f"<p>Error rendering game: {str(e)}</p>"

def save_cache(sub_agent_outputs, mode, user_inputs):
    """Save sub-agent results to JSON file for persistence across restarts"""
    cache_data = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "user_inputs": user_inputs,
        "sub_agent_outputs": sub_agent_outputs
    }
    try:
        with open(LATEST_CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2)
        logger.info(f"💾 Cache saved to {LATEST_CACHE_FILE}")
        return True
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")
        return False

def load_cache():
    """Load most recent sub-agent results from JSON file"""
    try:
        if LATEST_CACHE_FILE.exists():
            with open(LATEST_CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
            timestamp = cache_data.get('timestamp', 'unknown')
            logger.info(f"📂 Cache loaded from {LATEST_CACHE_FILE} (saved: {timestamp})")
            return cache_data.get('sub_agent_outputs')
        else:
            logger.info("No cache file found - will create on first generation")
            return None
    except Exception as e:
        logger.error(f"Failed to load cache: {e}")
        return None

# OMFGG Acronym Generator
def get_random_omfgg():
    acronyms = [
        "Our Mad-Lib Factory Generates Games",
        "One Mistyped Form: Great Game!",
        "Obliviously Mashing Fields: Good Game",
        "Overloaded Machine Forming Goofy Games",
        "Oddly Magical Fun Game Generator",
        "Overly Melodramatic Fake Game Generator"
    ]
    return random.choice(acronyms)

# Mode-specific field configurations
MODE_FIELDS = {
    "Relaxing": [
        ("Subject", "What you interact with (e.g., butterfly, cloud, leaf)"),
        ("Vibe", "Calm/zen/cozy feeling (e.g., peaceful, serene, gentle)"),
        ("Setting", "Peaceful location (e.g., garden, beach, forest)"),
        ("Wildcard", "Gentle mechanic (e.g., floating, drifting, breathing)")
    ],
    "Funny": [
        ("Subject", "Silly character/thing (e.g., dancing pickle, confused robot)"),
        ("Action", "Absurd verb (e.g., wobbling, exploding, yodeling)"),
        ("Vibe", "Comedic tone (e.g., slapstick, witty, ridiculous)"),
        ("Setting", "Weird location (e.g., giant toilet, moon cheese factory)"),
        ("Twist", "Unexpected element (e.g., surprise mustache, gravity reversal)")
    ],
    "Chaotic": [
        ("Subject", "Fast-moving character (e.g., caffeinated squirrel, rocket)"),
        ("Action", "Frantic verb (e.g., dodging, bouncing, spinning)"),
        ("Obstacle", "Hazard/challenge (e.g., falling pianos, laser beams)"),
        ("Chaos Modifier", "Randomness factor (e.g., screen shake, color swap)"),
        ("Setting", "Dynamic location (e.g., collapsing tower, speeding train)")
    ],
    "Challenge": [
        ("Subject", "Player character (e.g., ninja, space explorer, chef)"),
        ("Goal", "Win condition (e.g., collect 10 stars, reach the top)"),
        ("Obstacle", "Challenge/antagonist (e.g., evil wizard, time limit)"),
        ("Setting", "Game arena (e.g., volcano, underwater cave, city rooftop)"),
        ("Twist", "Power-up/mechanic (e.g., double jump, invisibility)")
    ],
    "Surprise Me": [
        ("Vibe", "Just one word to set the mood (e.g., mysterious, explosive)")
    ]
}

def update_fields(mode):
    """Update form fields based on selected mode"""
    fields = MODE_FIELDS.get(mode, [])

    # Create visibility updates and textbox updates
    updates = []

    for i in range(5):  # Max 5 fields
        if i < len(fields):
            label, placeholder = fields[i]
            updates.extend([
                gr.update(visible=True, label=label, placeholder=placeholder, value=""),
                gr.update(visible=True)
            ])
        else:
            updates.extend([
                gr.update(visible=False),
                gr.update(visible=False)
            ])

    return updates


async def generate_game_real(mode, field1, field2, field3, field4, field5, cached_results, provider="openai"):
    """Real game generation with LLM agents and caching"""

    logger.info(f"Starting game generation - Mode: {mode}, Provider: {provider}")

    # Collect non-empty fields
    fields = MODE_FIELDS.get(mode, [])
    user_inputs = {}
    for i, value in enumerate([field1, field2, field3, field4, field5]):
        if i < len(fields) and value.strip():
            field_name = fields[i][0]
            user_inputs[field_name] = value

    logger.info(f"User inputs: {user_inputs}")

    if not user_inputs:
        logger.warning("No user inputs provided")
        debug_info = json.dumps({"error": "No user inputs provided"}, indent=2)
        yield "⚠️ Please fill in at least one field!", None, None, debug_info
        return

    # Start generation
    status = f"🎮 **{get_random_omfgg()}**\n\n🚀 Starting game generation...\n"
    debug_data = {"mode": mode, "provider": provider, "user_inputs": user_inputs, "sub_agents": {}}
    yield status, None, cached_results, json.dumps(debug_data, indent=2)

    await asyncio.sleep(0.3)

    # Create agents
    agents = {
        "character": CharacterAgent(),
        "mechanic": MechanicAgent(),
        "style": StyleAgent(),
        "conflict": ConflictAgent(),
        "level": LevelAgent(),
        "twist": TwistAgent()
    }

    # Determine which agents to launch based on inputs
    agent_tasks = []
    agent_names = []

    if "Subject" in user_inputs:
        agent_tasks.append(agents["character"].generate(user_inputs["Subject"], mode, provider))
        agent_names.append("Character Agent")

    if "Action" in user_inputs or "Goal" in user_inputs:
        action_or_goal = user_inputs.get("Action") or user_inputs.get("Goal")
        agent_tasks.append(agents["mechanic"].generate(action_or_goal, mode, provider))
        agent_names.append("Mechanic Agent")

    if "Vibe" in user_inputs:
        agent_tasks.append(agents["style"].generate(user_inputs["Vibe"], mode, provider))
        agent_names.append("Style Agent")

    if "Obstacle" in user_inputs:
        agent_tasks.append(agents["conflict"].generate(user_inputs["Obstacle"], mode, provider))
        agent_names.append("Conflict Agent")

    if "Setting" in user_inputs:
        agent_tasks.append(agents["level"].generate(user_inputs["Setting"], mode, provider))
        agent_names.append("Level Agent")

    if "Wildcard" in user_inputs or "Twist" in user_inputs or "Chaos Modifier" in user_inputs:
        twist_value = user_inputs.get("Wildcard") or user_inputs.get("Twist") or user_inputs.get("Chaos Modifier")
        agent_tasks.append(agents["twist"].generate(twist_value, mode, provider))
        agent_names.append("Twist Agent")

    # For Surprise Me mode, launch all agents
    if mode == "Surprise Me":
        agent_tasks = [
            agents["character"].generate(user_inputs.get("Vibe", "random"), mode, provider),
            agents["mechanic"].generate("auto-generate", mode, provider),
            agents["style"].generate(user_inputs.get("Vibe", "random"), mode, provider),
            agents["conflict"].generate("auto-generate", mode, provider),
            agents["level"].generate("auto-generate", mode, provider),
            agents["twist"].generate("surprise", mode, provider)
        ]
        agent_names = ["Character Agent", "Mechanic Agent", "Style Agent", "Conflict Agent", "Level Agent", "Twist Agent"]

    logger.info(f"Launching {len(agent_names)} agents: {agent_names}")

    # Show agents launching
    status += "\n⚡ **Launching sub-agents in parallel:**\n"
    for name in agent_names:
        status += f"  • 🤖 Launching **{name}**\n"
    status += f"\n*Using {provider.upper()} API*\n"
    debug_data["launched_agents"] = agent_names
    yield status, None, cached_results, json.dumps(debug_data, indent=2)

    await asyncio.sleep(0.5)

    # Run agents in parallel
    status += "\n⏳ **Running agents in parallel...**\n"
    yield status, None, cached_results, json.dumps(debug_data, indent=2)

    try:
        results = await asyncio.gather(*agent_tasks)

        logger.info(f"All {len(results)} agents completed successfully")

        # Package results with names
        sub_agent_outputs = {}
        for name, result in zip(agent_names, results):
            # Extract just the agent type name (e.g., "Character" from "Character Agent")
            key = name.replace(" Agent", "").lower()
            sub_agent_outputs[key] = result
            debug_data["sub_agents"][key] = result
            status += f"  ✓ {name} complete\n"
            yield status, None, cached_results, json.dumps(debug_data, indent=2)

        logger.info("Sub-agent results collected and cached")

        # Save cache to JSON file for persistence across restarts
        save_cache(sub_agent_outputs, mode, user_inputs)

        status += "\n✅ **All sub-agents complete!**\n"
        status += "💾 *Results cached to disk for next session*\n"
        yield status, None, sub_agent_outputs, json.dumps(debug_data, indent=2)

        await asyncio.sleep(0.3)

        # Launch Composer Agent
        logger.info("Launching Composer Agent")
        status += "\n🎼 **Launching Composer Agent**\n"
        status += "  • Collecting sub-agent outputs...\n"
        yield status, None, sub_agent_outputs, json.dumps(debug_data, indent=2)

        await asyncio.sleep(0.3)

        composer = ComposerAgent()
        game_def = composer.compose(mode, sub_agent_outputs)

        debug_data["composer_output"] = game_def
        logger.info(f"Composer Agent completed - Generated GameDef")

        status += "  • Validating coherence...\n"
        status += "  • Constructing GameDef JSON...\n"
        yield status, None, sub_agent_outputs, json.dumps(debug_data, indent=2)

        await asyncio.sleep(0.3)

        # Generate slug
        slug = f"{mode.lower()}-{random.randint(1000, 9999)}"
        debug_data["slug"] = slug
        status += f"  • Generated shareable slug: **{slug}**\n"
        yield status, None, sub_agent_outputs, json.dumps(debug_data, indent=2)

        await asyncio.sleep(0.3)

        status += "\n✅ **Game generation complete!**\n\n"

        # Render the game in an iframe
        game_iframe = render_game_iframe(game_def)

        logger.info("Game generation completed successfully")
        yield status, game_iframe, sub_agent_outputs, json.dumps(debug_data, indent=2)

    except Exception as e:
        logger.error(f"Error during game generation: {str(e)}", exc_info=True)
        error_status = status + f"\n\n❌ **Error:** {str(e)}\n\nPlease check your API keys in .env.local"
        debug_data["error"] = str(e)
        yield error_status, None, cached_results, json.dumps(debug_data, indent=2)


async def regenerate_gamedef(mode, cached_results):
    """Regenerate GameDef using cached sub-agent results (saves API calls!)"""
    debug_data = {"mode": mode, "cached_results_present": bool(cached_results)}

    if not cached_results:
        logger.warning("Regeneration attempted without cached results")
        debug_data["error"] = "No cached results available"
        yield "⚠️ No cached results available. Please generate a game first!", None, json.dumps(debug_data, indent=2)
        return

    logger.info(f"Regenerating GameDef from cached results - Mode: {mode}")

    status = "🔄 **Regenerating GameDef from cached results...**\n\n"
    status += "💰 **Saving API costs by reusing sub-agent outputs!**\n\n"

    debug_data["sub_agents"] = cached_results
    yield status, None, json.dumps(debug_data, indent=2)

    await asyncio.sleep(0.3)

    logger.info("Launching Composer Agent for regeneration")
    status += "🎼 **Launching Composer Agent**\n"
    yield status, None, json.dumps(debug_data, indent=2)

    composer = ComposerAgent()
    game_def = composer.compose(mode, cached_results)

    debug_data["composer_output"] = game_def
    logger.info("Composer Agent completed - GameDef regenerated")

    await asyncio.sleep(0.5)

    slug = f"{mode.lower()}-{random.randint(1000, 9999)}"
    debug_data["slug"] = slug

    # Render the game in an iframe
    game_iframe = render_game_iframe(game_def)

    status += "\n✅ **GameDef regenerated!**\n"
    logger.info("GameDef regeneration completed successfully")
    yield status, game_iframe, json.dumps(debug_data, indent=2)


# Build the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="OMFGG - Game Generator") as demo:

    # Header
    gr.Markdown(f"""
    # 🎮 OMFGG
    ### {get_random_omfgg()}

    Fill in a few words and watch AI agents generate a ridiculous micro-game in seconds!

    **Now with REAL AI agents!** 🤖
    """)

    # Mode Selection
    with gr.Row():
        mode_selector = gr.Radio(
            choices=["Relaxing", "Funny", "Chaotic", "Challenge", "Surprise Me"],
            value="Funny",
            label="🎯 Choose Your Game Mode",
            info="Different modes unlock different creative fields"
        )

    with gr.Row():
        provider_selector = gr.Radio(
            choices=["openai", "anthropic"],
            value="openai",
            label="🤖 AI Provider for Sub-Agents",
            info="OpenAI (GPT-4o mini) or Anthropic (Claude Haiku 4.5)"
        )

    # Adaptive Mad-Lib Form
    gr.Markdown("## 📝 Fill in the Mad-Lib")

    with gr.Column():
        # Create 5 field rows (max needed)
        field_components = []
        for i in range(5):
            with gr.Row(visible=False) as row:
                field = gr.Textbox(
                    label=f"Field {i+1}",
                    placeholder="Enter your creative input...",
                    scale=4
                )
                field_components.append(field)
                field_components.append(row)

        # Extract just textboxes and rows for easier handling
        field_textboxes = [field_components[i] for i in range(0, 10, 2)]
        field_rows = [field_components[i] for i in range(1, 10, 2)]

    # Cached results state (invisible to user)
    # Load from disk on startup for persistence across restarts
    initial_cache = load_cache()
    cached_state = gr.State(value=initial_cache)

    # Generate Button
    generate_btn = gr.Button("🚀 Generate My Game!", variant="primary", size="lg")

    # Regenerate button (uses cached results)
    with gr.Row():
        regenerate_btn = gr.Button("🔄 Regenerate GameDef (Use Cached Results)", variant="secondary", size="sm")
        gr.Markdown("*Regenerate uses cached sub-agent results - saves API calls!*")

    # Output sections
    gr.Markdown("## 🔄 Generation Status")
    status_output = gr.Markdown()

    gr.Markdown("## 🎮 Your Game")
    game_output = gr.HTML()

    # Debug Output Section
    with gr.Accordion("Debug Output (Sub-Agent Results)", open=False):
        debug_output = gr.Code(
            label="Debug Information (JSON)",
            language="json",
            lines=25,
            interactive=False
        )

    # Event Handlers
    mode_selector.change(
        fn=update_fields,
        inputs=[mode_selector],
        outputs=field_components
    )

    generate_btn.click(
        fn=generate_game_real,
        inputs=[mode_selector, *field_textboxes, cached_state, provider_selector],
        outputs=[status_output, game_output, cached_state, debug_output]
    )

    regenerate_btn.click(
        fn=regenerate_gamedef,
        inputs=[mode_selector, cached_state],
        outputs=[status_output, game_output, debug_output]
    )

    # Initialize with default mode fields
    demo.load(
        fn=update_fields,
        inputs=[mode_selector],
        outputs=field_components
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
