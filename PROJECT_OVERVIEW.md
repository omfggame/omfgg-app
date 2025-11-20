# OMFGG Project Overview
**Our Mad-Lib Factory Generates Games**

*Last Updated: November 19, 2025*

---

## 🎯 What We're Building

A **Mad-Lib style AI game generator** that transforms simple user inputs (like "dancing pickle in Santa's workshop") into fully playable micro-games in seconds. Users fill in 5-8 playful blanks, and our AI agents create a unique, funny, shareable game experience.

**Think:** Infinite game generation meets improv comedy meets AI creativity.

---

## 🏆 Hackathon Context

**Event:** MCP's 1st Birthday Hackathon  
**Dates:** November 14-30, 2025 (17 days)  
**Track:** Track 2 - MCP in Action  
**Category:** Consumer MCP Servers  

**Requirements:**
- ✅ Gradio app hosted on HuggingFace Spaces
- ✅ Demonstrate MCP (Model Context Protocol) usage
- ✅ Show autonomous AI agent behavior (planning, reasoning, execution)
- ✅ Mobile-friendly UI
- 🚧 Game renderer (in progress)
- 🚧 MCP integration for storage (in progress)

**Prizes:** $2,500 (1st), $1,000 (2nd), $500 (3rd) + Community Choice Award

📖 **[Full hackathon details in hackathon_summary.md](hackathon_summary.md)**

---

## 🎮 Core Concept: Adaptive Mad-Libs

### Game Modes (5 Total)
Users first select a mode, which determines the input fields:

| Mode | Fields | Example Output |
|------|--------|---------------|
| **Relaxing** | Subject, Vibe, Setting, Wildcard | Zen garden meditation game |
| **Funny** | Subject, Action, Vibe, Setting, Twist | Dancing pickle dodges Santa's elves |
| **Chaotic** | Subject, Action, Obstacle, Chaos Modifier, Setting | Frantic robot avoids banana peels |
| **Challenge** | Subject, Goal, Obstacle, Setting, Twist | Hero collects coins while dodging fireballs |
| **Surprise Me** | Vibe only | AI generates everything else |

**Why this works:**
- Controlled creativity (not total chaos)
- Fast user input (5-30 seconds)
- Infinite variety within structure
- Personal and surprising results

📖 **[Detailed mechanics in hackathon_summary.md](hackathon_summary.md)**

---

## 🤖 AI Architecture: Multi-Agent System

### Parallel Sub-Agents (6 Specialized)
Each Mad-Lib field feeds a specialized AI agent that runs **in parallel**:

| Agent | Input | Output |
|-------|-------|--------|
| **Character Agent** | Subject | Traits, visual theme, personality |
| **Mechanic Agent** | Action/Goal | Interaction style, win condition |
| **Style Agent** | Vibe | Colors, mood, aesthetic |
| **Conflict Agent** | Obstacle | Challenge logic (or absence) |
| **Level Agent** | Setting | Background, environment, layout |
| **Twist Agent** | Wildcard/Twist | Special mechanics, power-ups |

### Composer Agent (Synthesis)
After sub-agents complete, the **Composer Agent**:
1. Collects all 6 outputs
2. Validates coherence
3. Constructs final `GameDef` JSON
4. Saves via MCP (future)
5. Generates shareable slug (e.g., `funny-pickle-4273`)

**Generation Speed:** 8-15 seconds (real agents) vs 5 seconds (mock)

📖 **[Full agent details in AGENT_DEMO.md](AGENT_DEMO.md)**  
📖 **[How to use agents in USING_REAL_AGENTS.md](USING_REAL_AGENTS.md)**

---

## 🧠 AI Models & Costs

### Current Configuration
- **Sub-agents:** OpenAI GPT-4o-mini ($0.15/1M tokens) *or* Anthropic Claude Haiku 4.5 ($1/1M tokens)
- **Composer:** Anthropic Claude Sonnet 4.5 ($3/1M tokens input)

### Cost Per Game
- **All OpenAI:** ~$0.0016/game
- **Mixed (recommended):** ~$0.0085/game
- **All Anthropic:** ~$0.0225/game

**With our $35 in credits:** Can generate 4,000+ games!

### Cache System (Development Feature)
Saves sub-agent results to disk between sessions:
- **First generation:** $0.0085
- **Regeneration (using cache):** $0.0013
- **Savings:** 85% cheaper when iterating!

📖 **[Model details in MODEL_REFERENCE.md](MODEL_REFERENCE.md)**  
📖 **[Cache system in CACHE_INFO.md](CACHE_INFO.md)**

---

## 🎨 Game Characteristics

Our micro-games aim to be:
- ⏱️ **Quick:** 5-30 seconds per playthrough
- 😂 **Funny:** Absurd, unexpected, chaotic
- 📱 **Mobile-first:** Vertical layout, touch-friendly
- 🔗 **Shareable:** Unique slugs, easy to remix
- ⚡ **Fast generation:** Seconds, not minutes
- 🎲 **Surprising:** "What did I just make?"

---

## 🏗️ Tech Stack

### Frontend
- **Gradio 5.49+** - Python UI framework with auto-deployment
- **Mobile-optimized** - Radio buttons, large touch targets, responsive layouts

### Backend
- **Python 3.10+**
- **asyncio** - Parallel agent execution
- **dotenv** - Environment variable management
- **Logging** - Full debug logs to `omfgg_app.log`

### AI APIs
- **OpenAI API** - Fast, affordable sub-agents
- **Anthropic API** - High-quality synthesis

### Deployment
- **HuggingFace Spaces** - Primary hosting (free tier: 2 vCPU, 16GB RAM)
- **GitHub Actions** - Auto-deployment on push to `main` or `dev`
- **Multi-environment:** Production (`omfgg`), Dev (`omfgg-dev`), Personal spaces

📖 **[Gradio docs in gradio_6_boilerplate.md and gradio_6_docs.md](gradio_6_boilerplate.md)**  
📖 **[Deployment setup in HUGGINGFACE_SETUP.md](HUGGINGFACE_SETUP.md)**

---

## 🚧 Current Status

### ✅ Complete
- [x] 6 specialized sub-agents + Composer Agent
- [x] Real API integration (OpenAI + Anthropic)
- [x] Parallel async execution
- [x] Cache system for development
- [x] Gradio UI with 5 game modes
- [x] Full logging and debugging
- [x] GitHub Actions auto-deploy setup
- [x] Multi-environment workflow (prod/dev)

### 🚧 In Progress
- [ ] Game renderer (decision pending)
- [ ] MCP integration for game storage
- [ ] Sprite/asset system
- [ ] Shareable URLs
- [ ] Demo video for hackathon
- [ ] Social media post

### 🤔 Decisions Needed

**Game Rendering Strategy:**
We've identified 4 options but haven't decided:

1. **HTML5 Canvas + Kenney sprites** (recommended, 8-10 hours)
2. **Phaser.js framework** (more features, 12-15 hours)
3. **Procedural/SVG generation** (lightweight, 3-4 hours)
4. **Hybrid approach** (best quality, most time)

📖 **[Full rendering options in GAME_RENDERING_PLAN.md](GAME_RENDERING_PLAN.md)**

**Game Mechanics Strategy:**
We're exploring compositional Mad-Lib mechanics instead of hardcoded game types:

- **Current:** 8 hardcoded game templates
- **Proposed:** 15 compositional categories = 438 trillion combinations
- **Micro-test:** Build 3 templates, validate approach (4-6 hours)

📖 **[Mechanics research in Game_Mechanics_Research.md](Game_Mechanics_Research.md)**

---

## 🔑 Key Files

### For New Agents/Sessions
- **THIS FILE** - Start here for overview
- **[hackathon_summary.md](hackathon_summary.md)** - Requirements, goals, Mad-Lib format
- **[README.md](README.md)** - Quick start, tech stack, license

### For AI Agent Development
- **[AGENT_DEMO.md](AGENT_DEMO.md)** - Agent architecture, demos, cost estimates
- **[USING_REAL_AGENTS.md](USING_REAL_AGENTS.md)** - How to run and test agents
- **[MODEL_REFERENCE.md](MODEL_REFERENCE.md)** - Model specs, costs, recommendations
- **`agents.py`** - Agent implementation code
- **`test_agents.py`** - Quick API verification tool

### For Game Development
- **[GAME_RENDERING_PLAN.md](GAME_RENDERING_PLAN.md)** - Rendering options, sprite sources
- **[Game_Mechanics_Research.md](Game_Mechanics_Research.md)** - Compositional mechanics research
- **[3Games_planning.md](3Games_planning.md)** - Game engine planning discussion

### For Gradio/UI Development
- **[gradio_6_boilerplate.md](gradio_6_boilerplate.md)** - Gradio tutorial and examples
- **[gradio_6_docs.md](gradio_6_docs.md)** - Comprehensive Gradio 6 reference
- **`app_with_agents.py`** - Main Gradio app with real agents
- **`mock-app.py`** - Original mock version (for testing)

### For Deployment
- **[HUGGINGFACE_SETUP.md](HUGGINGFACE_SETUP.md)** - Multi-environment setup guide
- **[CACHE_INFO.md](CACHE_INFO.md)** - Development cache system
- **`.github/workflows/`** - Auto-deployment workflows

### Templates
- **`templates/`** - HTML game templates (8 types)

---

## 🚀 Quick Start

### First Time Setup (10 minutes)
```bash
# 1. Clone repository
git clone https://github.com/omfggame/omfgg-app.git
cd omfgg-app

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API keys
cp .env.local.example .env.local
# Edit .env.local with your keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# 5. Run the app
python app_with_agents.py

# 6. Open browser
# http://localhost:7860
```

### Testing the Agents (2 minutes)
```bash
# Quick API verification
python test_agents.py

# Full demo (all 5 demonstrations)
python agents.py
```

### Development Workflow
```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/your-feature

# Make changes, test locally
python app_with_agents.py

# Push and create PR to dev
git push origin feature/your-feature
# Create PR on GitHub: dev ← feature/your-feature

# After merge, auto-deploys to:
# https://huggingface.co/spaces/therawr/omfgg-dev

# When stable, merge dev → main for production:
# https://huggingface.co/spaces/therawr/omfgg
```

---

## 💡 Project Philosophy

### "What Did I Just Make?"
Our goal is to create that delightful moment of surprise when users see their absurd inputs transformed into an actual game. The experience should feel:

- **Personal** - Their words, their creation
- **Unpredictable** - AI adds creative twists
- **Shareable** - "Look at this ridiculous thing!"
- **Instant** - No waiting, no setup
- **Replayable** - Generate infinite variations

### Why This Works for Hackathons
1. **Scoped creativity** - Mad-Libs constrain input without limiting fun
2. **Parallel agents** - Fast generation (hackathon judges love speed)
3. **MCP integration** - Modular, extensible architecture
4. **Demonstrable AI** - Clear agent roles and outputs
5. **Mobile-first** - Works on any device
6. **Viral potential** - Funny results = social sharing

---

## 🎯 Next Critical Steps

### Immediate (This Week)
1. **Decide rendering strategy** - Review GAME_RENDERING_PLAN.md as team
2. **Build minimal renderer** - Get 1 game type playable (8-10 hours)
3. **Add MCP storage** - Simple filesystem or Supabase (2 hours)
4. **Deploy dev Space** - Test full pipeline on HuggingFace (1 hour)

### Before Submission (Nov 30)
1. **Polish 3 game types** - Ensure quality and variety
2. **Record demo video** - 1-5 minutes showing full flow
3. **Write social post** - Share project, tag hackathon
4. **Update README** - Add demo video, post link, track tag
5. **Deploy production** - Final stable version

### Stretch Goals
- [ ] Audio/TTS with ElevenLabs credits ($44 available)
- [ ] More game mechanics (expand beyond 3 types)
- [ ] Community voting/rating system
- [ ] Export games as standalone HTML

---

## 📊 Available Resources

### Hackathon Credits
- **OpenAI:** $25
- **Anthropic:** $10  
- **HuggingFace:** $25  
- **Modal:** $250 (compute/deployment)
- **Blaxel:** $250  
- **ElevenLabs:** $44 (audio/TTS)  
- **SambaNova:** $25  
- **Nebius:** $50  

### Team Tools
- **Cursor/Vibe coding** - Allowed and encouraged
- **Existing libraries** - Use anything
- **Parallel workflows** - Perfect for our multi-agent system

---

## 🤝 Team Workflow

### Branches
- **`main`** - Production (auto-deploys to `omfgg` Space)
- **`dev`** - Staging (auto-deploys to `omfgg-dev` Space)
- **`feature/*`** - Individual features (PR to `dev`)

### Spaces
- **Production:** https://huggingface.co/spaces/therawr/omfgg
- **Dev/Staging:** https://huggingface.co/spaces/therawr/omfgg-dev
- **Personal:** (optional) Create your own Space for isolated testing

### Code Review Flow
```
Developer → Feature Branch → PR to Dev → Team Review
  → Merge to Dev → Auto-deploy to Dev Space → Team Test
  → PR to Main → Final Review → Merge to Main
  → Auto-deploy to Production → Demo Ready!
```

📖 **[Full team setup in HUGGINGFACE_SETUP.md](HUGGINGFACE_SETUP.md)**

---

## 🐛 Common Issues & Solutions

### "No API key found"
- Check `.env.local` exists and has valid keys
- Keys should start with `sk-` (OpenAI) or `sk-ant-` (Anthropic)

### "Module not found: agents"
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### "Build failed on HuggingFace"
- Verify README.md has frontmatter with `sdk: gradio`
- Check `requirements.txt` has all dependencies
- View GitHub Actions logs for specific error

### "No cached results available"
- Generate a game first (cache is populated after first generation)
- Cache saves to `cache/latest_cache.json`

### App doesn't update after merge
- Check GitHub Actions - did workflow run?
- Verify you merged to correct branch (`dev` → `omfgg-dev`, `main` → `omfgg`)
- Try "Factory Rebuild" in HuggingFace Space settings

📖 **[Full troubleshooting in HUGGINGFACE_SETUP.md](HUGGINGFACE_SETUP.md)**

---

## 🎬 Demo Script (For Hackathon Video)

**Opening (15 seconds):**
"Ever wondered what happens when you mash random words into an AI game generator? Watch this..."

**Demo Flow (2-3 minutes):**
1. Show Mad-Lib interface: "Let's make a Funny game"
2. Fill in: "dancing pickle" + "Santa's workshop" + "nervous" + "Easter"
3. Click Generate → Show parallel agents launching
4. Watch GameDef JSON generate
5. Play the resulting game
6. Show shareable slug
7. Regenerate to show variety

**Technical Highlight (30 seconds):**
- Show 6 sub-agents running in parallel
- Highlight MCP integration (future)
- Mention cost efficiency (cache system)

**Closing (15 seconds):**
"Infinite games, instant generation, powered by AI agents. Check out the code on GitHub!"

---

## 📈 Success Metrics

### For Hackathon Judging
- **Novelty:** Unique Mad-Lib approach to game generation
- **Technical:** 6 parallel agents + async execution + MCP integration
- **Completeness:** Full pipeline from input → GameDef → playable game
- **Polish:** Mobile-friendly UI, clear UX, funny results
- **Demonstration:** Video shows real-time generation

### For Community Choice
- **Shareability:** Funny, unexpected results
- **Accessibility:** Works on any device
- **Engagement:** Try multiple times to see variety
- **Virality:** "Look what I made!"

---

## 📚 Additional Resources

- **Gradio Docs:** https://gradio.app/docs
- **HuggingFace Spaces:** https://huggingface.co/spaces
- **OpenAI API:** https://platform.openai.com/docs
- **Anthropic API:** https://docs.anthropic.com
- **MCP Protocol:** https://modelcontextprotocol.io
- **Hackathon Page:** https://devpost.com/hackathons/mcp-birthday

---

## 🙋 Questions? Start Here:

1. **"What is this project?"** → Read this file (you're here!)
2. **"How do I run it?"** → See [Quick Start](#quick-start) above
3. **"How do the AI agents work?"** → Read [AGENT_DEMO.md](AGENT_DEMO.md)
4. **"How do I deploy?"** → Read [HUGGINGFACE_SETUP.md](HUGGINGFACE_SETUP.md)
5. **"What game mechanics do we use?"** → Read [GAME_RENDERING_PLAN.md](GAME_RENDERING_PLAN.md)
6. **"How much will this cost?"** → Read [MODEL_REFERENCE.md](MODEL_REFERENCE.md)
7. **"What's left to build?"** → See [Current Status](#-current-status) above

---

## 🎮 Let's Build Some Games!

This is a hackathon project built in 17 days by a team passionate about AI, games, and ridiculous ideas. We're making something that's never been built before, and having fun doing it.

**Ready to contribute?** Pick a task from [Next Critical Steps](#-next-critical-steps) and let's go!

---

*Built for MCP's 1st Birthday Hackathon 🎂*  
*November 14-30, 2025*

