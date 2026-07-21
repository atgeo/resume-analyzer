from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def get_llm():
    return ChatOpenAI(
        model="gpt-5-mini",
        temperature=0,
    )

def get_embedding_model():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
    )
