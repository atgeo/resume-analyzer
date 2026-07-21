from dotenv import load_dotenv

load_dotenv()

from qa import answer
from extractor import extract_resume
from pathlib import Path
import typer
from typing import Annotated
from rag import build_vector_store

app = typer.Typer()

PdfPath = Annotated[
    Path,
    typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True, help="Path to the resume PDF."),
]


@app.command()
def ask(
        pdf: PdfPath,
        query: Annotated[str, typer.Option()],
):
    vector_store = build_vector_store(pdf)

    reply = answer(vector_store, query)

    print(reply)


@app.command()
def extract(
        pdf: PdfPath
):
    vector_store = build_vector_store(pdf)

    summary = extract_resume(vector_store)

    with open("resume.json", "w", encoding="utf-8") as f:
        f.write(summary.model_dump_json(indent=2))

    typer.echo("Saved to resume.json")


if __name__ == "__main__":
    app()
