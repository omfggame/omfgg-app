# OMFGG Agent Demo Guide

## What We Built Today

We now have **real AI agents** working with both OpenAI and Anthropic APIs!

## Files Created

### Core Agent System
- **`agents.py`** - Complete sub-agent implementation
  - 6 specialized sub-agents (Character, Mechanic, Style, Conflict, Level, Twist)
  - Composer Agent for synthesis
  - Support for both OpenAI (GPT-4o mini) and Anthropic (Claude Haiku 4.5)
  - Async/parallel execution support

### Documentation
- **`MODEL_REFERENCE.md`** - Comprehensive guide to AI models
  - Latest OpenAI models (GPT-4.1, GPT-4o mini, etc.)
  - Latest Anthropic models (Claude 4.5 Haiku, Sonnet, etc.)
  - Cost estimates and recommendations
  - API setup instructions

### Testing
- **`test_agents.py`** - Quick API verification tool
- **`.env.local.example`** - Template for environment variables

## How to Test the Agents

### Quick Test (Single Agent Calls)
```bash
source venv/bin/activate
python test_agents.py
```

This will test both OpenAI and Anthropic APIs with a simple character generation request.

### Full Demo (All Demonstrations)
```bash
source venv/bin/activate
python agents.py
```

This runs 5 demonstrations:
1. Single agent with OpenAI
2. Single agent with Anthropic
3. All 6 agents in parallel with OpenAI
4. All 6 agents in parallel with Anthropic
5. Full pipeline: Sub-agents (OpenAI) → Composer (Claude Sonnet)

## What Each Demo Shows

### Demo 1 & 2: Single Agent Calls
Shows a single Character Agent generating a character design using either OpenAI or Anthropic.

**Example input:**
- Subject: "dancing pickle"
- Mode: "Funny"

**Output:** JSON with character design (name, visual, size, traits, animation style)

### Demo 3 & 4: Parallel Sub-Agents
Shows all 6 sub-agents running simultaneously:
- **Character Agent** - Designs the character
- **Mechanic Agent** - Creates game mechanics
- **Style Agent** - Defines visual aesthetic
- **Conflict Agent** - Designs challenges
- **Level Agent** - Creates environment
- **Twist Agent** - Adds special mechanics

**Example input:**
- Subject: "confused robot"
- Action: "wobbling"
- Vibe: "slapstick"
- Obstacle: "banana peels"
- Setting: "giant kitchen"
- Twist: "gravity reversal"

### Demo 5: Full Pipeline
Shows the complete agentic workflow:
1. **6 sub-agents run in parallel** using OpenAI GPT-4o mini
2. **Composer Agent** synthesizes outputs using Claude Sonnet 4.5
3. **Final GameDef JSON** is generated with all elements coherent

**Example input:**
- Subject: "sleepy cloud"
- Action: "floating gently"
- Vibe: "peaceful"
- Obstacle: "mild breeze"
- Setting: "sunset sky"
- Twist: "rainbow trail"

## Why This Demonstrates Agentic Behavior

✅ **Planning** - Each agent has a specific role and task
✅ **Autonomous Execution** - Agents run independently with their own prompts
✅ **Tool Usage** - Agents use LLM APIs as tools
✅ **Parallel Processing** - Multiple agents work simultaneously
✅ **Synthesis** - Composer agent combines outputs intelligently

This meets the hackathon's "autonomous Agent behavior: planning, reasoning, execution" requirement!

## Model Configuration

### Sub-Agents (Parallel)
- **OpenAI:** `gpt-4o-mini` - 15¢/1M input, 60¢/1M output
- **Anthropic:** `claude-haiku-4-5` - $1/1M input, $5/1M output

### Composer Agent (Synthesis)
- **Anthropic:** `claude-sonnet-4-5` - $3/1M input, $15/1M output

### Why These Models?
- **Fast:** Near-instant responses
- **Cheap:** Conserves our hackathon credits
- **Smart:** Still very capable for creative generation
- **No thinking flags:** Standard chat completion, no extended reasoning

## Cost Per Game Generation

### Option 1: All OpenAI
~$0.0016 per game

### Option 2: All Anthropic
~$0.0225 per game

### Option 3: Mixed (Recommended)
~$0.0085 per game
- OpenAI for sub-agents (parallel, fast)
- Claude Sonnet for composer (quality synthesis)

With our $35 in OpenAI + Anthropic credits, we can generate:
- **21,875 games** (all OpenAI)
- **4,118 games** (mixed approach)
- **1,556 games** (all Anthropic)

## Next Steps

To integrate this into the Gradio app:
1. Import agents into `app.py`
2. Replace mock generation with real agent calls
3. Show streaming updates as agents complete
4. Display final GameDef JSON

Example integration:
```python
from agents import (
    CharacterAgent, MechanicAgent, StyleAgent,
    ConflictAgent, LevelAgent, TwistAgent, ComposerAgent
)

async def generate_game_real(mode, inputs):
    # Create agents
    agents = {...}

    # Run in parallel
    results = await asyncio.gather(...)

    # Compose
    composer = ComposerAgent()
    game_def = composer.compose(mode, results)

    return game_def
```

## Troubleshooting

### API Key Errors
Make sure `.env.local` has your keys:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Import Errors
Install dependencies:
```bash
pip install -r requirements.txt
```

### Rate Limit Errors
The models we're using have high rate limits, but if you hit them:
- Add small delays between calls
- Reduce parallel agent count
- Use free tier models during testing
