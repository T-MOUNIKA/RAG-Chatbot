import os
from langchain.chains import RetrievalQA
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate


COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'rag_pdf_collection')
PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', './chroma_data')

# Custom prompt template to restrict answers to document content
CUSTOM_PROMPT = PromptTemplate(
    template="""Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the provided context, just say "I don't have information about that in the provided documents."
Do not make up an answer or use information outside of the provided context.

Context:
{context}

Question: {question}
Answer:""",
    input_variables=["context", "question"]
)

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

def build_qa_chain():
    llm = ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o-mini"), temperature=0.0)
    retriever = build_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever,
        chain_type_kwargs={"prompt": CUSTOM_PROMPT}
    )
    return qa