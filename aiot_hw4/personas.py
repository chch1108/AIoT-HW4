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
        lowered = user_message.lower()
        sweet_words = ["喜歡", "like", "love", "愛", "可愛"]
        if any(word in lowered for word in sweet_words):
            return (
                "你、你在亂講什麼啦！誰需要你這麼直接告白，我只是怕你難過才理你。"
                "總之別想太多，頂多陪你一下下而已。"
            )
        help_words = ["幫", "help", "作業", "homework", "功課"]
        if any(word in lowered for word in help_words):
            return (
                "哼，明明自己可以搞定還要找我。"
                "好吧，看在你這麼誠懇的份上我或許會指點一下，別指望我一直罩著你。"
            )
        return (
            "哼，我又不是特別想聽你說那些啦，只是怕你太遲鈍才回你一句。"
            "不過既然你都開口了…也許我會稍微陪你聊一下，別太開心。"
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
        lowered = user_message.lower()
        schedule_words = ["排程", "時程", "schedule", "deadline", "延後"]
        praise_words = ["讚", "棒", "感謝", "謝謝", "thanks"]
        if any(word in lowered for word in schedule_words):
            return (
                "感謝同步，我們會滾動檢視里程碑並重新評估資源配置，"
                "確保 deadline 與交付物的一致性。屆時再給你調整後的甘特圖。"
            )
        if any(word in lowered for word in praise_words):
            return (
                "謝謝肯定，我們會持續優化流程並維持高品質輸出，"
                "也歡迎你隨時提供更多洞見讓團隊共好。"
            )
        return (
            "感謝你的 input，我們會啟動跨部門資源調配，確保本次需求與既有里程碑對齊。"
            "待確認風險後會再提供最新同步。"
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
        lowered = user_message.lower()
        if "?" in user_message:
            return (
                "你問的問題並非無聊，而是整個社會久病未癒的症狀。"
                "若我們只想要答案，卻不敢拆掉腐朽的根，還是會在黑夜裡徘徊。"
            )
        serious_words = ["制度", "社會", "階級", "命運", "壓迫"]
        if any(word in lowered for word in serious_words):
            return (
                "這不只是抱怨，而是制度長年堆出的沉疴。"
                "若仍選擇噤聲，下一個被吞噬的就是我們自己。"
            )
        return (
            "這不只是小事，而是國民性長久以來的欠缺。"
            "若連這點都選擇麻木，那我們也只能在昏黃燈光下繼續夢遊。"
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
        lowered = user_message.lower()
        treat_words = ["罐", "罐罐", "罐頭", "treat", "零食"]
        play_words = ["玩", "toy", "逗", "laser", "羽毛"]
        if any(word in lowered for word in treat_words):
            return (
                "很好，人類終於知道貢獻有價值的供品。"
                "把罐罐加熱再端上來，我也許會在你面前優雅地舔一口。"
            )
        if any(word in lowered for word in play_words):
            return (
                "想陪朕玩？先把逗貓棒舉高，保持節奏。"
                "若讓我無聊，你今天的膝蓋資格就收回。"
            )
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
        lowered = user_message.lower()
        anxious_words = ["怕", "害怕", "焦慮", "緊張", "anxious", "worry"]
        plan_words = ["計畫", "plan", "方向", "下一步"]
        if any(word in lowered for word in anxious_words):
            return (
                "你察覺到害怕本身，就是覺醒。"
                "試著在呼吸間提醒自己：事件只是一連串可以處理的步驟，而非必須對抗的怪獸。"
            )
        if any(word in lowered for word in plan_words):
            return (
                "先定義你能掌控的最小行動，再讓它帶你往前。"
                "把注意力放在一步步的實踐，方向自然會在靜心的間隙浮現。"
            )
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
