from pathlib import Path
from typing import Iterable
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from docx import Document as DocxDocument


SUPPORTED_FILE_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}


class DocxLoader:
    """Minimal .docx loader producing one Document per paragraph."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self) -> list[Document]:
        doc = DocxDocument(self.file_path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        metadata = {"source": str(self.file_path)}
        return [Document(page_content=text, metadata=metadata)]


def load_documents(file_path: Path) -> Iterable[Document]:
    suffix = file_path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return TextLoader(file_path).load()
    elif suffix == ".pdf":
        return PyPDFLoader(file_path).load()
    elif suffix == ".docx":
        return DocxLoader(file_path).load()
    else:
        raise ValueError(f"Unsupported file extension: {suffix}")


def chunk_documents(docs: Iterable[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900, chunk_overlap=120, add_start_index=True
    )
    return splitter.split_documents(list(docs))
