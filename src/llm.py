from langchain_openai import ChatOpenAI

def get_llm():
    llm = ChatOpenAI(
        api_key="xyz",
        model="gpt-5-nano-2025-08-07",  # free tier friendly model
        temperature=0.0,
        max_retries=3
    )

