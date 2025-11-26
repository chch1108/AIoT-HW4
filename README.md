# AIoT HW4 – Multi-Persona Two-Stage CoT Response Generator

This project follows the HW4 specification to build a small, game-like conversational AI playground. It implements:

- Five persona modules (Tsundere, Corporate Speak, Luxun Critic, Cat Overlord, Stoic Mentor)
- Two-stage Chain-of-Thought (inner Stage 1 + outer Stage 2)
- Reveal UI that masks Stage 1 thoughts until the user presses **偷看內心**
- RPG-style affinity engine with goals, turn limits, and Good/Bad endings
- Streamlit front-end for persona switching, logging, and ending presentation

## Project Structure

```
.
├── aiot_hw4/
│   ├── __init__.py
│   ├── engines.py        # Two-Stage CoT + RPG engines
│   ├── orchestrator.py   # Flow controller & conversation state
│   └── personas.py       # Persona modules + scoring rules
├── app.py                # Streamlit UI
├── project.md            # Original specification
├── README.md             # You are here
└── requirements.txt      # Streamlit dependency list
```

## Running the demo

```bash
pip install -r requirements.txt
streamlit run app.py
```

Once the browser UI opens:

1. Pick a persona from the selector.
2. Type your line in the input box and send.
3. Read the persona's Stage 2 response and optionally click **偷看內心** to reveal Stage 1.
4. Watch the turn counter, affinity progress, and endings triggered by persona-specific goals.

Have fun mind-reading the characters while surviving the 10-turn limit!

## Enabling LLM mode

The default gameplay uses hand-written templates, but you can hook it up to Google Gemini for richer persona replies:

1. Obtain a Google Generative AI key and set `GENAI_API_KEY` in Streamlit secrets (or as an environment variable locally).
2. (Optional) Set `GENAI_MODEL_NAME` if you want a different Gemini variant. It defaults to `gemini-1.5-flash`.
3. Deploy/run the app again—when the key loads successfully the UI will show “LLM 模式啟用…”.

If the key is missing or the API call fails, the orchestrator automatically falls back to the built-in templates so the experience keeps working.
