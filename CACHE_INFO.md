# Cache System (Development Feature)

## Purpose

Saves sub-agent results to disk so you don't lose them when restarting the app during development. This saves API costs during iteration.

## How It Works

### When You Generate a Game:

1. Sub-agents run and return results
2. Results are saved to `cache/latest_cache.json`
3. You see: "💾 *Results cached to disk for next session*"
4. Results are also in Gradio State (in-memory)

### When You Restart the App:

1. App starts
2. Automatically loads `cache/latest_cache.json`
3. Cached results populate the Gradio State
4. You can immediately click "Regenerate" without generating first!

### File Structure:

```
cache/
└── latest_cache.json
```

### Cache File Format:

```json
{
  "timestamp": "2025-11-15T19:30:45.123456",
  "mode": "Funny",
  "user_inputs": {
    "Subject": "pickle",
    "Action": "dancing"
  },
  "sub_agent_outputs": {
    "character": "{...JSON...}",
    "mechanic": "{...JSON...}",
    "style": "{...JSON...}",
    "level": "{...JSON...}",
    "twist": "{...JSON...}"
  }
}
```

## Testing the Cache

### Test 1: Within Session
```bash
1. Start app: python3 app_with_agents.py
2. Generate a game → Cache saved ✓
3. Click "Regenerate" → Uses cache ✓
```

### Test 2: Across Restarts
```bash
1. Start app: python3 app_with_agents.py
2. Generate a game → Cache saved to disk ✓
3. Stop app (Ctrl-C)
4. Start app again: python3 app_with_agents.py
   → Console shows: "📂 Cache loaded from cache/latest_cache.json"
5. Click "Regenerate" → Uses cached results from disk! ✓
```

## Checking the Cache

### View the cache file:
```bash
cat cache/latest_cache.json | python3 -m json.tool
```

### Check if cache exists:
```bash
ls -lh cache/
```

### View cache timestamp:
```bash
cat cache/latest_cache.json | grep timestamp
```

## Clearing the Cache

### Option 1: Delete the cache file
```bash
rm cache/latest_cache.json
```

### Option 2: Delete entire cache directory
```bash
rm -rf cache/
```

The directory will be recreated automatically on next app start.

## Logs

Cache operations are logged to `omfgg_app.log`:

```bash
# See cache saves
grep "Cache saved" omfgg_app.log

# See cache loads
grep "Cache loaded" omfgg_app.log
```

## Before Production

**IMPORTANT:** This is a development feature. Before deploying:

1. Remove cache loading logic from `app_with_agents.py`
2. Remove `save_cache()` calls
3. Delete `cache/` directory
4. Remove from `.gitignore` (or keep if using different storage)

The cache directory is already gitignored, so it won't be committed.

## Cost Savings

### Without Cache Across Restarts:
```
Session 1: Generate → $0.0085
Stop/Restart
Session 2: Generate again → $0.0085
Total: $0.017
```

### With Cache Across Restarts:
```
Session 1: Generate → $0.0085 (cached to disk)
Stop/Restart
Session 2: Regenerate → $0.0013 (uses disk cache!)
Total: $0.0098
```

**Savings: 42% cheaper!**

## Troubleshooting

### Cache not loading?
Check logs:
```bash
tail omfgg_app.log | grep cache
```

### Wrong cache being used?
The cache file shows timestamp and inputs:
```bash
cat cache/latest_cache.json | head -10
```

Delete and regenerate if needed.

### Want multiple caches?
Currently only saves one cache (latest). Could enhance to save multiple with timestamps/slugs if needed.
