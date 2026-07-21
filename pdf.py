from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import typer


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
        raise typer.BadParameter("File is not a valid PDF.")
