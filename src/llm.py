from langchain_openai import ChatOpenAI
import os

def get_llm():
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature=0.0,
        max_retries=3
    )
    return llm

