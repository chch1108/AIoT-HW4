"""High level controller that wires personas, CoT engine and RPG engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .engines import RPGEngine, TwoStageCoTEngine
from .personas import PERSONA_REGISTRY, Persona


@dataclass
class ConversationTurn:
    idx: int
    user_message: str
    persona: str
    stage2: str
    stage1: str
    masked_stage1: str
    affinity_delta: int
    revealed: bool = False


@dataclass
class ConversationState:
    persona_name: str
    turn: int
    affinity: int
    status: str
    ending_text: str | None
    history: List[ConversationTurn] = field(default_factory=list)


class ConversationOrchestrator:
    """Encapsulates gameplay-level flow control."""

    def __init__(self, persona_name: str = "Tsundere") -> None:
        self.cot_engine = TwoStageCoTEngine()
        self.rpg_engine = RPGEngine()
        self._persona = PERSONA_REGISTRY[persona_name]
        self.state = ConversationState(
            persona_name=self._persona.name,
            turn=0,
            affinity=0,
            status="CONTINUE",
            ending_text=None,
        )

    @property
    def persona(self) -> Persona:
        return self._persona

    def switch_persona(self, persona_name: str) -> None:
        self._persona = PERSONA_REGISTRY[persona_name]
        self.state = ConversationState(
            persona_name=self._persona.name,
            turn=0,
            affinity=0,
            status="CONTINUE",
            ending_text=None,
            history=[],
        )

    def run_turn(self, message: str) -> ConversationState:
        if self.state.status != "CONTINUE":
            return self.state

        cot_result = self.cot_engine.run(self._persona, message, self.state.turn, self.state.affinity)
        new_turn = ConversationTurn(
            idx=self.state.turn + 1,
            user_message=message,
            persona=self._persona.name,
            stage2=cot_result.response.stage2,
            stage1=cot_result.response.stage1,
            masked_stage1=cot_result.masked_stage1,
            affinity_delta=cot_result.response.affinity_delta,
        )

        state_after_rpg = self.rpg_engine.update(
            persona=self._persona,
            current_turn=self.state.turn,
            current_affinity=self.state.affinity,
            delta=cot_result.response.affinity_delta,
        )

        history = [*self.state.history, new_turn]
        self.state = ConversationState(
            persona_name=self._persona.name,
            turn=state_after_rpg.turn,
            affinity=state_after_rpg.affinity,
            status=state_after_rpg.status,
            ending_text=state_after_rpg.ending_text,
            history=history,
        )
        return self.state

    def reveal_turn(self, idx: int) -> None:
        for turn in self.state.history:
            if turn.idx == idx:
                turn.revealed = True
                break
