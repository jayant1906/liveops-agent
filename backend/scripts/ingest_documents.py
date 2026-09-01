from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_KNOWLEDGE_BASE_PATH = Path(__file__).resolve().parents[2] / "knowledge_base"
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "knowledge_chunks.jsonl"
DEFAULT_CHUNK_SIZE = 50
DEFAULT_CHUNK_OVERLAP = 5



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


def word_count(text):
    return len(text.split())

def chunk_document(cleaned_text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, 
                   chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,) -> list[str]:
    
    # Matches lines starting with 1-6 '#' characters
    pattern = r'^(#{1,6}\s+.+)$'
    lines = cleaned_text.split('\n')

    sections = []
    current_content = []
    
    for line in lines:
        if re.match(pattern, line):
            if current_content:
                sections.append('\n'.join(current_content).strip())
            current_content = [line]
        else:
            current_content.append(line)
    if current_content:
        sections.append('\n'.join(current_content).strip())
    
    final = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=word_count,
        separators=["\n\n", "\n", " ", ""],
    )
    for elem in sections:
        final += text_splitter.split_text(elem)

    return final


def add_metadata(chunk: str, source_document: SourceDocument, chunk_index: int, 
                 knowledge_base_path: Path,) -> DocumentChunk:
    source_path = str(source_document.path.relative_to(knowledge_base_path))
    document_id = stable_id(source_path)
    chunk_id = stable_id(f"{document_id}:{chunk_index}:{chunk}")

    section = None
    first_line = chunk.splitlines()[0] if chunk.splitlines() else ""
    if first_line.startswith("#"):
        section = first_line.lstrip("#").strip()

    return DocumentChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        source_path=source_path,
        category=source_document.category,
        title=source_document.title,
        chunk_index=chunk_index,
        text=chunk,
        section=section,
    )


def write_chunks(chunks: Iterable[DocumentChunk], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    counter = 0

    with output_path.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            json.dump(asdict(chunk), file)
            file.write("\n")
            counter += 1

    return counter


def stable_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest markdown knowledge base documents into JSONL chunks."
    )
    parser.add_argument(
        "--knowledge-base-path",
        type=Path,
        default=DEFAULT_KNOWLEDGE_BASE_PATH,
        help="Directory containing markdown knowledge base documents.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path to write JSONL document chunks.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help="Maximum chunk size in words.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=DEFAULT_CHUNK_OVERLAP,
        help="Chunk overlap in words.",
    )
    return parser.parse_args()


def ingest_documents(
    knowledge_base_path: Path,
    output_path: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> int:
    knowledge_base_path = knowledge_base_path.resolve()
    output_path = output_path.resolve()
    chunks = []

    for source_document in load_documents(knowledge_base_path):
        cleaned_text = clean_document(source_document.raw_text)
        document_chunks = chunk_document(cleaned_text, chunk_size, chunk_overlap)

        for chunk_index, chunk in enumerate(document_chunks):
            chunks.append(
                add_metadata(
                    chunk=chunk,
                    source_document=source_document,
                    chunk_index=chunk_index,
                    knowledge_base_path=knowledge_base_path,
                )
            )

    return write_chunks(chunks, output_path)


def main() -> None:
    args = parse_args()
    chunk_count = ingest_documents(
        knowledge_base_path=args.knowledge_base_path,
        output_path=args.output_path,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    print(f"Wrote {chunk_count} chunks to {args.output_path}")


if __name__ == "__main__":
    main()
