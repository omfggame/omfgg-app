"""
Persistence helpers for narrative games and playthroughs.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from models import GameSpec, GameState

DATA_DIR = Path(__file__).resolve().parent / "data"
GAMES_DIR = DATA_DIR / "games"
RUNS_DIR = DATA_DIR / "runs"

# Ensure directories exist at import time
for directory in (DATA_DIR, GAMES_DIR, RUNS_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def _read_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_game_spec(game: GameSpec) -> Path:
    """
    Persist a `GameSpec` as JSON to `data/games/<game_id>.json`.

    Returns the path to the saved file.
    """
    path = GAMES_DIR / f"{game.id}.json"
    _write_json(path, game.to_dict())
    return path


def load_game_spec(game_id: str) -> GameSpec:
    """
    Load a `GameSpec` JSON file by id.
    """
    path = GAMES_DIR / f"{game_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Game spec '{game_id}' not found at {path}")
    data = _read_json(path)
    return GameSpec.from_dict(data)


def save_game_state(state: GameState, run_id: Optional[str] = None) -> Path:
    """
    Persist the current `GameState` to `data/runs/<run_id>.json`.

    If `run_id` is not provided, generate one using timestamp + game id.
    """
    if run_id is None:
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        run_id = f"{state.game_id}-{timestamp}"
    path = RUNS_DIR / f"{run_id}.json"
    payload = {
        "run_id": run_id,
        "saved_at": datetime.utcnow().isoformat(),
        "state": state.to_dict(),
    }
    _write_json(path, payload)
    return path


def load_game_state(run_id: str) -> GameState:
    """
    Load a previously saved `GameState` from disk.
    """
    path = RUNS_DIR / f"{run_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Run '{run_id}' not found at {path}")
    payload = _read_json(path)
    state_dict = payload.get("state")
    if not isinstance(state_dict, dict):
        raise ValueError(f"Run '{run_id}' file missing 'state' payload.")
    return GameState.from_dict(state_dict)


def list_saved_games() -> List[Dict]:
    """
    Return metadata about saved games.
    """
    games: List[Dict] = []
    for path in sorted(GAMES_DIR.glob("*.json")):
        try:
            data = _read_json(path)
            games.append(
                {
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "mode": data.get("mode"),
                    "path": str(path),
                    "scene_count": len(data.get("scenes", {})),
                    "saved_at": datetime.utcfromtimestamp(path.stat().st_mtime).isoformat(),
                }
            )
        except Exception:
            # Skip corrupted files but continue listing others
            continue
    return games


def list_saved_runs(game_id: Optional[str] = None) -> List[Dict]:
    """
    Return metadata for saved playthroughs, optionally filtered by game id.
    """
    runs: List[Dict] = []
    for path in sorted(RUNS_DIR.glob("*.json")):
        try:
            payload = _read_json(path)
            state = payload.get("state", {})
            if game_id and state.get("game_id") != game_id:
                continue
            runs.append(
                {
                    "run_id": payload.get("run_id"),
                    "game_id": state.get("game_id"),
                    "path": str(path),
                    "saved_at": payload.get("saved_at"),
                    "score": state.get("score"),
                    "is_complete": state.get("is_complete"),
                    "ending_tag": state.get("ending_tag"),
                }
            )
        except Exception:
            continue
    return runs


