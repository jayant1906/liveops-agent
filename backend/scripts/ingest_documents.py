from __future__ import annotations

import argparse
import hashlib
import json
import re
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_KNOWLEDGE_BASE_PATH = Path(__file__).resolve().parents[2] / "knowledge_base"
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "knowledge_chunks.jsonl"
DEFAULT_CHUNK_SIZE = 180
DEFAULT_CHUNK_OVERLAP = 35



@dataclass(frozen=True)
class SourceDocument:
    path: Path
    category: str
    title: str
    raw_text: str


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    source_path: str
    category: str
    title: str
    chunk_index: int
    text: str
    section: str | None

class EmptyFileError(Exception):
    pass

def load_documents(knowledge_base_path: Path) -> list[SourceDocument]:
    list_files = []
    for files in knowledge_base_path.rglob("*.md"):
        file_path = Path(files).resolve()
        file_category = Path(files).resolve().parents[0].name
        with file_path.open("r", encoding="utf-8") as file:
            file_raw_text = file.read()
            if not file_raw_text.strip():
                raise EmptyFileError(f"Empty knowledge base document: {file_path}")
            file_title = file_path.stem
            for line in file_raw_text.splitlines():
                if re.match(r"^#+\s+", line.strip()):
                    file_title = re.sub(r"^#+\s*", "", line.strip())
                    break
        list_files.append(SourceDocument(file_path, file_category, file_title, file_raw_text))
    return list_files


def clean_document(raw_text: str) -> str:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # 1. Collapse multiple spaces/tabs within lines into a single space
    text = re.sub(r'[ \t]+', ' ', text)

    # 2. Collapse 3+ newlines (i.e. 2+ blank lines) down to a single blank line
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 3. Strip leading/trailing whitespace from the whole document
    text = text.strip()
    return text


def chunk_document(cleaned_text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, 
                   chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,) -> list[str]:
    # TODO
    pass


def add_metadata(chunk: str, source_document: SourceDocument, chunk_index: int, 
                 knowledge_base_path: Path,) -> DocumentChunk:
    # TODO
    pass


def write_chunks(chunks: Iterable[DocumentChunk], output_path: Path) -> int:
    # TODO
    pass


def stable_id(value: str) -> str:
    # TODO
    pass


def parse_args() -> argparse.Namespace:
    # TODO
    pass


def ingest_documents(knowledge_base_path: Path,output_path: Path,chunk_size: int = DEFAULT_CHUNK_SIZE,
                     chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,) -> int:
    # TODO
    pass


def main() -> None:
    # TODO
    pass


if __name__ == "__main__":
    main()
