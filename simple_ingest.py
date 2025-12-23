import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'rag_pdf_collection')
PERSIST_DIR = os.getenv('CHROMA_PERSIST_DIR', './chroma_data')

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyPDF2"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def ingest_documents():
    """Ingest documents from data folder"""
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Initialize Chroma
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    
    # Process PDF files
    data_dir = Path('./data')
    pdf_files = list(data_dir.glob('*.pdf'))
    
    all_texts = []
    all_metadatas = []
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        text = extract_text_from_pdf(pdf_file)
        
        if text.strip():
            # Split text into chunks
            chunks = text_splitter.split_text(text)
            
            for i, chunk in enumerate(chunks):
                all_texts.append(chunk)
                all_metadatas.append({
                    'source': str(pdf_file),
                    'chunk': i
                })
    
    if all_texts:
        # Add to vectorstore
        vectorstore.add_texts(
            texts=all_texts,
            metadatas=all_metadatas
        )
        print(f"Successfully ingested {len(all_texts)} chunks from {len(pdf_files)} PDF files")
    else:
        print("No text found to ingest")

if __name__ == "__main__":
    ingest_documents()