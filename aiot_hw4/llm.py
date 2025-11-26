"""LLM client helper for persona-aware generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Sequence, Tuple

try:
    import google.generativeai as genai
except ImportError as exc:  # pragma: no cover - optional dependency
    genai = None
    GENAI_IMPORT_ERROR = exc
else:
    GENAI_IMPORT_ERROR = None


SYSTEM_PROMPT = """You are a game-like AI that roleplays personas with a two-stage thought process.
Given the persona information and the user's input, produce JSON with exactly two fields:
- stage1: the hidden inner thinking that follows the persona's Stage 1 instructions.
- stage2: the outward response that the user can see, following Stage 2 instructions.
Keep it concise (<= 3 sentences each), write in the persona's voice, and stay in Traditional Chinese when appropriate."""

DEFAULT_MODEL_CANDIDATES = (
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
)


@dataclass
class LLMClient:
    api_key: str
    model_name: str | None = None
    model_candidates: Sequence[str] = DEFAULT_MODEL_CANDIDATES

    def __post_init__(self) -> None:
        if genai is None:
            message = "google-generativeai is not installed"
            if GENAI_IMPORT_ERROR:
                message += f": {GENAI_IMPORT_ERROR}"
            raise RuntimeError(message)
        if not self.api_key:
            raise ValueError("GENAI API key is required")
        genai.configure(api_key=self.api_key)
        self._model = self._init_model()

    def generate(self, persona, user_message: str) -> Tuple[str, str]:
        prompt = self._build_prompt(persona, user_message)
        response = self._model.generate_content(prompt)
        text = response.text or ""
        return self._parse_response(text)

    @staticmethod
    def _build_prompt(persona, user_message: str) -> str:
        return (
            f"{SYSTEM_PROMPT}\n"
            f"Persona Name: {persona.name}\n"
            f"Persona Description: {persona.description}\n"
            "Stage 1 Instructions: "
            "用內心戲描述該 persona 真實的感受與盤算，不能被使用者看到。\n"
            "Stage 2 Instructions: 使用 persona 的外在語氣回覆，保持個性。\n"
            f"User Message: {user_message}\n"
            "Respond with valid JSON only: {\"stage1\": \"...\", \"stage2\": \"...\"}."
        )

    @staticmethod
    def _parse_response(raw_text: str) -> Tuple[str, str]:
        cleaned = raw_text.strip()
        if "```" in cleaned:
            cleaned = cleaned.replace("```json", "").replace("```", "")
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            cleaned = cleaned[start : end + 1]
        data = json.loads(cleaned)
        stage1 = data.get("stage1") or data.get("stage_1")
        stage2 = data.get("stage2") or data.get("stage_2")
        if not stage1 or not stage2:
            raise ValueError("LLM response missing stage1/stage2 fields")
        return stage1.strip(), stage2.strip()

    def _init_model(self):
        errors = []
        for name in self._ordered_candidates():
            try:
                model = genai.GenerativeModel(name)
                self.model_name = name
                return model
            except Exception as exc:  # pragma: no cover - remote dependency
                errors.append(f"{name}: {exc}")
        joined = "; ".join(errors) if errors else "unknown error"
        raise RuntimeError(f"Unable to initialize Gemini model ({joined})")

    def _ordered_candidates(self) -> Tuple[str, ...]:
        candidates = []
        if self.model_name:
            candidates.append(self.model_name)
        for name in self.model_candidates:
            if name not in candidates:
                candidates.append(name)
        if not candidates:
            candidates.extend(DEFAULT_MODEL_CANDIDATES)
        return tuple(candidates)
