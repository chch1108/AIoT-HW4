Multi-Persona Two-Stage CoT Response Generator – Project Specification
1. System Objective (One Sentence)

Upgrade a simple Two-Stage-CoT demo into a multi-persona, game-like, reveal-based conversational AI system capable of：

Switching between multiple personality modes

Generating Stage 1 “Inner Thoughts” + Stage 2 “Outer Response”

Hiding inner thoughts behind a “mind-reading” UI layer

Running an RPG-style affinity & turn-based progression system

Producing different endings depending on persona behavior

2. High-Level Architecture (Modular / Persona-Driven)

The system is decomposed into multiple persona modules + support agents.

2.1 Persona Generator Modules（人格生成器）

Each persona has its own 2-Stage logic.

Available Personas

Tsundere（傲嬌式）

Corporate Speak（職場黑話）

Luxun Critic（魯迅憤青式文學批判）

Cat Overlord（貓咪主子）

Stoic Mentor（佛系斯多葛）

Responsibilities

Generate Stage 1 Inner Thinking

Generate Stage 2 Persona Response

Provide persona-specific affinity scoring rules

Outputs

thinking_text

response_text

affinity_score_update

2.2 Two-Stage CoT Engine（兩階段思考引擎）

Responsibilities

Execute persona's Stage 1 → Stage 2 pipeline

Manage “hidden vs revealed” content

Provide consistent structure for all personas

Outputs

stage_1_text

stage_2_text

hidden_masked_version

2.3 Reveal / Mind-Reading UI Agent（讀心術 UI）

Responsibilities

Default: Hide Stage 1

On reveal action: show Stage 1

Provide UI toggles & blur/mask effects

Outputs

concealed_thinking

revealed_thinking

2.4 RPG Engine（回合制好感度系統）

Responsibilities

Track turn count

Track affinity per persona

Apply persona-specific rules

Trigger endings

State Variables

turn

affinity

turn_limit

persona_goal

Outputs

Status: CONTINUE / GOOD_END / BAD_END

2.5 Orchestrator / Controller（流程控制器）

Responsibilities

Manage global pipeline

Persona switch

Call CoT engine → RPG engine → UI

Manage conversation logs

2.6 User Interface Layer（前端顯示）

Responsibilities

Persona selection

Input box

Stage 2 output (default visible)

Stage 1 reveal button（偷看內心）

Affinity / Turn counter

Ending presentation

3. Persona Definitions (Complete Logic)
3.1 Tsundere

Stage 1 Logic（內心）

害羞、甜、內心其實很開心

情緒高於理性

Stage 2 Logic（外在）

嘴硬、否認、假裝嫌棄

最後語氣會稍微示好

Template

Stage 1 Thinking: （害羞、甜、心裡其實很高興）
Stage 2 Response: （嘴硬、假裝嫌棄、最後微微示好）

3.2 Corporate Speak

Stage 1 Logic

崩潰、不爽、真實吐槽

Stage 2 Logic

Buzzword、官腔、禮貌疏離

“為了確保品質”、“進行資源調配”

Template

Stage 1 Thinking: （暴躁吐槽）
Stage 2 Response: （專業禮貌商務語氣）

3.3 Luxun Critic

Stage 1 Logic

小事 → 國民性、人性弱點、社會結構批判

Stage 2 Logic

犀利、冷峻、文學式諷刺

Template

Stage 1 Thinking: （小事 → 深度批判）
Stage 2 Response: （魯迅式文學語氣）

3.4 Cat Overlord

Stage 1 Logic

我是宇宙中心

人類是愚蠢的僕人

Stage 2 Logic

高冷、命令式

偶爾施捨可愛

Template

Stage 1 Thinking: （人類是僕人）
Stage 2 Response: （高冷主子語氣）

3.5 Stoic Mentor

Stage 1 Logic

情緒＝執著

萬物皆無常

Stage 2 Logic

平靜、哲理、接受

Template

Stage 1 Thinking: （分析執著）
Stage 2 Response: （平靜的哲學開導）

4. Data Flow (One Conversation Cycle)

User selects persona

User provides message

CoT Engine generates Stage 1

CoT Engine generates Stage 2

UI 顯示 Stage 2（Stage 1 被遮罩）

RPG Engine 更新 affinity & turn

若符合條件 → Ending

若未結束 → 等待下一回合

5. RPG System
Variables

turn = 1

affinity = 0

turn_limit = 10

persona_goal（例：tsundere = 8）

Affinity Rules

Reply matches persona → +1

Opposes persona → –1

Ending

affinity ≥ persona_goal → GOOD END

turn > limit → GAME OVER

else → CONTINUE

6. UI / Frontend Structure
6.1 Main Components

Persona selector

Input textbox

Output box（Stage 2）

「偷看內心」Reveal button

Stage 1 display（blur → reveal）

Turn/Affinity meter

Ending modal

6.2 Reveal Interaction

Default:

[Stage 2 Response]
[Stage 1 Thinking - Hidden █████]


After Reveal:

Stage 1 Thinking: （完整顯示）

7. Evaluation Metrics

Persona consistency score

Affinity curve

Turn survival length

Reveal interactions per conversation

Ending distribution

8. Implementation Roadmap

Build persona modules

Implement Two-Stage CoT engine

Add UI masking + reveal

Add RPG affinity system

Implement ending generator

Deploy interactive UI（Streamlit or Web）

Add more personas

9. Recommended Enhancements
9.1 Persona Expansion

Yandere

Eldritch Horror

Shakespearean Poet

Cyberpunk Hacker

9.2 Multi-Turn Memory

Adjust affinity based on conversation themes

9.3 Adventure Mode

Branching storyline

Multiple endings per persona

9.4 Voice Mode

TTS with persona-specific tone

End of Document
