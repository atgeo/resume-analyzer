import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def get_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        temperature=0,
    )


def get_embedding_model():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
    )
