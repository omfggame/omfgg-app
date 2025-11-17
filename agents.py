"""
OMFGG Sub-Agents - Real LLM Implementation
Demonstrates each sub-agent making calls via OpenAI and Anthropic
"""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from anthropic import Anthropic
import asyncio
import json
import random

# Load environment variables
load_dotenv('.env.local')

# Initialize clients
openai_client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Configuration
OPENAI_MODEL = "gpt-4o-mini"  # Fast, cheap, good for parallel agents
ANTHROPIC_MODEL = "claude-3-5-haiku-20241022"  # Fast, cheap Anthropic model (Haiku 4.5 not yet available)
COMPOSER_MODEL = "claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5 for synthesis


class SubAgent:
    """Base class for all sub-agents"""

    def __init__(self, name, role):
        self.name = name
        self.role = role

    async def call_openai(self, prompt, temperature=0.8):
        """Make async call to OpenAI"""
        try:
            response = await openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.role},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

    async def call_anthropic(self, prompt, temperature=0.8):
        """Make async call to Anthropic"""
        try:
            message = anthropic_client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=500,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": f"{self.role}\n\n{prompt}"}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error calling Anthropic: {str(e)}"


class CharacterAgent(SubAgent):
    """Generates character/subject design"""

    def __init__(self):
        super().__init__(
            name="Character Agent",
            role="You are a creative character designer for micro-games. Design visually interesting, simple characters that fit the game's vibe."
        )

    async def generate(self, subject, mode, provider="openai"):
        """Generate character design"""
        prompt = f"""Game Mode: {mode}
Subject: {subject}

Generate a character design with:
- Visual description (colors, shape, style)
- Size (small/medium/large)
- 2-3 key traits
- Animation style suggestion

Keep it simple for a micro-game. Return as JSON:
{{
  "name": "character name",
  "visual": "description",
  "size": "medium",
  "traits": ["trait1", "trait2"],
  "animation_style": "description"
}}"""

        if provider == "openai":
            return await self.call_openai(prompt)
        else:
            return await self.call_anthropic(prompt)


class MechanicAgent(SubAgent):
    """Generates game mechanics"""

    def __init__(self):
        super().__init__(
            name="Mechanic Agent",
            role="You are a game mechanic designer. Create simple, fun interactions for micro-games."
        )

    async def generate(self, action_or_goal, mode, provider="openai"):
        """Generate game mechanics"""
        prompt = f"""Game Mode: {mode}
Action/Goal: {action_or_goal}

Design simple game mechanics:
- Primary interaction (tap, swipe, hold, etc.)
- Win/lose condition (if applicable)
- Progression or scoring
- Duration (5-30 seconds)

Return as JSON:
{{
  "interaction": "description",
  "win_condition": "description or null",
  "scoring": "description",
  "duration_seconds": 15
}}"""

        if provider == "openai":
            return await self.call_openai(prompt)
        else:
            return await self.call_anthropic(prompt)


class StyleAgent(SubAgent):
    """Generates visual style and aesthetics"""

    def __init__(self):
        super().__init__(
            name="Style Agent",
            role="You are a visual style designer. Create cohesive color palettes and aesthetic directions for games."
        )

    async def generate(self, vibe, mode, provider="openai"):
        """Generate style guide"""
        prompt = f"""Game Mode: {mode}
Vibe: {vibe}

Create a visual style guide:
- Color palette (3-5 colors with hex codes)
- Overall mood/tone
- Visual style (pixel art, flat, 3D, etc.)
- Effects suggestions

Return as JSON:
{{
  "colors": ["#FF5733", "#33FF57", "#3357FF"],
  "mood": "description",
  "style": "visual style",
  "effects": ["effect1", "effect2"]
}}"""

        if provider == "openai":
            return await self.call_openai(prompt)
        else:
            return await self.call_anthropic(prompt)


class ConflictAgent(SubAgent):
    """Generates challenges and obstacles"""

    def __init__(self):
        super().__init__(
            name="Conflict Agent",
            role="You are a game challenge designer. Create interesting obstacles and challenges for micro-games."
        )

    async def generate(self, obstacle, mode, provider="openai"):
        """Generate conflict/challenge design"""
        prompt = f"""Game Mode: {mode}
Obstacle: {obstacle}

Design the challenge system:
- Type of obstacle/challenge
- How it appears or behaves
- Difficulty curve (if any)
- How player overcomes it

Return as JSON:
{{
  "challenge_type": "description",
  "behavior": "description",
  "difficulty": "easy/medium/hard",
  "player_response": "how to overcome"
}}"""

        if provider == "openai":
            return await self.call_openai(prompt)
        else:
            return await self.call_anthropic(prompt)


class LevelAgent(SubAgent):
    """Generates environment and setting"""

    def __init__(self):
        super().__init__(
            name="Level Agent",
            role="You are an environment designer. Create simple, evocative game environments."
        )

    async def generate(self, setting, mode, provider="openai"):
        """Generate level/environment design"""
        prompt = f"""Game Mode: {mode}
Setting: {setting}

Design the game environment:
- Background description
- Layout (vertical/horizontal scroll, static, etc.)
- Environmental elements
- Atmosphere/ambiance

Return as JSON:
{{
  "background": "description",
  "layout": "description",
  "elements": ["element1", "element2"],
  "atmosphere": "description"
}}"""

        if provider == "openai":
            return await self.call_openai(prompt)
        else:
            return await self.call_anthropic(prompt)


class TwistAgent(SubAgent):
    """Generates special mechanics and surprises"""

    def __init__(self):
        super().__init__(
            name="Twist Agent",
            role="You are a creative surprise designer. Add unexpected, delightful twists to games."
        )

    async def generate(self, wildcard_or_twist, mode, provider="openai"):
        """Generate twist/special mechanic"""
        prompt = f"""Game Mode: {mode}
Twist/Wildcard: {wildcard_or_twist}

Design a SIMPLE special mechanic or twist:
- What makes it special/unexpected
- How it changes gameplay (KEEP IT SIMPLE - no mini-games!)
- When it appears
- Visual or audio cue

IMPORTANT: Keep it feasible for rapid development. NO games-within-games, NO complex multi-stage interactions.
Think: a visual effect, a simple modifier, a bonus item - not an entire separate game mode.

Return as JSON:
{{
  "mechanic": "description",
  "effect": "how it changes gameplay (1-2 sentences max)",
  "trigger": "when it appears",
  "cue": "visual/audio indication"
}}"""

        if provider == "openai":
            return await self.call_openai(prompt)
        else:
            return await self.call_anthropic(prompt)


class ComposerAgent:
    """Synthesizes all sub-agent outputs into coherent GameDef"""

    def __init__(self):
        self.name = "Composer Agent"

    def compose(self, mode, sub_agent_outputs, game_type="random"):
        """Compose final GameDef from all sub-agent outputs"""
        # Determine game type
        all_game_types = [
            "tap_to_avoid", "side_scroller", "which_doesnt_belong",
            "true_or_false", "memory_match", "emoji_ancestry",
            "sort_sequence", "emoji_rebus"
        ]

        if game_type == "random":
            selected_game_type = random.choice(all_game_types)
        else:
            selected_game_type = game_type

        print(f"[Composer] Selected game type: {selected_game_type}")

        prompt = f"""You are the Composer Agent. Synthesize the following sub-agent outputs into a flat JSON structure for a playable game.

Game Mode: {mode}
Game Type: {selected_game_type}

Sub-Agent Outputs:
{json.dumps(sub_agent_outputs, indent=2)}

IMPORTANT CONSTRAINTS:
- Keep it SIMPLE and FEASIBLE - this is a micro-game (5-30 seconds)
- Adapt the theme to fit the game type, regardless of what the sub-agents suggested
- NO mini-games within games
- NO complex multi-stage interactions
- Speed of development is the priority
- Think mobile-friendly, single-screen, instant-play

GAME TYPE DESCRIPTIONS:
1. tap_to_avoid: Tap to move horizontally, avoid falling obstacles
2. side_scroller: Auto-run right, tap to jump over ground obstacles
3. which_doesnt_belong: Find the odd one out (5 rounds, 4 options each)
4. true_or_false: Answer true/false questions (6 questions)
5. memory_match: Match pairs of emoji (6 unique emoji = 12 cards)
6. emoji_ancestry: Combine emoji to discover the Ancient Ancestor (8-12 breeding pairs, 2-3 minutes gameplay)
7. sort_sequence: Sort items in correct order (3 puzzles)
8. emoji_rebus: Decode emoji puzzles (3 puzzles)

EMOJI EXTRACTION:
- Extract emoji characters from sub-agent outputs or create appropriate ones based on the theme
- Use actual emoji characters (e.g., "☁️", "💨", "🍌"), not text descriptions

BACKGROUND COLOR:
- Select a hex color that matches the theme and vibe from the style agent's color palette
- Choose the most appropriate background color that enhances the game's atmosphere

WIN/LOSE MESSAGES:
- Generate short, thematic messages based on the game context
- Should reflect the game's vibe (funny, relaxing, scary, etc.)
- Keep them brief (3-8 words each)

JSON STRUCTURE BY GAME TYPE:

For "tap_to_avoid" or "side_scroller":
{{
  "game_type": "{selected_game_type}",
  "title": "Game Title",
  "player_emoji": "☁️",
  "obstacle_emoji": "💨",
  "background_color": "#FFB366",
  "win_message": "You floated peacefully!",
  "lose_message": "Too much wind!"
}}

For "which_doesnt_belong":
{{
  "game_type": "which_doesnt_belong",
  "title": "Game Title",
  "background_color": "#FFB366",
  "rounds": [
    {{"options": ["🍎", "🍊", "🍌", "🚗"], "correct_index": 3, "explanation": "One is not a fruit"}},
    {{"options": ["😀", "😂", "😢", "🏠"], "correct_index": 3, "explanation": "One is not an emoji face"}},
    {{"options": ["🐶", "🐱", "🐭", "🌳"], "correct_index": 3, "explanation": "One is not an animal"}},
    {{"options": ["⚽", "🏀", "🎾", "🍕"], "correct_index": 3, "explanation": "One is not a ball"}},
    {{"options": ["🌞", "🌙", "⭐", "🍔"], "correct_index": 3, "explanation": "One is not in the sky"}}
  ],
  "win_message": "You found them all!",
  "lose_message": "Try again!"
}}

For "true_or_false":
{{
  "game_type": "true_or_false",
  "title": "Game Title",
  "background_color": "#FFB366",
  "player_emoji": "🤔",
  "questions": [
    {{"statement": "The sky is blue", "answer": true}},
    {{"statement": "Fish can fly", "answer": false}},
    {{"statement": "Water is wet", "answer": true}},
    {{"statement": "Dogs meow", "answer": false}},
    {{"statement": "Ice is cold", "answer": true}},
    {{"statement": "Fire is cold", "answer": false}}
  ],
  "win_message": "Truth master!",
  "lose_message": "False start!"
}}

For "memory_match":
{{
  "game_type": "memory_match",
  "title": "Game Title",
  "background_color": "#FFB366",
  "emoji_pairs": ["🍎", "🍊", "🍌", "🍇", "🍓", "🍒"],
  "win_message": "Perfect match!",
  "lose_message": "Memory lapse!"
}}

For "emoji_ancestry":
{{
  "game_type": "emoji_ancestry",
  "title": "Game Title",
  "background_color": "#FFB366",
  "seed_emoji": [
    {{"emoji": "🥒", "name": "Pickle"}},
    {{"emoji": "💃", "name": "Dancer"}},
    {{"emoji": "😰", "name": "Nervous"}},
    {{"emoji": "🎅", "name": "Santa"}},
    {{"emoji": "🐰", "name": "Bunny"}}
  ],
  "breeding_pairs": [
    {{"parent1": "🥒", "parent2": "💃", "child": "🕺", "name": "Dancing Pickle", "description": "A pickle with moves!"}},
    {{"parent1": "😰", "parent2": "🎅", "child": "🎄", "name": "Nervous Christmas", "description": "Holiday anxiety"}},
    {{"parent1": "🎄", "parent2": "🐰", "child": "🎁", "name": "Easter Gift", "description": "Wrong holiday!"}},
    {{"parent1": "🕺", "parent2": "🎁", "child": "🌟", "name": "Party Star", "description": "The ancient ancestor!"}},
    {{"parent1": "🥒", "parent2": "🐰", "child": "🥕", "name": "Bunny Snack", "description": "Rabbits love veggies"}},
    {{"parent1": "💃", "parent2": "🎅", "child": "🔔", "name": "Jingle Dancer", "description": "Santa's got rhythm"}},
    {{"parent1": "😰", "parent2": "🐰", "child": "🐇", "name": "Anxious Rabbit", "description": "Always hopping away"}},
    {{"parent1": "🥕", "parent2": "🔔", "child": "🎺", "name": "Veggie Horn", "description": "Musical produce"}},
    {{"parent1": "🐇", "parent2": "🎄", "child": "🎀", "name": "Holiday Bow", "description": "Wrapped up nicely"}},
    {{"parent1": "🎀", "parent2": "🎺", "child": "🌟", "name": "Celebration Star", "description": "The ancient ancestor!"}}
  ],
  "ancestor_emoji": "🌟",
  "ancestor_name": "The Celebration Star - origin of all joy!",
  "hints": [
    "Try combining your starting emoji first",
    "The ancestor connects all your keywords",
    "Mix different discoveries together",
    "Some paths lead to the same ancestor"
  ],
  "win_message": "You found the Ancient Ancestor!",
  "lose_message": "Keep exploring!"
}}

IMPORTANT FOR EMOJI_ANCESTRY:
- Create 8-12 breeding_pairs that form a discovery tree
- The ancestor_emoji should appear as the "child" in at least 2 different breeding pairs (multiple paths to victory)
- seed_emoji should be 4-6 emoji derived from the Mad Lib keywords (Subject, Action, Vibe, Setting, Twist)
- Each breeding pair should feel logical or humorously absurd based on the theme
- breeding_pairs should allow players to discover 8-12 new emoji before finding the ancestor
- Make sure multiple combination paths lead to the ancestor emoji for replayability

For "sort_sequence":
{{
  "game_type": "sort_sequence",
  "title": "Game Title",
  "background_color": "#FFB366",
  "puzzles": [
    {{"items": ["🥚", "🐣", "🐥", "🐔"], "correct_order": [0, 1, 2, 3], "prompt": "Life cycle of a chicken", "explanation": "Egg, hatching, chick, then chicken"}},
    {{"items": ["🌱", "🌿", "🌳", "🍎"], "correct_order": [0, 1, 2, 3], "prompt": "Growth of an apple tree", "explanation": "Seedling, sprout, tree, then fruit"}},
    {{"items": ["☁️", "🌧️", "💧", "🌊"], "correct_order": [0, 1, 2, 3], "prompt": "Water cycle", "explanation": "Cloud, rain, droplet, then ocean"}}
  ],
  "win_message": "Perfect order!",
  "lose_message": "Out of sequence!"
}}

For "emoji_rebus":
{{
  "game_type": "emoji_rebus",
  "title": "Game Title",
  "background_color": "#FFB366",
  "puzzles": [
    {{"emoji_sequence": ["🐝", "🍃"], "accepted_answers": ["believe", "bee leaf"], "hint": "Insect + leaf"}},
    {{"emoji_sequence": ["👁️", "❤️", "🐑"], "accepted_answers": ["i love you", "eye love ewe"], "hint": "Eye + heart + ewe"}},
    {{"emoji_sequence": ["☀️", "🌻"], "accepted_answers": ["sunflower", "sun flower"], "hint": "Sun + flower"}}
  ],
  "win_message": "Puzzle master!",
  "lose_message": "Rebus confuses!"
}}

IMPORTANT:
- game_type must be "{selected_game_type}" for this game
- All emoji must be actual Unicode emoji characters
- background_color must be a valid hex color
- Generate thematic content that matches the game mode and sub-agent outputs
- For intellectual games, create content that fits the theme (e.g., space theme = space questions)
- Ensure all elements are coherent and work together!

Return ONLY valid JSON matching the structure above for game type "{selected_game_type}"."""

        try:
            message = anthropic_client.messages.create(
                model=COMPOSER_MODEL,  # Use higher quality model
                max_tokens=2000,  # Increased for intellectual games with more content
                temperature=0.3,  # Lower temp for structured output
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse the JSON response
            response_text = message.content[0].text

            # Try to extract JSON if wrapped in markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            # Parse and return as dictionary
            game_json = json.loads(response_text)
            return game_json

        except json.JSONDecodeError as e:
            return {"error": f"JSON parsing error: {str(e)}", "raw_response": response_text}
        except Exception as e:
            return {"error": f"Error in Composer: {str(e)}"}


# Demonstration functions

async def demo_single_agent(provider="openai"):
    """Demonstrate a single agent call"""
    print(f"\n{'='*60}")
    print(f"DEMO: Single Agent Call ({provider.upper()})")
    print(f"{'='*60}\n")

    agent = CharacterAgent()
    result = await agent.generate(
        subject="dancing pickle",
        mode="Funny",
        provider=provider
    )

    print(f"Character Agent ({provider}):")
    print(result)
    print()


async def demo_all_agents_parallel(provider="openai"):
    """Demonstrate all agents running in parallel"""
    print(f"\n{'='*60}")
    print(f"DEMO: All Agents Parallel ({provider.upper()})")
    print(f"{'='*60}\n")

    # Create all agents
    character = CharacterAgent()
    mechanic = MechanicAgent()
    style = StyleAgent()
    conflict = ConflictAgent()
    level = LevelAgent()
    twist = TwistAgent()

    # Sample inputs (Funny mode)
    inputs = {
        "subject": "confused robot",
        "action": "wobbling",
        "vibe": "slapstick",
        "obstacle": "banana peels",
        "setting": "giant kitchen",
        "twist": "gravity reversal"
    }

    print(f"Launching 6 sub-agents in parallel using {provider}...")
    print(f"Inputs: {inputs}\n")

    # Run all agents in parallel
    results = await asyncio.gather(
        character.generate(inputs["subject"], "Funny", provider),
        mechanic.generate(inputs["action"], "Funny", provider),
        style.generate(inputs["vibe"], "Funny", provider),
        conflict.generate(inputs["obstacle"], "Funny", provider),
        level.generate(inputs["setting"], "Funny", provider),
        twist.generate(inputs["twist"], "Funny", provider)
    )

    # Display results
    agents = [character, mechanic, style, conflict, level, twist]
    for agent, result in zip(agents, results):
        print(f"\n{agent.name}:")
        print(f"{result}")
        print(f"{'-'*60}")


async def demo_full_pipeline(provider="openai"):
    """Demonstrate complete pipeline: sub-agents → composer"""
    print(f"\n{'='*60}")
    print(f"DEMO: Full Pipeline ({provider.upper()} → Claude Composer)")
    print(f"{'='*60}\n")

    # Create all agents
    agents = {
        "character": CharacterAgent(),
        "mechanic": MechanicAgent(),
        "style": StyleAgent(),
        "conflict": ConflictAgent(),
        "level": LevelAgent(),
        "twist": TwistAgent()
    }

    composer = ComposerAgent()

    # Sample inputs
    inputs = {
        "subject": "sleepy cloud",
        "action": "floating gently",
        "vibe": "peaceful",
        "obstacle": "mild breeze",
        "setting": "sunset sky",
        "twist": "rainbow trail"
    }

    mode = "Relaxing"

    print(f"Step 1: Launching {len(agents)} sub-agents in parallel...")
    print(f"Mode: {mode}")
    print(f"Inputs: {inputs}\n")

    # Run sub-agents
    results = await asyncio.gather(
        agents["character"].generate(inputs["subject"], mode, provider),
        agents["mechanic"].generate(inputs["action"], mode, provider),
        agents["style"].generate(inputs["vibe"], mode, provider),
        agents["conflict"].generate(inputs["obstacle"], mode, provider),
        agents["level"].generate(inputs["setting"], mode, provider),
        agents["twist"].generate(inputs["twist"], mode, provider)
    )

    # Package results
    sub_agent_outputs = {
        "character": results[0],
        "mechanic": results[1],
        "style": results[2],
        "conflict": results[3],
        "level": results[4],
        "twist": results[5]
    }

    print("Sub-agents complete!\n")

    print("Step 2: Launching Composer Agent (Claude Sonnet)...")
    game_def = composer.compose(mode, sub_agent_outputs)

    print("\nFinal GameDef:")
    print(json.dumps(game_def, indent=2))
    print()


# Main demo runner
async def main():
    """Run all demonstrations"""
    print("\n" + "="*60)
    print("OMFGG SUB-AGENT DEMONSTRATIONS")
    print("="*60)

    # Demo 1: Single agent with OpenAI
    await demo_single_agent(provider="openai")

    # Demo 2: Single agent with Anthropic
    await demo_single_agent(provider="anthropic")

    # Demo 3: All agents parallel with OpenAI
    await demo_all_agents_parallel(provider="openai")

    # Demo 4: All agents parallel with Anthropic
    await demo_all_agents_parallel(provider="anthropic")

    # Demo 5: Full pipeline (OpenAI agents → Claude composer)
    await demo_full_pipeline(provider="openai")

    print("\n" + "="*60)
    print("ALL DEMONSTRATIONS COMPLETE!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Check for API keys
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not found in .env.local")
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  Warning: ANTHROPIC_API_KEY not found in .env.local")

    # Run demos
    asyncio.run(main())
