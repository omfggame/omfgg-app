# AI Model Reference for OMFGG

**Last Updated:** November 15, 2025

## Recommended Models for Development

For our hackathon project, we want to use **fast, affordable models** during development to save on credits.

### OpenAI Models (Best for Development)

#### GPT-4o mini - RECOMMENDED FOR SUB-AGENTS
- **Model ID:** `gpt-4o-mini`
- **Speed:** Fastest general-purpose model
- **Cost:** 15¢ per 1M input tokens, 60¢ per 1M output tokens (60% cheaper than GPT-4o)
- **Context:** 128K tokens
- **Best For:** Sub-agents running in parallel (Character, Mechanic, Style, etc.)
- **Strengths:** Balanced performance, multimodal (text + images), multilingual
- **Score:** 82% on MMLU benchmarks

#### GPT-4.1 nano - CHEAPEST OPTION
- **Model ID:** `gpt-4.1-nano`
- **Cost:** 10¢ per 1M input tokens (cheapest OpenAI model)
- **Best For:** Simple classification, intent detection, fast completions
- **Score:** 80.1% on MMLU

### Anthropic Models (Best for Quality)

#### Claude Haiku 4.5 - RECOMMENDED FOR SUB-AGENTS
- **Model ID:** `claude-haiku-4-5`
- **Speed:** Fastest Anthropic model (2-4x faster than Sonnet)
- **Cost:** $1 per 1M input tokens, $5 per 1M output tokens
- **Context:** 200K tokens
- **Best For:** Fast sub-agents, coding tasks, real-time responses
- **Strengths:** Near-frontier performance, matches Sonnet 4 on many tasks
- **Score:** 73.3% on SWE-bench Verified (one of world's best coding models)

#### Claude Sonnet 4.5 - RECOMMENDED FOR COMPOSER AGENT
- **Model ID:** `claude-sonnet-4-5-20250514`
- **Cost:** $3 per 1M input tokens, $15 per 1M output tokens
- **Context:** 200K tokens
- **Best For:** Composer Agent (synthesis, coherence, JSON validation)
- **Strengths:** Best overall intelligence, excellent at following structured output formats
- **Max Output:** 8,192 tokens

### What to AVOID During Development

❌ **Reasoning Models** (high cost, not needed):
- o1, o3, o4-mini (OpenAI)
- Claude with extended thinking flags

❌ **Large/Pro Models**:
- GPT-5, GPT-4.1 (full version)
- Claude Opus 4.1
- Any model with "pro" or "thinking" in the name

❌ **Thinking Flags**:
- Don't enable extended thinking
- Don't use reasoning modes
- Stick to standard chat completion endpoints

## Recommended Architecture for OMFGG

### Sub-Agents (Parallel Execution)
Use **GPT-4o mini** OR **Claude Haiku 4.5** for:
- Character Agent
- Mechanic Agent
- Style Agent
- Conflict Agent
- Level Agent
- Twist Agent

**Why:** These run in parallel, so cost adds up. Fast + cheap is critical.

### Composer Agent (Synthesis)
Use **Claude Sonnet 4.5** for:
- Collecting all sub-agent outputs
- Validating coherence
- Generating GameDef JSON
- Ensuring quality and structure

**Why:** This is a single call, runs once, needs high quality for JSON output.

## API Configuration

### OpenAI Setup
```python
import openai
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Example call
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Your prompt"}],
    temperature=0.8
)
```

### Anthropic Setup
```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Example call
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your prompt"}]
)
```

## Cost Estimates

### For 100 Game Generations:

#### Option 1: All GPT-4o mini
- 6 sub-agents × 500 tokens input × 100 games = 300K input tokens
- 6 sub-agents × 200 tokens output × 100 games = 120K output tokens
- 1 composer × 2K tokens input × 100 games = 200K input tokens
- 1 composer × 500 tokens output × 100 games = 50K output tokens
- **Total Cost:** ~$0.16 for 100 games

#### Option 2: Claude Haiku sub-agents + Sonnet composer
- 6 sub-agents × 500 tokens input × 100 games = $0.30
- 6 sub-agents × 200 tokens output × 100 games = $0.60
- 1 composer (Sonnet) × 2K tokens input × 100 games = $0.60
- 1 composer (Sonnet) × 500 tokens output × 100 games = $0.75
- **Total Cost:** ~$2.25 for 100 games

#### Option 3: Mixed (GPT-4o mini sub-agents + Claude Sonnet composer)
- **Total Cost:** ~$0.85 for 100 games
- **RECOMMENDED:** Best balance of cost and quality

## Available Hackathon Credits

From our sponsor stack:
- **OpenAI:** $25
- **Anthropic:** $10
- **HuggingFace:** $25
- **Modal:** $250 (compute)
- **Blaxel:** $250
- **ElevenLabs:** $44 (audio/TTS)
- **SambaNova:** $25
- **Nebius:** $50

**Strategy:** Use OpenAI and Anthropic credits wisely for development. Save Modal/Blaxel for deployment if needed.

## Knowledge Cutoff Dates

- **GPT-4o mini:** October 2023
- **GPT-4.1 series:** June 2024
- **Claude 4.x series:** May 2025 ✨ (Most recent!)
- **Claude 3.5 Haiku:** June 2024

## Additional Notes

- All models support streaming for better UX
- Both providers offer async APIs for parallel calls
- Use `temperature=0.8-0.9` for creative generation
- Use `temperature=0.1-0.3` for structured output (JSON)
