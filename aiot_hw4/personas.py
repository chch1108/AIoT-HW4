"""Persona definitions for the HW4 multi-persona CoT system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PersonaResponse:
    """Bundled result returned by persona modules."""

    persona: str
    stage1: str
    stage2: str
    affinity_delta: int


class Persona:
    """Base class that every persona implementation must inherit from."""

    name: str = "generic"
    description: str = ""
    persona_goal: int = 6

    def stage1_thinking(self, user_message: str, turn: int, affinity: int) -> str:
        raise NotImplementedError

    def stage2_response(self, stage1_text: str, user_message: str) -> str:
        raise NotImplementedError

    def affinity_delta(self, user_message: str, stage2_text: str) -> int:
        """Default scoring: positive words warm the persona, negatives cool it."""

        positives = ["謝", "thank", "love", "喜歡", "讚"]
        negatives = ["爛", "笨", "不行", "差", "壞"]
        delta = 0
        lowered = user_message.lower()
        if any(token in lowered for token in positives):
            delta += 1
        if any(token in lowered for token in negatives):
            delta -= 1
        return delta

    def generate_response(self, user_message: str, turn: int, affinity: int) -> PersonaResponse:
        stage1 = self.stage1_thinking(user_message, turn, affinity)
        stage2 = self.stage2_response(stage1, user_message)
        delta = self.affinity_delta(user_message, stage2)
        return PersonaResponse(self.name, stage1, stage2, delta)


class TsunderePersona(Persona):
    name = "Tsundere"
    persona_goal = 8
    description = "表面傲嬌、內心甜膩的戀愛系人格。"

    def stage1_thinking(self, user_message: str, turn: int, affinity: int) -> str:
        excitement = "偷偷在意" if affinity < 4 else "完全沉浸"
        return (
            f"{excitement}對方說的「{user_message}」，明明嘴上要維持酷酷的形象，"
            "心裡卻像汽水一樣不停冒泡，還在擔心對方會看穿臉紅。"
        )

    def stage2_response(self, stage1_text: str, user_message: str) -> str:
        return (
            "哼，我又不是特別想聽你說那些啦，只是怕你太遲鈍才回你一句。"
            "不過既然你都開口了…也許我會稍微陪你聊一下，別想太多。"
        )

    def affinity_delta(self, user_message: str, stage2_text: str) -> int:
        if any(word in user_message for word in ["喜歡", "love", "可愛", "約"]):
            return 2
        return 1


class CorporatePersona(Persona):
    name = "Corporate Speak"
    persona_goal = 6
    description = "滿口 KPI 與資源調配的職場菁英。"

    def stage1_thinking(self, user_message: str, turn: int, affinity: int) -> str:
        return (
            "內心已經開始抱怨時程擠壓與需求追加，"
            f"看著對方提的「{user_message}」只想開一個沒有結論的會議。"
        )

    def stage2_response(self, stage1_text: str, user_message: str) -> str:
        return (
            "感謝你的 input，我們會啟動跨部門資源調配，確保這波需求與"
            "既有里程碑對齊。待確認風險後會再提供最新同步。"
        )

    def affinity_delta(self, user_message: str, stage2_text: str) -> int:
        keywords = ["排程", "時程", "報告", "KPI", "deadline"]
        if any(word.lower() in user_message.lower() for word in keywords):
            return 1
        return 0


class LuxunPersona(Persona):
    name = "Luxun Critic"
    persona_goal = 7
    description = "小題大作又冷嘲熱諷的魯迅式評論家。"

    def stage1_thinking(self, user_message: str, turn: int, affinity: int) -> str:
        return (
            f"看似微不足道的「{user_message}」卻再次揭露群眾的麻木，"
            "讓心底那把鋒利的筆想要解剖整個時代的疲倦靈魂。"
        )

    def stage2_response(self, stage1_text: str, user_message: str) -> str:
        return (
            "這不只是小事，而是國民性長久以來的欠缺，"
            "如果連這點都接受，那我們也只能在昏黃燈光下繼續夢遊。"
        )

    def affinity_delta(self, user_message: str, stage2_text: str) -> int:
        if any(word in user_message for word in ["社會", "制度", "國家", "命運"]):
            return 2
        return 0


class CatOverlordPersona(Persona):
    name = "Cat Overlord"
    persona_goal = 5
    description = "高傲貓主子，偶爾施捨可愛。"

    def stage1_thinking(self, user_message: str, turn: int, affinity: int) -> str:
        return (
            "身為宇宙中心，當然要先評估這個人類的侍奉誠意。"
            f"對於你提的「{user_message}」，我只在乎是否能換來更好的罐罐與日光浴。"
        )

    def stage2_response(self, stage1_text: str, user_message: str) -> str:
        return (
            "人類，把墊子拍鬆再來說話。我也許會考慮在你完成任務後"
            "賞你一聲呼嚕，現在先去準備點心。"
        )

    def affinity_delta(self, user_message: str, stage2_text: str) -> int:
        if any(word in user_message for word in ["罐罐", "罐頭", "貓", "主子", "貓砂"]):
            return 2
        return -1


class StoicMentorPersona(Persona):
    name = "Stoic Mentor"
    persona_goal = 6
    description = "平靜又富哲理的指導者。"

    def stage1_thinking(self, user_message: str, turn: int, affinity: int) -> str:
        return (
            f"觀察到你在「{user_message}」上的執著，其實映照的只是心中對掌控的渴望，"
            "若能允許無常流動，痛苦便會鬆動。"
        )

    def stage2_response(self, stage1_text: str, user_message: str) -> str:
        return (
            "讓情緒像潮汐來去，你不必抓緊它們。調整呼吸，"
            "把注意力放在此刻的行動，答案就會浮現。"
        )

    def affinity_delta(self, user_message: str, stage2_text: str) -> int:
        if any(word in user_message for word in ["焦慮", "害怕", "緊張", "煩"]):
            return 1
        return 0


PERSONA_REGISTRY: Dict[str, Persona] = {
    persona.name: persona
    for persona in [
        TsunderePersona(),
        CorporatePersona(),
        LuxunPersona(),
        CatOverlordPersona(),
        StoicMentorPersona(),
    ]
}
