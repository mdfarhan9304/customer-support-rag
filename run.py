"""Test script: verify document loading + chunking for files in uploads/."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.rag.ingestion import chunk_documents, load_documents


def preview(text: str, n: int = 120) -> str:
    return text[:n].replace("\n", " ") + ("..." if len(text) > n else "")


def main() -> None:
    uploads_dir = Path(__file__).parent / "uploads"
    files = [
        p for p in uploads_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {".txt", ".md", ".pdf", ".docx"}
    ]

    if not files:
        print("No supported files found in uploads/")
        sys.exit(1)

    # show first chunk of each file
    for file_path in files:
        docs = load_documents(file_path)
        chunks = chunk_documents(docs)
        print(f"\nFirst chunk of {file_path.name}:")
        print(f"Chunk size: {len(chunks[3].page_content)} characters")
        print(chunks[3].page_content)
        print("-" * 70)

    # for file_path in files:
    #     print(f"\n{'=' * 70}")
    #     print(f"FILE: {file_path.name}")
    #     print(f"{'=' * 70}")

    #     try:
    #         docs = load_documents(file_path)
    #     except Exception as e:
    #         print(f"  LOAD FAILED: {e}")
    #         continue

    #     print(f"Loaded {len(docs)} document(s)")

    #     chunks = chunk_documents(docs)
    #     sizes = [len(c.page_content) for c in chunks]

    #     print(f"Chunked into {len(chunks)} chunks")
    #     print(f"Chunk size stats: min={min(sizes)}, max={max(sizes)}, avg={sum(sizes) // len(sizes)}")

    #     print("\nFirst 3 chunks:")
    #     for i, chunk in enumerate(chunks[:3]):
    #         start = chunk.metadata.get("start_index")
    #         print(f"  [{i}] size={sizes[i]} start_index={start} | {preview(chunk.page_content)}")

    #     if len(chunks) > 3:
    #         i = len(chunks) - 1
    #         print(f"  ... last chunk:")
    #         print(f"  [{i}] size={sizes[i]} start_index={chunks[i].metadata.get('start_index')} | {preview(chunks[i].page_content)}")

    #     # Sanity checks
    #     assert all(s <= 900 for s in sizes), "Found chunk exceeding chunk_size=900"
    #     total_doc_chars = sum(len(d.page_content) for d in docs)
    #     total_chunk_chars = sum(sizes)
    #     print(f"\nTotal chars: docs={total_doc_chars}, chunks={total_chunk_chars} "
    #           f"(overlap accounts for difference)")
    #     print("PASS: all chunks within chunk_size=900")


if __name__ == "__main__":
    main()
