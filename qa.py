from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from llm import get_llm

llm = get_llm()

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
