from pathlib import Path

import typer
from typing import Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from models import ResumeSummary

load_dotenv()

app = typer.Typer()

PERSIST_DIR = "./chroma_db"

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0,
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


def load_file(filename: Path) -> PdfReader:
    if not filename.exists():
        raise typer.BadParameter("File does not exist.")

    if not filename.is_file():
        raise typer.BadParameter("Not a file.")

    if filename.suffix.lower() != ".pdf":
        raise typer.BadParameter("Please provide a PDF file.")

    try:
        return PdfReader(filename)
    except PdfReadError:
        raise typer.BadParameter("Error: The file is not a valid PDF.")


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


prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
You must answer ONLY using the provided context.

If the answer cannot be determined from the context,
reply exactly:
"I don't know based on the provided context."

Do not use your own knowledge.

Context:
{context}
"""
     ),
    ("human", "{question}")
])


def answer(vector_store: Chroma, query: str) -> str:
    docs = vector_store.similarity_search(query, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    messages = prompt.invoke({
        "context": context,
        "question": query,
    })

    response = llm.invoke(messages)
    return response.content


def extract_resume(vector_store: Chroma) -> ResumeSummary:
    structured_llm = llm.with_structured_output(ResumeSummary)

    docs = vector_store.similarity_search(
        "resume contact information employment history",
        k=5,
    )

    context = "\n\n".join(doc.page_content for doc in docs)

    messages = ChatPromptTemplate.from_messages([
        (
            "system",
            """
Extract the requested fields from the provided resume.

If a value cannot be determined, infer nothing.
Return only the structured data.

Context:
{context}
"""
        )
    ]).invoke({"context": context})

    return structured_llm.invoke(messages)


@app.command()
def ask(
        pdf: Path,
        query: Annotated[str, typer.Option()],
):
    vector_store = build_vector_store(pdf)

    reply = answer(vector_store, query)

    print(reply)


@app.command()
def extract(
        pdf: Path
):
    vector_store = build_vector_store(pdf)

    summary = extract_resume(vector_store)

    with open("resume.json", "w", encoding="utf-8") as f:
        f.write(summary.model_dump_json(indent=2))

    typer.echo("Saved to resume.json")


if __name__ == "__main__":
    app()
