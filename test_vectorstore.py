import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def test_vectorstore():
    embeddings = OpenAIEmbeddings()
    
    vectorstore = Chroma(
        collection_name='rag_pdf_collection',
        embedding_function=embeddings,
        persist_directory='./chroma_data',
    )
    
    # Test search
    results = vectorstore.similarity_search("Docker", k=3)
    print(f"Found {len(results)} results for 'Docker':")
    for i, doc in enumerate(results):
        print(f"Result {i+1}: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")
        print("---")

if __name__ == "__main__":
    test_vectorstore()