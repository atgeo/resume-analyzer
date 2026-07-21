from pathlib import Path
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from llm import get_embedding_model
from pdf import load_file

embeddings = get_embedding_model()


def build_vector_store(filename: Path) -> Chroma:
    reader = load_file(filename)

    retrieved_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            retrieved_text += text + "\n"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_text(retrieved_text)

    return Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
    )
