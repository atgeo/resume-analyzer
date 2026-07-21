from dotenv import load_dotenv

load_dotenv()

from qa import answer
from extractor import extract_resume
from pathlib import Path
import typer
from typing import Annotated
from rag import build_vector_store

app = typer.Typer()


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
