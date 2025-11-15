# HuggingFace Spaces Team Setup Guide

**Project:** OMFGG (Our Mad-Lib Factory Generates Games)
**Platform:** HuggingFace Spaces with GitHub Auto-Deploy
**Team Size:** 2-4 developers

---

## Overview

This setup provides Vercel-style auto-deployments for our Gradio app:
- Developers work in GitHub
- Push to `main` → Auto-deploys to HuggingFace Spaces
- Live at `https://huggingface.co/spaces/[username]/omfgg`

---

# Multi-Environment Strategy

**For team development, we'll use multiple HuggingFace Spaces:**

| Space | Branch | URL | Purpose |
|-------|--------|-----|---------|
| `omfgg` | `main` | `huggingface.co/spaces/[user]/omfgg` | **Production** - Stable, demo-ready |
| `omfgg-dev` | `dev` | `huggingface.co/spaces/[user]/omfgg-dev` | **Staging** - Team integration testing |
| `omfgg-[yourname]` | `yourname/dev` | Personal Space (optional) | **Personal** - Individual testing |

**Why this approach?**
- Each developer can test changes before merging to `dev`
- `dev` branch is shared staging environment
- `main` branch is production (for demo/hackathon submission)
- No conflicts, everyone can work independently

---

# Part 1: Initial Setup (One Person Does This)

**Time:** 30-40 minutes (creating 2 Spaces)
**Who:** Project lead or whoever creates the HuggingFace Spaces

## Step 1: Create HuggingFace Account & Spaces

1. **Sign up at HuggingFace** (if you don't have an account)
   - Go to https://huggingface.co
   - Click "Sign Up" (free account)
   - Verify email

2. **Create PRODUCTION Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Fill in details:
     - **Name:** `omfgg`
     - **License:** MIT
     - **Space SDK:** Select **Gradio**
     - **Visibility:** Public (required for hackathon)
     - **Hardware:** Free CPU (2 vCPU, 16GB RAM)
   - Click "Create Space"

3. **Create DEV/STAGING Space**
   - Click "Create new Space" again
   - Fill in details:
     - **Name:** `omfgg-dev`
     - **License:** MIT
     - **Space SDK:** Select **Gradio**
     - **Visibility:** Public (or Private for internal testing)
     - **Hardware:** Free CPU
   - Click "Create Space"

4. **Note your Space URLs**
   - Production: `https://huggingface.co/spaces/[username]/omfgg`
   - Dev/Staging: `https://huggingface.co/spaces/[username]/omfgg-dev`
   - Save these for later

## Step 2: Prepare GitHub Repository

1. **Add README.md frontmatter** (CRITICAL!)

   Add this to the **very top** of your `README.md`:
   ```markdown
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
   ---

   # OMFGG - Our Mad-Lib Factory Generates Games
   [Rest of your README...]
   ```

2. **Verify required files exist:**
   - ✅ `app_with_agents.py` (or rename your main file)
   - ✅ `requirements.txt`
   - ✅ `README.md` (with frontmatter above)
   - ✅ `.gitignore` (includes `.env`, `.env.local`)

3. **Update requirements.txt** (if needed)
   ```
   gradio==5.49.0
   openai
   anthropic
   python-dotenv
   ```

4. **Commit and push changes**
   ```bash
   git add README.md requirements.txt
   git commit -m "Add HuggingFace Space configuration"
   git push origin main
   ```

## Step 3: Create HuggingFace Write Token

1. **Generate token**
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Settings:
     - **Name:** `github-actions-deploy`
     - **Type:** Fine-grained token
     - **Permissions:**
       - ✅ Write access to repos
       - Repository: Select your Space (`[username]/omfgg`)
   - Click "Generate token"

2. **Copy token value**
   - Copy the `hf_...` token immediately (won't be shown again)
   - Save it temporarily (you'll add it to GitHub next)

## Step 4: Add GitHub Actions for Multi-Environment Deploy

1. **Create workflow directory**
   ```bash
   mkdir -p .github/workflows
   ```

2. **Create PRODUCTION deployment workflow**

   Create `.github/workflows/deploy-production.yml`:
   ```yaml
   name: Deploy to Production (HuggingFace)

   on:
     push:
       branches: [main]
     workflow_dispatch:

   jobs:
     deploy-production:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v3
           with:
             fetch-depth: 0
             lfs: true

         - name: Push to HuggingFace Production Space
           uses: nateraw/huggingface-sync-action@v0.0.4
           with:
             github_repo_id: joerawr/omfgg  # CHANGE THIS
             huggingface_repo_id: YOUR_HF_USERNAME/omfgg  # CHANGE THIS
             repo_type: space
             space_sdk: gradio
             hf_token: ${{ secrets.HF_TOKEN }}
   ```

3. **Create DEV/STAGING deployment workflow**

   Create `.github/workflows/deploy-dev.yml`:
   ```yaml
   name: Deploy to Dev/Staging (HuggingFace)

   on:
     push:
       branches: [dev]
     workflow_dispatch:

   jobs:
     deploy-dev:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v3
           with:
             fetch-depth: 0
             lfs: true

         - name: Push to HuggingFace Dev Space
           uses: nateraw/huggingface-sync-action@v0.0.4
           with:
             github_repo_id: joerawr/omfgg  # CHANGE THIS
             huggingface_repo_id: YOUR_HF_USERNAME/omfgg-dev  # CHANGE THIS
             repo_type: space
             space_sdk: gradio
             hf_token: ${{ secrets.HF_TOKEN }}
   ```

4. **Update BOTH workflow files**
   - Replace `joerawr/omfgg` with your GitHub `username/repo`
   - Replace `YOUR_HF_USERNAME` with your HuggingFace username
   - Production deploys from `main` to `omfgg` Space
   - Dev deploys from `dev` to `omfgg-dev` Space

4. **Add HuggingFace token to GitHub Secrets**
   - Go to your GitHub repo
   - Click Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `HF_TOKEN`
   - Value: Paste the `hf_...` token from Step 3
   - Click "Add secret"

5. **Create `dev` branch in GitHub**
   ```bash
   git checkout -b dev
   git push origin dev
   git checkout main
   ```

6. **Commit and push workflows**
   ```bash
   git add .github/workflows/
   git commit -m "Add HuggingFace multi-environment deploy workflows"
   git push origin main
   ```

7. **Verify deployments**
   - Go to GitHub repo → Actions tab
   - You should see "Deploy to Production" workflow running
   - Wait 2-5 minutes for build to complete
   - Check production Space - app should be live!

   - Switch to `dev` branch and push to trigger dev deployment:
   ```bash
   git checkout dev
   git push origin dev
   ```
   - Check dev Space - should deploy to `omfgg-dev`

## Step 5: Add App Secrets to BOTH HuggingFace Spaces

**Do this for BOTH Production and Dev Spaces:**

1. **Add secrets to PRODUCTION Space**
   - Open: `https://huggingface.co/spaces/[username]/omfgg`
   - Click "Settings" tab
   - Scroll to "Repository secrets"
   - Click "New secret" and add:
     - **Name:** `OPENAI_API_KEY`, **Value:** `sk-...` (production key)
     - **Name:** `ANTHROPIC_API_KEY`, **Value:** `sk-ant-...` (production key)

2. **Add secrets to DEV Space**
   - Open: `https://huggingface.co/spaces/[username]/omfgg-dev`
   - Click "Settings" tab
   - Scroll to "Repository secrets"
   - Click "New secret" and add:
     - **Name:** `OPENAI_API_KEY`, **Value:** `sk-...` (dev/test key - can be same or different)
     - **Name:** `ANTHROPIC_API_KEY`, **Value:** `sk-ant-...` (dev/test key)

3. **Restart both Spaces** (if needed)
   - Click "Settings" → "Factory Rebuild"

**Note:** You can use the same API keys for both, or separate keys to track dev vs prod costs.

## Step 6: Add Team Members to Space

1. **Go to Space settings**
   - Click "Settings" tab
   - Scroll to "Collaborators"

2. **Add team members**
   - Click "Add collaborator"
   - Enter their HuggingFace username
   - Select role:
     - **Admin:** Full control (recommended for core team)
     - **Write:** Can edit, add secrets
     - **Read:** View only

3. **Share GitHub repo access**
   - Add team members to GitHub repo (if not already)
   - Settings → Collaborators → Add people

---

# Part 2: Team Member Setup (Everyone Else)

**Time:** 5-10 minutes
**Who:** All other developers on the team

## Step 1: Create HuggingFace Account

1. **Sign up** (if you don't have an account)
   - Go to https://huggingface.co
   - Click "Sign Up" (free)
   - Verify email

2. **Share your username**
   - Tell the project lead your HuggingFace username
   - They'll add you as a collaborator to the Space

## Step 2: Clone GitHub Repository

1. **Clone the repo** (if you haven't already)
   ```bash
   git clone https://github.com/joerawr/omfgg.git
   cd omfgg
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create local .env file**

   Create `.env.local` (this is gitignored):
   ```bash
   OPENAI_API_KEY=sk-your-dev-key-here
   ANTHROPIC_API_KEY=sk-ant-your-dev-key-here
   ```

   **Note:** Use your own API keys for local development, not production keys

## Step 3: Test Locally

1. **Run the app**
   ```bash
   source venv/bin/activate
   python app_with_agents.py
   ```

2. **Open browser**
   - Go to http://localhost:7860
   - Test game generation
   - Verify it works with your API keys

## Step 4: Development Workflow (Multi-Environment)

**Here's the recommended workflow for 4-person team:**

### Option A: Merge to Dev First (Recommended)

1. **Create feature branch from `dev`**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/your-feature-name
   ```

2. **Make changes & test locally**
   ```bash
   # Edit files
   python app_with_agents.py  # Test locally
   ```

3. **Commit & push feature branch**
   ```bash
   git add .
   git commit -m "Add new game feature"
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request to `dev` branch**
   - Go to GitHub repo
   - Click "Pull requests" → "New pull request"
   - **Base:** `dev` ← **Compare:** `feature/your-feature-name`
   - Request review from team

5. **Team reviews & merges to `dev`**
   - Once approved, merge PR to `dev`
   - **Auto-deploys to DEV Space!** (`omfgg-dev`)
   - Team tests at: `https://huggingface.co/spaces/[username]/omfgg-dev`

6. **When `dev` is stable, merge to `main`**
   - Create PR: `main` ← `dev`
   - Final review
   - Merge to `main`
   - **Auto-deploys to PRODUCTION!** (`omfgg`)

### Option B: Personal Dev Spaces (For Heavy Testing)

If you need your own isolated environment:

1. **Create your personal Space** (one-time setup)
   - Go to HuggingFace → Create Space
   - Name: `omfgg-yourname` (e.g., `omfgg-alice`)
   - Copy settings from main Space

2. **Create personal workflow** (one-time setup)
   - Create `.github/workflows/deploy-yourname.yml`:
   ```yaml
   name: Deploy to Alice's Dev Space

   on:
     push:
       branches: [alice/dev]
     workflow_dispatch:

   jobs:
     deploy-alice:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
           with:
             fetch-depth: 0
             lfs: true
         - uses: nateraw/huggingface-sync-action@v0.0.4
           with:
             github_repo_id: joerawr/omfgg
             huggingface_repo_id: YOUR_USERNAME/omfgg-alice
             repo_type: space
             space_sdk: gradio
             hf_token: ${{ secrets.HF_TOKEN }}
   ```

3. **Use personal branch**
   ```bash
   git checkout -b alice/dev
   # Make changes, test
   git push origin alice/dev
   # Auto-deploys to YOUR Space only!
   ```

4. **When ready, merge to team `dev`**
   - Create PR: `dev` ← `alice/dev`
   - Team reviews
   - Deploys to shared `omfgg-dev` Space

### Environment Promotion Flow

```
Local Testing
    ↓
Feature Branch (yourname/feature)
    ↓
Personal Space (optional: omfgg-yourname)
    ↓
Dev Branch → DEV Space (omfgg-dev) ← Team testing
    ↓
Main Branch → PRODUCTION (omfgg) ← Demo/Hackathon
```

---

# Quick Reference

## Workflow Summary (Multi-Environment)

### Standard Flow (Recommended)
```
Developer:
1. git checkout dev
2. git checkout -b feature/new-thing
3. Make changes, test locally
4. git push origin feature/new-thing
5. Create PR to `dev` branch

Team:
6. Review PR
7. Merge to `dev`

GitHub Action (automatic):
8. Detects merge to `dev`
9. Deploys to DEV Space (omfgg-dev)

Team Testing:
10. Test at https://huggingface.co/spaces/[username]/omfgg-dev
11. If stable, create PR: main ← dev
12. Merge to `main`

GitHub Action (automatic):
13. Deploys to PRODUCTION (omfgg)

Result:
14. Demo-ready at https://huggingface.co/spaces/[username]/omfgg
```

### With Personal Spaces
```
Developer → Personal Branch → Personal Space (test alone)
    ↓
Team Dev Branch → Dev Space (test together)
    ↓
Main Branch → Production (demo/hackathon)
```

## Important URLs

- **Production Space:** https://huggingface.co/spaces/[username]/omfgg
- **Dev/Staging Space:** https://huggingface.co/spaces/[username]/omfgg-dev
- **Personal Space (if using):** https://huggingface.co/spaces/[username]/omfgg-yourname
- **GitHub Repo:** https://github.com/joerawr/omfgg
- **GitHub Actions:** https://github.com/joerawr/omfgg/actions
- **HF Settings:** https://huggingface.co/settings/tokens

## Troubleshooting

### "Build failed" on HuggingFace
- Check GitHub Actions logs for errors
- Verify `requirements.txt` has all dependencies
- Check README.md has correct frontmatter

### "Secrets not found" error
- Go to HF Space Settings → Repository secrets
- Add `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`
- Click "Factory Rebuild"

### App doesn't update after merge
- Check GitHub Actions tab - did workflow run?
- **Check which branch you merged to** - `dev` deploys to `omfgg-dev`, `main` deploys to `omfgg`
- If workflow succeeded but app unchanged, try "Factory Rebuild" in HF Settings
- Clear browser cache

### "Which Space am I looking at?"
- Production: `huggingface.co/spaces/[username]/omfgg` (from `main` branch)
- Dev/Staging: `huggingface.co/spaces/[username]/omfgg-dev` (from `dev` branch)
- Check Space settings to see which branch it's synced to

### Can't see the Space
- Verify you were added as collaborator (check HF notifications)
- Make sure Space is Public (required for hackathon)

### Local development issues
- Make sure venv is activated: `source venv/bin/activate`
- Verify `.env.local` has your API keys
- Check `omfgg_app.log` for errors

---

# Security Best Practices

## DO ✅
- Use `.env.local` for local development (gitignored)
- Add production API keys to HuggingFace Space secrets
- Add `HF_TOKEN` to GitHub Secrets (not to code)
- Keep `.gitignore` updated

## DON'T ❌
- Commit API keys to GitHub
- Share HuggingFace tokens in Slack/Discord
- Use production keys in local development
- Push `.env` or `.env.local` files

---

# For the Hackathon

## Required for Submission
- ✅ HuggingFace Space must be **Public**
- ✅ README.md must have tag `mcp-in-action`
- ✅ Demo video link in README
- ✅ Social media post link in README

## Deployment Checklist
- [ ] Space is Public
- [ ] App loads without errors
- [ ] All 5 game modes work
- [ ] Mobile-friendly (test on phone)
- [ ] README has complete docs
- [ ] Demo video uploaded & linked

---

**Questions?**
- HuggingFace Docs: https://huggingface.co/docs/hub/spaces
- GitHub Actions: https://docs.github.com/en/actions
- Team chat: [your team communication channel]
