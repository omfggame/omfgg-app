# OMFGG Project Instructions for Claude Code

## Project Context

This is OMFGG (Our Mad-Lib Factory Generates Games) - a hackathon project for MCP's 1st Birthday Hackathon (Nov 14-30, 2025). We're building an AI-powered game generator using Gradio, with parallel sub-agents creating micro-games from user Mad-Lib inputs.

**Track:** Track 2 - MCP in Action
**Category:** Consumer MCP Servers
**Tech Stack:** Python, Gradio, OpenAI API, Anthropic API

## Sub-Agent Usage for Context Conservation

**IMPORTANT:** To conserve context in the main conversation, use the Task tool with sub-agents for research and data collection tasks.

### When to Use Sub-Agents

Use sub-agents for:
- **Web searches** (Perplexity MCP)
- **Documentation research** (fetching docs, API references)
- **Code exploration** (finding files, searching patterns)
- **External data gathering** (web fetches, API calls)

### How to Use Sub-Agents

Instead of directly using tools that consume main context, delegate to sub-agents using the Task tool.

**Example: Research with Perplexity MCP**

When the user asks to research something, use a sub-agent:

```
Task tool with:
- subagent_type: "general-purpose"
- description: "Research latest Gradio features"
- prompt: "Use the perplexity MCP search tool to find the latest Gradio 5.x features and best practices for async event handlers. Return a concise summary (300 words max) of:
  1. Latest async patterns
  2. State management recommendations
  3. Performance tips

  Focus on actionable information we can use in our project."
- model: "sonnet"
```

**Why This Helps:**
- Sub-agent uses its own context window for research
- Main conversation only receives the summary (300 words vs. thousands of tokens)
- Keeps main chat focused on implementation
- Saves context for actual coding work

### Good Sub-Agent Practices

1. **Be specific in prompts** - Tell the sub-agent exactly what to research and what format to return
2. **Request summaries** - Ask for "concise summary" or "top 5 takeaways"
3. **Filter information** - Request only actionable items relevant to our project
4. **Use appropriate models** - Haiku for simple tasks, Sonnet for complex research

### Examples of Tasks for Sub-Agents

**Web Research:**
- "Find latest MCP server implementations"
- "Research Gradio deployment options on HuggingFace Spaces"
- "Look up best practices for async LLM calls in Python"

**Documentation:**
- "Fetch OpenAI API docs for async chat completions"
- "Get Anthropic Claude API pricing information"
- "Find Gradio State management documentation"

**Code Exploration:**
- "Search our codebase for all agent definitions"
- "Find examples of async functions in the project"
- "Locate all Gradio event handlers"

## File Organization

```
omfgg/
├── .claude/
│   └── CLAUDE.md          # This file
├── .env.local             # API keys (DO NOT COMMIT)
├── .gitignore
├── agents.py              # Sub-agent implementations
├── app.py                 # Original mock Gradio app
├── app_with_agents.py     # Real LLM-powered Gradio app
├── test_agents.py         # API verification
├── requirements.txt
├── README.md
├── MODEL_REFERENCE.md     # AI model guide
├── AGENT_DEMO.md          # Demo instructions
├── hackathon_summary.md   # Hackathon requirements
├── next_steps.md          # Progress tracker
└── TODO.md                # Implementation roadmap
```

## Development Guidelines

### Game Scope Constraints ⚠️
**IMPORTANT:** Keep game designs simple and feasible for rapid development.

**IN SCOPE:**
- Single core mechanic (tap, swipe, hold, drag)
- 5-30 second micro-games
- Simple visual effects and modifiers
- Single-screen, instant-play mobile games
- Basic scoring or win/lose conditions

**OUT OF SCOPE:**
- Mini-games within games
- Complex multi-stage interactions
- Elaborate progression systems
- Multiple game modes per game
- Complex physics simulations
- Multiplayer features

**Priority:** Speed of development > Feature richness
**Goal:** Demonstrate multi-agent system, not build AAA games

### API Key Management
- API keys in `.env.local` (gitignored)
- Use `python-dotenv` to load
- Never commit keys to git

### Model Selection
- **Sub-agents:** GPT-4o mini (OpenAI) or Claude Haiku 4.5 (Anthropic)
- **Composer:** Claude Sonnet 4.5 (Anthropic)
- **Avoid:** Reasoning models (o1, o3, extended thinking) during development
- **Model IDs:**
  - OpenAI: `gpt-4o-mini`
  - Anthropic Haiku: `claude-3-5-haiku-20241022`
  - Anthropic Sonnet: `claude-sonnet-4-5-20250929`
  - ⚠️ DO NOT use Claude 3.5 or 3.7 Sonnet

### Cost Optimization
1. Cache sub-agent results (implemented in `app_with_agents.py`)
2. Use faster/cheaper models for parallel agents
3. Use better models only for synthesis (Composer)
4. Implement regenerate feature to iterate without re-calling sub-agents

### Testing
- `python test_agents.py` - Quick API verification
- `python agents.py` - Full agent demos
- `python app_with_agents.py` - Gradio app with real agents

## Hackathon Requirements Checklist

- [x] Gradio app as frontend
- [x] Demonstrate agentic behavior (6 specialized sub-agents)
- [x] Parallel agent execution
- [ ] MCP integration (for game storage/retrieval)
- [ ] Demo video (1-5 minutes)
- [ ] Social media post
- [ ] HuggingFace Space deployment
- [ ] Complete README with track tag

## Important Dates

- **Hackathon:** November 14-30, 2025
- **Submission Deadline:** November 30, 2025
- **Development Status:** In progress (started Nov 15)

## Contact & Links

- **GitHub:** https://github.com/joerawr
- **Hackathon:** https://huggingface.co/MCP-1st-Birthday
- **Track:** Track 2 - MCP in Action

## Notes

- This is original work created during the hackathon window
- We retain IP rights
- Project will be open source
- Focus on demonstrating autonomous agent behavior and MCP integration
