---
title: OMFGG - Our Mad-Lib Factory Generates Games
emoji: 🎮
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.49.0
app_file: app_with_agents.py
pinned: false
tags:
  - mcp-in-action
  - game-generator
  - gradio
  - hackathon
---

# OMFGG - Our Mad-Lib Factory Generates Games

A Mad-Lib style game generator that creates playable micro-games in seconds using AI agents.

**MCP's 1st Birthday Hackathon** | Track 2: MCP in Action | Nov 14-30, 2025

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/omfggame/omfgg-app.git
cd omfgg-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Add API keys
cp .env.local.example .env.local
# Edit .env.local with your OpenAI and Anthropic keys

# 3. Run the app
python app_with_agents.py
# Open http://localhost:7860
```

## Project Status

✅ AI agents integrated (OpenAI GPT-4o-mini, Anthropic Claude Sonnet 4.5)
✅ Parallel sub-agent execution (6 specialized agents)
✅ Persistent cache system
✅ Full logging and debugging

🚧 In Progress: Game renderer, MCP integration, deployment

## Documentation

See the `initial-development` branch for full documentation and code.

## Tech Stack

- **Frontend:** Gradio 5.49+ (mobile-friendly)
- **Backend:** Python 3.10+
- **AI:** OpenAI GPT-4o-mini, Anthropic Claude Sonnet 4.5
- **Deployment:** HuggingFace Spaces

## License

MIT

---

Built for MCP's 1st Birthday Hackathon 🎂
