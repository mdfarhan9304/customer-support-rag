# LangGraph FastAPI service

## Setup

Use Python 3.12 or 3.13. The pinned Pinecone/LangChain integration does not
support Python 3.14 yet.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `GET /health`

Add provider credentials to `.env` only for integrations you intend to use. The `.env` file is ignored by Git.

## OpenAI with LangChain

Set these values in a local `.env` file:

```dotenv
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-5-mini
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=langraph-kb
PINECONE_NAMESPACE=default
PINECONE_TEXT_FIELD=chunk_text
PINECONE_TITLE_FIELD=title
```

`POST /chat` uses `langchain_openai.ChatOpenAI` and calls the OpenAI API with
`OPENAI_API_KEY`. The configured default model is `gpt-5-mini`.

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Explain LangGraph in one sentence."}'
```

## Ingest the sample knowledge base

The `langraph-kb` index is a Pinecone document-schema index. Pinecone embeds its
`chunk_text` field with the model configured on the index, so the application
upserts documents rather than manually generated OpenAI vectors.

```bash
python ingest_sample_kb.py
```

The script splits the sample text into overlapping chunks, creates matching OpenAI
embeddings, and upserts those chunks into the configured Pinecone index.
