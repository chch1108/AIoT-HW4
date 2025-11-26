"""Streamlit front-end for the AIoT HW4 multi-persona CoT demo."""

from __future__ import annotations

import streamlit as st

from aiot_hw4 import ConversationOrchestrator, PERSONA_REGISTRY

st.set_page_config(
    page_title="AIoT HW4 – Multi-Persona CoT",
    page_icon="⭐️",
    layout="centered",
)


def init_state() -> None:
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = ConversationOrchestrator()


init_state()
orchestrator: ConversationOrchestrator = st.session_state.orchestrator

st.title("Multi-Persona Two-Stage CoT Playground")
st.caption("完成傲嬌、社畜、魯迅、貓主子與斯多葛導師等五種人格的兩階段演算。")

persona_names = list(PERSONA_REGISTRY.keys())
current_idx = persona_names.index(orchestrator.persona.name)
selected_persona = st.selectbox(
    "選擇人格 persona",
    persona_names,
    index=current_idx,
)

if selected_persona != orchestrator.persona.name:
    orchestrator.switch_persona(selected_persona)
    st.experimental_rerun()

st.info(
    f"{orchestrator.persona.description}｜好感目標 {orchestrator.persona.persona_goal}，"
    "回合上限 10。"
)

with st.form("chat-form", clear_on_submit=True):
    user_message = st.text_input("輸入訊息", placeholder="丟出你的提問或攏絡台詞…")
    submitted = st.form_submit_button("送出")
    if submitted and user_message.strip():
        orchestrator.run_turn(user_message.strip())
        st.experimental_rerun()

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
                    st.experimental_rerun()
                st.markdown(f"**Stage 1 Thinking**: {turn.masked_stage1}")
            st.caption(f"好感變化：{turn.affinity_delta:+d}")
            st.divider()

st.caption(
    "提示：持續與人格互動累積好感，達成 persona 專屬門檻即可解鎖 Good End！"
)
