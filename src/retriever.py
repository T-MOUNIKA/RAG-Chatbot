import os
from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'rag_pdf_collection')
PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', '/app/chroma_data')

def build_retriever(k=4):
    # Initialize your embedding function
    embeddings = OpenAIEmbeddings()

    # Create or connect to a chroma vectorstore using LangChain wrapper
    vectordb = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    
    # Create retriever with top-k results
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    return retriever

# def build_qa_chain():
#     llm = ChatOpenAI(model_name=os.getenv("LLM_MODEL", "gpt-4o-mini"), temperature=0.0)
#     retriever = build_retriever()
#     qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
#     return qa
def build_qa_chain():
    llm = ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-5-nano-2025-08-07"), temperature=0.0)
    retriever = build_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa