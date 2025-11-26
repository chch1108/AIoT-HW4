"""Streamlit front-end for the AIoT HW4 multi-persona CoT demo."""

from __future__ import annotations

import os

import streamlit as st

from aiot_hw4 import ConversationOrchestrator, PERSONA_REGISTRY, LLMClient

DISPLAY_LABELS = {
    "Tsundere": "傲嬌式",
    "Corporate Speak": "職場黑話",
    "Luxun Critic": "魯迅：憤青式",
    "Cat Overlord": "貓咪主子",
    "Stoic Mentor": "佛系：斯多葛",
}

st.set_page_config(
    page_title="AIoT HW4 – Multi-Persona CoT",
    page_icon="⭐️",
    layout="centered",
)


def init_state() -> None:
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = ConversationOrchestrator()


def get_genai_key() -> str | None:
    if "GENAI_API_KEY" in st.secrets:
        return st.secrets["GENAI_API_KEY"]
    return os.environ.get("GENAI_API_KEY")


def get_genai_model_name() -> str:
    if "GENAI_MODEL_NAME" in st.secrets:
        return st.secrets["GENAI_MODEL_NAME"]
    return os.environ.get("GENAI_MODEL_NAME", "gemini-1.5-flash")


def sync_llm_client() -> None:
    api_key = get_genai_key()
    model_name = get_genai_model_name()
    current_key = st.session_state.get("llm_api_key")
    llm_client = st.session_state.get("llm_client")
    if api_key and api_key == current_key and llm_client:
        st.session_state.llm_error = None
        st.session_state.orchestrator.set_llm_client(llm_client)
        return
    if not api_key:
        st.session_state.llm_client = None
        st.session_state.llm_api_key = None
        st.session_state.llm_error = None
        st.session_state.orchestrator.set_llm_client(None)
        return
    try:
        llm_client = LLMClient(api_key=api_key, model_name=model_name)
        st.session_state.llm_client = llm_client
        st.session_state.llm_api_key = api_key
        st.session_state.llm_error = None
    except Exception as exc:  # pragma: no cover - depends on remote API
        st.session_state.llm_client = None
        st.session_state.llm_api_key = None
        st.session_state.llm_error = str(exc)
    st.session_state.orchestrator.set_llm_client(st.session_state.llm_client)


init_state()
sync_llm_client()
orchestrator: ConversationOrchestrator = st.session_state.orchestrator
llm_client: LLMClient | None = st.session_state.get("llm_client")

st.title("Multi-Persona Two-Stage CoT Playground")
st.caption("完成傲嬌、社畜、魯迅、貓主子與斯多葛導師等五種人格的兩階段演算。")

llm_error = st.session_state.get("llm_error")
if llm_client:
    st.success(f"LLM 模式啟用：{llm_client.model_name}")
elif get_genai_key():
    st.warning("偵測到 GENAI_API_KEY 但初始化失敗，改用模板回覆。")
else:
    st.info("尚未設定 GENAI_API_KEY，使用內建模板產生回答。")

if llm_error:
    st.warning(f"LLM 初始化錯誤：{llm_error}")
elif orchestrator.last_llm_error:
    st.warning(f"LLM 回覆失敗，已改用模板：{orchestrator.last_llm_error}")

persona_names = list(PERSONA_REGISTRY.keys())
display_names = [DISPLAY_LABELS.get(name, name) for name in persona_names]
current_idx = persona_names.index(orchestrator.persona.name)
selected_display = st.selectbox(
    "選擇人格 persona",
    display_names,
    index=current_idx,
)
display_to_persona = {display: name for display, name in zip(display_names, persona_names)}
selected_persona = display_to_persona[selected_display]

def safe_rerun() -> None:
    """Use new Streamlit rerun API while keeping compatibility."""
    if hasattr(st, "rerun"):
        st.rerun()  # type: ignore[attr-defined]
    else:  # pragma: no cover
        st.experimental_rerun()


if selected_persona != orchestrator.persona.name:
    orchestrator.switch_persona(selected_persona)
    safe_rerun()

st.info(
    f"{orchestrator.persona.description}｜好感目標 {orchestrator.persona.persona_goal}，"
    "回合上限 10。"
)

with st.form("chat-form", clear_on_submit=True):
    user_message = st.text_input("輸入訊息", placeholder="丟出你的提問或攏絡台詞…")
    submitted = st.form_submit_button("送出")
    if submitted and user_message.strip():
        orchestrator.run_turn(user_message.strip())
        safe_rerun()

state = orchestrator.state

col_turn, col_affinity, col_status = st.columns(3)
col_turn.metric("回合", f"{state.turn}/10")
col_affinity.metric("好感", state.affinity)
col_status.metric("狀態", state.status)

if state.ending_text:
    st.success(state.ending_text)

st.subheader("對話紀錄")

if not state.history:
    st.write("尚未開始，輸入訊息後就能偷看角色腦內劇場！")
else:
    for turn in reversed(state.history):
        with st.container():
            st.markdown(f"**Turn {turn.idx} – {turn.persona}**")
            st.markdown(f"`You:` {turn.user_message}")
            st.markdown(f"**Stage 2 Response**: {turn.stage2}")
            if turn.revealed:
                st.markdown(f"**Stage 1 Thinking**: {turn.stage1}")
            else:
                reveal = st.button("偷看內心", key=f"reveal_{turn.idx}")
                if reveal:
                    orchestrator.reveal_turn(turn.idx)
                    safe_rerun()
                st.markdown(f"**Stage 1 Thinking**: {turn.masked_stage1}")
            st.caption(f"好感變化：{turn.affinity_delta:+d}")
            st.divider()

st.caption(
    "提示：持續與人格互動累積好感，達成 persona 專屬門檻即可解鎖 Good End！"
)
