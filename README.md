# Resume Analyzer

A lightweight CLI tool for querying and extracting structured information from PDF resumes using RAG (Retrieval-Augmented Generation).

## Features

- **Ask**: Chat with a resume using natural language queries.
- **Extract**: Automatically extract key resume data into `resume.json`.

## Installation

```bash
uv sync
```

## Commands

| Command     | Description                              | Usage Example |
|-------------|------------------------------------------|---------------|
| `ask`       | Ask questions about the resume           | `python main.py ask resume.pdf --query "What is the candidate's last job?"` |
| `extract`   | Extract structured resume to JSON        | `python main.py extract resume.pdf` |
