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

    def compose(self, mode, sub_agent_outputs):
        """Compose final GameDef from all sub-agent outputs"""
        prompt = f"""You are the Composer Agent. Synthesize the following sub-agent outputs into a flat JSON structure for a playable game.

Game Mode: {mode}

Sub-Agent Outputs:
{json.dumps(sub_agent_outputs, indent=2)}

IMPORTANT CONSTRAINTS:
- Keep it SIMPLE and FEASIBLE - this is a micro-game (5-30 seconds)
- GAME TYPE MUST BE "tap_to_avoid" (tap to move horizontally, avoid falling obstacles)
- Adapt the theme to fit this mechanic, regardless of what the sub-agents suggested
- NO mini-games within games
- NO complex multi-stage interactions
- Speed of development is the priority
- Think mobile-friendly, single-screen, instant-play

EMOJI EXTRACTION:
- Extract emoji characters from sub-agent outputs (character for player, obstacle for obstacles)
- Look for emoji in the visual descriptions or create appropriate ones based on the theme
- Use actual emoji characters (e.g., "☁️", "💨", "🍌"), not text descriptions

BACKGROUND COLOR:
- Select a hex color that matches the theme and vibe from the style agent's color palette
- Choose the most appropriate background color that enhances the game's atmosphere

WIN/LOSE MESSAGES:
- Generate short, thematic messages based on the game context
- Should reflect the game's vibe (funny, relaxing, scary, etc.)
- Keep them brief (3-8 words each)

Return as valid JSON with this EXACT flat structure:
{{
  "game_type": "tap_to_avoid",
  "title": "Game Title",
  "player_emoji": "☁️",
  "obstacle_emoji": "💨",
  "background_color": "#FFB366",
  "win_message": "You floated peacefully!",
  "lose_message": "Too much wind!"
}}

IMPORTANT:
- game_type should match the mode and mechanic (e.g., "tap_to_avoid", "swipe_to_collect", "hold_to_charge")
- All emoji must be actual Unicode emoji characters
- background_color must be a valid hex color
- Ensure all elements are coherent and work together!"""

        try:
            message = anthropic_client.messages.create(
                model=COMPOSER_MODEL,  # Use higher quality model
                max_tokens=1000,
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
