"""Core engines: Two-Stage CoT and RPG affinity tracker."""

from __future__ import annotations

from dataclasses import dataclass

from .personas import Persona, PersonaResponse


@dataclass
class CoTResult:
    response: PersonaResponse
    masked_stage1: str


def _mask_text(text: str) -> str:
    return "█" * max(4, len(text))


class TwoStageCoTEngine:
    """Runs Stage 1/Stage 2 for the activated persona."""

    def run(
        self,
        persona: Persona,
        user_message: str,
        turn: int,
        affinity: int,
        forced_response: PersonaResponse | None = None,
    ) -> CoTResult:
        persona_response = forced_response or persona.generate_response(user_message, turn, affinity)
        masked = _mask_text(persona_response.stage1)
        return CoTResult(response=persona_response, masked_stage1=masked)


@dataclass
class RPGState:
    turn: int
    affinity: int
    status: str
    ending_text: str | None = None


class RPGEngine:
    """Applies persona-specific affinity and ending rules."""

    def __init__(self, turn_limit: int = 10) -> None:
        self.turn_limit = turn_limit

    def update(self, persona: Persona, current_turn: int, current_affinity: int, delta: int) -> RPGState:
        next_turn = current_turn + 1
        next_affinity = current_affinity + delta
        status = "CONTINUE"
        ending = None
        if next_affinity >= persona.persona_goal:
            status = "GOOD_END"
            ending = (
                f"{persona.name} 的好感度達到目標，故事解鎖圓滿結局。"
            )
        elif next_turn > self.turn_limit:
            status = "BAD_END"
            ending = "回合數耗盡，對方客氣告退，只剩你與螢幕相伴。"
        return RPGState(turn=next_turn, affinity=next_affinity, status=status, ending_text=ending)
