Debate AI
=========

Debate AI runs a FastAPI backend and a Streamlit client that asks two AI
debaters to argue a topic, judge the result, and summarize supporting evidence.

Setup
-----

Create a `.env` file in the project root:

```env
APP_NAME="Debate AI API"
APP_VERSION="0.1.0"
GROQ_API_KEY="your-groq-key"
GROQ_MODEL="openai/gpt-oss-20b"
TRAVILY_API_KEY="your-tavily-key"
```

Install dependencies:

```bash
uv sync
```

Run the API:

```bash
uv run uvicorn server.src.main:app --reload
```

Run the Streamlit client in a second terminal:

```bash
uv run streamlit run client.py
```

The client posts to `http://127.0.0.1:8000/api/v1/debate`.
