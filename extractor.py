from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

from llm import get_llm
from models import ResumeSummary

llm = get_llm()


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
