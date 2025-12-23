import os
from src.retriever import build_retriever, build_qa_chain
from dotenv import load_dotenv

load_dotenv()

def test_retrieval():
    try:
        # Test retriever
        retriever = build_retriever()
        docs = retriever.get_relevant_documents("What is Docker?")
        print(f"Found {len(docs)} documents")
        for i, doc in enumerate(docs):
            print(f"Doc {i+1}: {doc.page_content[:200]}...")
        
        # Test QA chain
        qa = build_qa_chain()
        result = qa.run("What is Docker?")
        print(f"\nQA Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_retrieval()