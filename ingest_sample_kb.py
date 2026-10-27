"""Ingest a small sample knowledge-base document into Pinecone."""

from app.rag.ingestion import ingest_text


SAMPLE_TEXT = """
LangGraph is a framework for building stateful, multi-step AI applications.
It models workflows as graphs where nodes perform work and edges control flow.
Knowledge-base documents are split into overlapping chunks, embedded as vectors,
and stored in Pinecone so relevant context can be retrieved for a user question.
""".strip()


if __name__ == "__main__":
    chunk_count = ingest_text(SAMPLE_TEXT, source="sample-knowledge-base")
    print(f"Successfully ingested {chunk_count} chunk(s) into Pinecone.")
