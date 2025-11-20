"""
Deterministic state management for branching narrative games.
"""

from __future__ import annotations

from typing import Dict, Optional
from datetime import datetime

from models import Choice, GameSpec, GameState, Scene


class GameEngineError(Exception):
    """Base error for the game engine."""


class InvalidChoiceError(GameEngineError):
    """Raised when a requested choice cannot be applied."""


class GameEngine:
    """
    Provides deterministic state transitions for a branching narrative game.
    """

    def __init__(self, game_spec: GameSpec, initial_state: Optional[GameState] = None):
        self.game = game_spec
        starting_stats = game_spec.metadata.get("starting_stats", {})
        self.state = initial_state or GameState(
            game_id=game_spec.id,
            current_scene_id=game_spec.start_scene_id,
            score=game_spec.metadata.get("starting_score", 0),
            stats=starting_stats.copy() if isinstance(starting_stats, dict) else {},
        )

    # -- Basic helpers -----------------------------------------------------------------

    def reset(self) -> None:
        """Reset the engine to the starting scene."""
        self.state.current_scene_id = self.game.start_scene_id
        self.state.score = self.game.metadata.get("starting_score", 0)
        self.state.inventory = []
        starting_stats = self.game.metadata.get("starting_stats", {})
        self.state.stats = starting_stats.copy() if isinstance(starting_stats, dict) else {}
        self.state.history = []
        self.state.is_complete = False
        self.state.ending_tag = None

    def get_current_scene(self) -> Scene:
        """Return the active scene."""
        try:
            return self.game.scenes[self.state.current_scene_id]
        except KeyError as exc:
            raise GameEngineError(f"Scene '{self.state.current_scene_id}' missing from game spec") from exc

    def get_choice(self, choice_id: str) -> Choice:
        """Return a choice by identifier within the current scene."""
        for choice in self.get_current_scene().choices:
            if choice.id == choice_id:
                return choice
        raise InvalidChoiceError(f"Choice '{choice_id}' not found in scene '{self.state.current_scene_id}'")

    # -- Core transition logic ---------------------------------------------------------

    def apply_choice(self, choice_id: str) -> Dict:
        """
        Apply a player's choice and return an updated snapshot for UI rendering.

        Returns:
            dict: Snapshot including scene info, state values, and terminal data.
        """
        current_scene = self.get_current_scene()
        choice = self.get_choice(choice_id)

        # Update score
        self.state.score += choice.delta_score

        # Update stats
        if choice.stat_changes:
            for stat, delta in choice.stat_changes.items():
                self.state.stats[stat] = self.state.stats.get(stat, 0) + delta

        # Loot handling
        if choice.loot:
            self.state.inventory.append(choice.loot)

        # Record history (immutable entry to support UI timeline)
        history_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "scene_id": current_scene.id,
            "scene_title": current_scene.title,
            "choice_id": choice.id,
            "choice_label": choice.label,
            "result_text": choice.result_text,
            "delta_score": choice.delta_score,
            "risk_level": choice.risk_level,
            "loot": choice.loot,
            "stat_changes": choice.stat_changes,
            "next_scene_id": choice.next_scene_id,
        }
        self.state.history.append(history_entry)

        # Determine next scene
        next_scene_id = choice.next_scene_id
        if next_scene_id:
            if next_scene_id not in self.game.scenes:
                raise GameEngineError(f"Scene '{next_scene_id}' referenced by choice '{choice.id}' is missing.")
            self.state.current_scene_id = next_scene_id
            next_scene = self.game.scenes[next_scene_id]
            self.state.is_complete = bool(next_scene.is_terminal)
            self.state.ending_tag = next_scene.ending_tag if next_scene.is_terminal else None
        else:
            # Remain on the current scene but mark completion
            self.state.is_complete = True
            self.state.ending_tag = current_scene.ending_tag

        if self.state.is_complete and not next_scene_id:
            # Preserve current scene for UI but ensure choices are disabled
            self.state.current_scene_id = current_scene.id
            self.state.history[-1]["ending_tag"] = self.state.ending_tag or current_scene.ending_tag
        elif self.state.is_complete:
            self.state.history[-1]["ending_tag"] = self.state.ending_tag

        return self._build_snapshot(choice)

    # -- Snapshot logic ----------------------------------------------------------------

    def _build_snapshot(self, last_choice: Optional[Choice] = None) -> Dict:
        """
        Build a comprehensive state snapshot for UI rendering.
        """
        scene: Optional[Scene]

        if self.state.current_scene_id and self.state.current_scene_id in self.game.scenes:
            scene = self.game.scenes[self.state.current_scene_id]
        else:
            scene = None

        game_over = self.state.is_complete or (scene.is_terminal if scene else True)
        ending_tag = self.state.ending_tag or (scene.ending_tag if scene and scene.is_terminal else None)

        scene_payload = None
        if scene:
            scene_payload = scene.to_dict()
            if game_over:
                # Do not expose further choices once the game is complete
                scene_payload["choices"] = []

        return {
            "scene": scene_payload,
            "game_over": game_over,
            "ending_tag": ending_tag,
            "last_choice": last_choice.to_dict() if last_choice else None,
            "state": self.state.to_dict(),
            "metadata": self.game.metadata,
        }

    # -- Serialization helpers ---------------------------------------------------------

    def to_dict(self) -> Dict:
        """Serialize engine contents for persistence."""
        return {
            "game": self.game.to_dict(),
            "state": self.state.to_dict(),
        }

    def snapshot(self) -> Dict:
        """Return the current engine snapshot without applying a choice."""
        return self._build_snapshot(None)

    @staticmethod
    def from_dict(payload: Dict) -> "GameEngine":
        """Restore a `GameEngine` instance from persisted data."""
        game_spec = GameSpec.from_dict(payload["game"])
        game_state = GameState.from_dict(payload["state"])
        return GameEngine(game_spec, game_state)


