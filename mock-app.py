import gradio as gr
import time
import random

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

def generate_game(mode, field1, field2, field3, field4, field5):
    """Mock game generation with sub-agent launches"""

    # Collect non-empty fields
    fields = MODE_FIELDS.get(mode, [])
    user_inputs = {}
    for i, value in enumerate([field1, field2, field3, field4, field5]):
        if i < len(fields) and value.strip():
            field_name = fields[i][0]
            user_inputs[field_name] = value

    if not user_inputs:
        yield "⚠️ Please fill in at least one field!", None
        return

    # Start generation
    yield f"🎮 **{get_random_omfgg()}**\n\n🚀 Starting game generation...\n", None
    time.sleep(0.5)

    # Launch sub-agents based on mode and fields
    agents_to_launch = []

    if "Subject" in user_inputs:
        agents_to_launch.append(("Character Agent", f"Creating character: '{user_inputs['Subject']}'"))
    if "Action" in user_inputs or "Goal" in user_inputs:
        agents_to_launch.append(("Mechanic Agent", "Designing core game mechanics"))
    if "Vibe" in user_inputs:
        agents_to_launch.append(("Style Agent", f"Crafting aesthetic: '{user_inputs['Vibe']}'"))
    if "Obstacle" in user_inputs:
        agents_to_launch.append(("Conflict Agent", f"Building challenges: '{user_inputs['Obstacle']}'"))
    if "Setting" in user_inputs:
        agents_to_launch.append(("Level Agent", f"Constructing environment: '{user_inputs['Setting']}'"))
    if "Wildcard" in user_inputs or "Twist" in user_inputs or "Chaos Modifier" in user_inputs:
        twist_value = user_inputs.get("Wildcard") or user_inputs.get("Twist") or user_inputs.get("Chaos Modifier")
        agents_to_launch.append(("Twist Agent", f"Adding special mechanic: '{twist_value}'"))

    # For Surprise Me mode, launch all agents
    if mode == "Surprise Me":
        agents_to_launch = [
            ("Character Agent", "Auto-generating character"),
            ("Mechanic Agent", "Auto-designing mechanics"),
            ("Style Agent", f"Creating {user_inputs.get('Vibe', 'random')} aesthetic"),
            ("Conflict Agent", "Auto-generating challenges"),
            ("Level Agent", "Auto-building environment"),
            ("Twist Agent", "Adding surprise element")
        ]

    # Launch agents in parallel (mock)
    status = f"🎮 **{get_random_omfgg()}**\n\n🚀 Starting game generation...\n\n"
    status += "⚡ **Launching sub-agents in parallel:**\n"
    for agent_name, description in agents_to_launch:
        status += f"  • 🤖 Launching **{agent_name}** - {description}\n"

    yield status, None
    time.sleep(1.5)

    # Show agents working
    status += "\n⏳ **Agents working...**\n"
    for agent_name, _ in agents_to_launch:
        status += f"  ✓ {agent_name} processing...\n"
        yield status, None
        time.sleep(0.4)

    # Composer agent
    status += "\n🎼 **Launching Composer Agent**\n"
    status += "  • Collecting sub-agent outputs...\n"
    yield status, None
    time.sleep(0.6)

    status += "  • Validating coherence...\n"
    yield status, None
    time.sleep(0.5)

    status += "  • Constructing GameDef JSON...\n"
    yield status, None
    time.sleep(0.5)

    status += "  • Saving via MCP (Supabase)...\n"
    yield status, None
    time.sleep(0.5)

    # Generate mock game slug
    slug = f"{mode.lower()}-{random.randint(1000, 9999)}"
    status += f"  • Generated shareable slug: **{slug}**\n"
    yield status, None
    time.sleep(0.5)

    # Final result
    status += "\n✅ **Game generation complete!**\n\n"

    # Create mock game preview
    game_preview = f"""
# 🎮 Your {mode} Game

## Game Details:
"""
    for field_name, value in user_inputs.items():
        game_preview += f"- **{field_name}**: {value}\n"

    game_preview += f"""
## Shareable Link:
`omfgg.com/{slug}`

## What Happened:
Your game was generated using {len(agents_to_launch)} specialized AI agents working in parallel!

### Agent Outputs (Mock):
"""

    for agent_name, description in agents_to_launch:
        game_preview += f"- **{agent_name}**: {description} ✓\n"

    game_preview += f"""
---
*Game would render here in full implementation*

**Next Steps**:
- Share with friends!
- Remix this game
- Create another masterpiece
"""

    yield status, game_preview

# Build the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="OMFGG - Game Generator") as demo:

    # Header
    gr.Markdown(f"""
    # 🎮 OMFGG
    ### {get_random_omfgg()}

    Fill in a few words and watch AI generate a ridiculous micro-game in seconds!
    """)

    # Mode Selection
    with gr.Row():
        mode_selector = gr.Radio(
            choices=["Relaxing", "Funny", "Chaotic", "Challenge", "Surprise Me"],
            value="Funny",
            label="🎯 Choose Your Game Mode",
            info="Different modes unlock different creative fields"
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

    # Generate Button
    generate_btn = gr.Button("🚀 Generate My Game!", variant="primary", size="lg")

    # Output sections
    gr.Markdown("## 🔄 Generation Status")
    status_output = gr.Markdown()

    gr.Markdown("## 🎮 Your Game")
    game_output = gr.Markdown()

    # Event Handlers
    mode_selector.change(
        fn=update_fields,
        inputs=[mode_selector],
        outputs=field_components
    )

    generate_btn.click(
        fn=generate_game,
        inputs=[mode_selector] + field_textboxes,
        outputs=[status_output, game_output]
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
