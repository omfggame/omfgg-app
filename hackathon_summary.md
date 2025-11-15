# Project Summary: Mad-Lib Generated Micro-Games (AI Hackathon Version)

## 🕹️ Overview
We’re building a **Mad-Lib–style game generator** where the user fills in a few playful blanks, and our AI turns those words into a fully playable micro‑game in seconds. The experience should be funny, surprising, and instantly shareable.

This approach supports rapid creativity, a controlled input schema, and parallel AI generation — perfect for an AI Hackathon.

Working Title OMFGG
Which we will be vague about what it stands for, and randomize it.  Examples:

Our Mad-Lib Factory Generates Games
One Mistyped Form: Great Game!
Obliviously Mashing Fields: Good Game
Overloaded Machine Forming Goofy Games

---

## 🎯 AI Hackathon Requirements (Track 2: MCP in Action)

**Event:** MCP's 1st Birthday Hackathon
**Dates:** November 14-30, 2025 (17 days)
**Track:** Track 2 - MCP in Action
**Category:** Consumer MCP Servers (best fit for our game generator)

### Must-Haves for Submission
- Build a **Gradio app** hosted as a HuggingFace Space
- Demonstrate **MCP (Model Context Protocol)** usage
- Show **autonomous Agent behavior**: planning, reasoning, execution
- Must be **original work** created during Nov 14-30, 2025
- **Required deliverables:**
  - HuggingFace Space with appropriate track tag in README
  - 1-5 minute demo video showing the app in action
  - Social media post about the project (link included in README)
  - Complete documentation in README
- Mobile-friendly UI is strongly encouraged

### Prize Structure (Track 2)
- **1st Place (per category):** $2,500 USD
- **2nd Place:** $1,000 USD
- **3rd Place:** $500 USD
- **Community Choice Award:** $1,000 USD (based on engagement)
- **Sponsor Choice Awards:** Various
- **API Credits:** See below

### Available Sponsor Credits
Our complete credit stack:
- **OpenAI:** $25
- **Anthropic:** $10
- **HuggingFace:** $25
- **Modal:** $250 (compute/deployment)
- **Blaxel:** $250
- **ElevenLabs Creator:** $44 (audio/TTS)
- **SambaNova:** $25
- **Nebius Token Factory:** $50

### Allowed Tools & Resources
- Vibe coding tools (Bolt, Lovable, Cursor) are permitted
- Existing libraries and frameworks allowed
- Core contributions must be original
- Parallel agent workflows encouraged (perfect for our use case!)
- Multimodal features encouraged

---

## 🧩 How We Define & Generate the Game

### 1. **Adaptive Mad-Lib Blueprint**
The user first selects a **game mode**, which determines the field set:

**Game Modes:**
- **Relaxing** - Calm, meditative experiences
- **Funny** - Absurd, humorous scenarios
- **Chaotic** - Fast-paced, wild gameplay
- **Challenge** - Goal-oriented with obstacles
- **Surprise Me** - AI picks everything with minimal input

Based on the mode, the user fills in 5–8 adaptive fields:

#### Mode: Relaxing
- Subject (what you interact with)
- Vibe (calm/zen/cozy)
- Setting (peaceful location)
- Wildcard (gentle mechanic)

#### Mode: Funny
- Subject (silly character/thing)
- Action (absurd verb)
- Vibe (comedic tone)
- Setting (weird location)
- Twist (unexpected element)

#### Mode: Chaotic
- Subject (fast-moving character)
- Action (frantic verb)
- Obstacle (hazard/challenge)
- Chaos Modifier (randomness)
- Setting (dynamic location)

#### Mode: Challenge
- Subject (player character)
- Goal (win condition)
- Obstacle (challenge/antagonist)
- Setting (game arena)
- Twist (power-up/mechanic)

#### Mode: Surprise Me
- Vibe (just one input)
- *Everything else auto-generated*

These structured inputs constrain creativity while maximizing fun and personalization.

---

### 2. **Parallel Sub-Agents**
Each field feeds a specialized agent (agents adapt based on mode):

| Field | Sub-Agent | Output |
|-------|-----------|--------|
| Subject | Character-Agent | Traits, sprite/theme, or abstract element |
| Action/Goal | Mechanic-Agent | Interaction style, win condition (if any) |
| Vibe | Style-Agent | Colors, mood, tone, aesthetic |
| Obstacle | Conflict-Agent | Challenge logic (or absence of conflict) |
| Setting | Level-Agent | Background, layout, environment |
| Wildcard/Twist/Chaos | Twist-Agent | Special mechanics, power-ups, randomness |

Agents run **in parallel** for speed and incorporate mode-specific instructions.

---

### 3. **Composer Agent**
The Composer Agent:
- Collects all sub-agent outputs
- Validates coherence
- Constructs the final `GameDef` JSON
- Saves it via MCP (e.g., Supabase)
- Returns a **shareable slug**
- Triggers the playable micro‑game in Gradio

---

## 📱 Game Characteristics
We aim for micro-games that are:
- Quick to play (5–30 seconds)
- Funny and chaotic
- Mobile-first, vertical layout
- Shareable and remixable
- Generated in a few seconds
- Simple but surprising

---

## 💥 Why This Works
- Mad Libs create controlled randomness
- Sub-agents allow parallel creativity
- MCP makes tool integration modular
- The system is fast enough for live demoing
- Results feel personal and chaotic in a good way

---

## 🚀 Goal
Deliver a **“What Did I Just Make?”** experience:

> Fill in a few words → AI generates a ridiculous micro‑game → Share with friends.