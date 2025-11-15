# Game Rendering & Sprite Strategy - Team Discussion Doc

**Created:** Nov 15, 2025
**Status:** Needs team decision before implementation

## Current State

### ✅ What's Working

```
User Mad-Lib Input
  ↓
5 Sub-Agents (parallel) → Character, Mechanics, Style, Environment, Twist
  ↓
Composer Agent (Claude 4.5 Sonnet) → GameDef JSON
  ↓
Cache to disk (cache/latest_cache.json)
  ↓
❌ NO RENDERER YET
```

**Example GameDef Generated:**
- Title: "Pickle Pete's Dance Party"
- Mechanics: Tap rhythm game, 15 seconds
- Character: Pickle with googly eyes and top hat
- Style: Flat design, vibrant colors
- Special: Bunny boost (2x points for 3 seconds)

### ❌ What's Missing

1. **Game Renderer** - We generate JSON specs but can't actually play the games
2. **Sprite/Asset System** - No visuals, just text descriptions
3. **MCP Integration** - Not storing/retrieving games yet
4. **Shareable URLs** - No way to share generated games

## Sprite Research (Perplexity MCP Search)

### Fastest Options for Hackathon

#### 1. Kenney.nl ⭐ TOP RECOMMENDATION
- **License:** CC0/Public Domain (use anywhere, no attribution)
- **Speed:** 2-5 minutes to get complete themed pack
- **Variety:** Thousands of assets across all genres
- **Format:** Pre-organized game kits with matching styles
- **URL:** https://kenney.nl

**Why best for us:**
- Complete themed sets eliminate art style mismatches
- Zero licensing concerns
- Fastest acquisition time
- Professional quality

#### 2. itch.io (Free filter)
- **License:** Mixed (CC0, CC-BY, custom - check per pack)
- **Speed:** 5-10 minutes browsing and download
- **Variety:** 5,400+ free sprite packs, excellent filtering
- **Format:** Individual packs, varying quality
- **URL:** https://itch.io/game-assets/free

**Why good for us:**
- Huge variety for different game themes
- Good backup/supplement to Kenney
- Community-driven with unique styles

#### 3. OpenGameArt.org
- **License:** Mostly CC0/CC-BY (requires attribution)
- **Speed:** 10-30 minutes (more searching required)
- **Variety:** Massive library, most diverse styles
- **Format:** Individual assets, quality varies
- **URL:** https://opengameart.org

**Why use as backup:**
- Best for finding specific assets Kenney doesn't have
- High quality community contributions
- More time-consuming to search

### AI Sprite Generators - NOT RECOMMENDED

Research found that current AI tools (Midjourney, DALL-E, Stable Diffusion) are **not good for game sprites** because:
- ❌ Inconsistent across sprite sheets
- ❌ Poor transparent background handling
- ❌ Can't generate matching animation frames
- ❌ Slower than downloading pre-made packs

**Conclusion:** Pre-made asset libraries are faster for hackathon timeline.

## Game Rendering Options

### Option 1: HTML5 Canvas (Pure JavaScript)

**Pros:**
- Lightweight, no dependencies
- Full control over rendering
- Fast load times
- Easy to embed in Gradio iframe

**Cons:**
- Need to implement game loop, collision, input handling from scratch
- More code to write
- No built-in physics

**Use Case:** Simple tap/click games with minimal physics

**Estimated Implementation Time:** 4-6 hours for basic renderer

---

### Option 2: Phaser.js Framework

**Pros:**
- Full game engine with physics, collision, animations built-in
- Huge community and examples
- Great for rapid prototyping
- Handles sprite sheets, audio, particle effects

**Cons:**
- Learning curve (~2-3 hours to get comfortable)
- Heavier bundle size (~1MB minified)
- Might be overkill for 15-second micro-games

**Use Case:** Games needing physics, complex animations, or particle effects

**Estimated Implementation Time:** 6-8 hours (includes learning curve)

---

### Option 3: Procedural/SVG-Based Generation

**Pros:**
- No sprite files needed
- Generated on-the-fly from GameDef
- Very lightweight
- Infinitely scalable graphics

**Cons:**
- Limited visual variety (geometric shapes mostly)
- Looks basic/abstract
- Harder to make "cute" characters

**Use Case:** Abstract/minimal style games, geometric puzzles

**Estimated Implementation Time:** 3-4 hours for basic system

---

### Option 4: Hybrid (Kenney Sprites + HTML5 Canvas) ⭐ RECOMMENDED

**Pros:**
- Fast asset acquisition (Kenney packs)
- Simple custom renderer
- Good visual quality
- Full control, lightweight
- Can hard-code sprite mappings

**Cons:**
- Still need to build game loop, collision, input
- Limited to sprites we've downloaded
- Some manual sprite mapping work

**Use Case:** Our exact use case - simple micro-games with nice visuals

**Estimated Implementation Time:** 5-7 hours total
- 1 hour: Download and organize Kenney packs
- 2 hours: Build sprite mapping system (GameDef → sprite files)
- 2-3 hours: Build Canvas renderer with game loop
- 1 hour: Test and polish

---

## Proposed Architecture

### Full Game Creation Flow

```
1. User fills Mad-Lib
   ↓
2. 5 Sub-Agents generate specs (parallel)
   ↓
3. Composer synthesizes → GameDef JSON
   ↓
4. GameDef stored via MCP (slug: "pickle-pete-dance-party")
   ↓
5. Sprite Mapper: GameDef → Select sprites from Kenney pack
   ↓
6. Renderer: GameDef + Sprites → HTML5 Canvas game
   ↓
7. Game embedded in Gradio UI (iframe)
   ↓
8. Shareable URL: /play/pickle-pete-dance-party
```

### Rendering Choices to Decide

1. **Where to render the game?**
   - **Option A:** In Gradio app directly (gr.HTML with Canvas iframe)
   - **Option B:** Separate web page, Gradio links to it
   - **Option C:** Export standalone HTML file user can download

2. **Sprite strategy?**
   - **Option A:** Download 5-10 Kenney packs now, hard-code mappings
   - **Option B:** Download massive collection, dynamic selection
   - **Option C:** Procedural generation (no sprites)
   - **Option D:** Hybrid (Kenney base + procedural fallback)

3. **Renderer complexity?**
   - **Option A:** Minimal (just display sprites, basic tap interaction)
   - **Option B:** Medium (add simple physics, scoring, effects)
   - **Option C:** Full (particle effects, animations, complex mechanics)

## Team Discussion Questions

### Priority & Scope
1. **How much time can we allocate to building the renderer?**
   - Quick demo (3-4 hours): Minimal renderer, procedural graphics
   - Medium effort (6-8 hours): Canvas + Kenney sprites, basic mechanics
   - Full implementation (12+ hours): Phaser.js, complex mechanics, polish

2. **What's the minimum viable game experience for the demo?**
   - Just show static sprites with game description?
   - Simple tap interaction (score counter)?
   - Full playable game with win/lose conditions?

### Technical Decisions
3. **Rendering approach preference?**
   - Pure HTML5 Canvas (lightweight, custom)
   - Phaser.js (feature-rich, heavier)
   - Hybrid approach?

4. **Sprite strategy?**
   - Use Kenney.nl packs (recommended, ~1 hour to set up)
   - Search multiple sources per game (slower, more variety)
   - Procedural/generated graphics (faster, looks basic)

5. **Where should games be hosted/rendered?**
   - Embedded in Gradio UI
   - Separate static web page
   - Exported HTML files

### MCP Integration
6. **What MCP server should we use for storage?**
   - Supabase (requires setup)
   - Local filesystem (simpler for demo)
   - Other MCP server?

7. **Do we need shareable URLs for the demo?**
   - Yes, critical feature
   - Nice to have
   - Can skip for hackathon

## Recommendations (Based on Research)

### For Fastest Hackathon Demo:

**Sprite Strategy:**
1. Download 3-5 Kenney game kit packs NOW (30 minutes)
   - Platformer pack (characters, items)
   - UI pack (buttons, effects)
   - Casual pack (cute characters)
   - Space pack (for variety)
2. Create simple sprite mapping: GameDef theme → Kenney pack folder
3. Use fallback sprites for unmapped themes

**Renderer Strategy:**
1. Build simple HTML5 Canvas renderer (4-5 hours)
2. Support 2-3 core mechanics only:
   - Tap/click scoring
   - Simple timer
   - Win/lose conditions
3. Embed in Gradio using gr.HTML component

**MCP Strategy:**
1. Start with filesystem storage (1 hour setup)
2. Generate slugs from GameDef titles
3. Upgrade to proper MCP server if time permits

**Total Estimated Time:** 8-10 hours for minimal playable demo

### For More Polished Demo:

Use Phaser.js + Kenney sprites (12-15 hours total)
- Better animations, physics, effects
- Professional feel
- Reusable for future games

## Next Steps (After Team Decision)

### If going with Recommended Approach:

1. **Download Sprites** (30 min - 1 hour)
   - [ ] Download 3-5 Kenney game kits
   - [ ] Organize in `assets/sprites/` directory
   - [ ] Document sprite pack contents

2. **Build Sprite Mapper** (2 hours)
   - [ ] Define GameDef → sprite mapping logic
   - [ ] Create sprite selection function
   - [ ] Add fallback sprites for unknown themes

3. **Build Canvas Renderer** (3-4 hours)
   - [ ] Create game loop (update/render)
   - [ ] Implement tap/click input handling
   - [ ] Add sprite rendering
   - [ ] Implement timer and scoring
   - [ ] Add win/lose conditions

4. **Integrate with Gradio** (1 hour)
   - [ ] Add gr.HTML component for game display
   - [ ] Pass GameDef to renderer
   - [ ] Test in Gradio UI

5. **MCP Storage** (2 hours)
   - [ ] Set up filesystem MCP or Supabase
   - [ ] Implement save/load GameDef
   - [ ] Generate shareable slugs
   - [ ] Test retrieval

6. **Test & Polish** (2 hours)
   - [ ] Test all 5 game modes
   - [ ] Mobile testing
   - [ ] Bug fixes
   - [ ] Visual polish

**Total:** ~12-15 hours for complete working demo

## Resources & Links

- **Kenney.nl:** https://kenney.nl
- **itch.io Free Assets:** https://itch.io/game-assets/free
- **OpenGameArt:** https://opengameart.org
- **Phaser.js:** https://phaser.io
- **HTML5 Canvas Tutorial:** https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial

## Hosting Decision ✅

**Platform:** HuggingFace Spaces (Required for hackathon submission)

**Why:**
- Native Gradio support (literally built for it)
- Free tier: 2 vCPU, 16GB RAM, unlimited public apps
- $25 credit from hackathon sponsors (bonus on top of free tier)
- Deployment: `git push` (no Docker, no config)
- Mobile-friendly out of the box
- Required for hackathon anyway

**Alternatives considered:**
- ❌ Vercel - No Python/Gradio support without Docker
- Modal ($250 credit) - Backup if need heavy GPU compute
- Blaxel ($250 credit) - Not ideal for web hosting
- Nebius ($50 credit) - Insufficient documentation

## Decision Tracking

| Decision | Options | Team Choice | Date |
|----------|---------|-------------|------|
| **Hosting Platform** | **HuggingFace / Modal / Vercel** | **✅ HuggingFace Spaces** | **Nov 15** |
| Renderer | Canvas / Phaser / Procedural / Hybrid | _TBD_ | |
| Sprites | Kenney / itch.io / Procedural | _TBD_ | |
| Game Display | Gradio embed / Separate page / Export | _TBD_ | |
| MCP Server | Supabase / Filesystem / Other | _TBD_ | |
| Scope | Minimal / Medium / Full | _TBD_ | |
| Timeline | 3-4h / 6-8h / 12-15h / 20+ | _TBD_ | |

---

**Ready for team discussion!**
