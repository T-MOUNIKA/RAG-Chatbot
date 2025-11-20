import os
from pathlib import Path
from langchain.document_loaders import PyPDFLoader, TextLoader, CSVLoader, UnstructuredFileLoader
from langchain.embeddings import OpenAIEmbeddings
from src.chroma_client import get_or_create_collection
from src.utils import split_text

def ingest_folder(data_dir='./data', collection_name=None, persist_dir=None):
    collection_name = collection_name or os.getenv('CHROMA_COLLECTION_NAME', 'rag_pdf_collection')
    persist_dir = persist_dir or os.getenv('CHROMA_PERSIST_DIR', '/app/chroma_data')

    embeddings = OpenAIEmbeddings()
    collection = get_or_create_collection(collection_name, embedding_function=None, persist_directory=persist_dir)

    files = list(Path(data_dir).glob('**/*'))
    doc_id = 0
    for f in files:
        if f.is_dir():
            continue
        suffix = f.suffix.lower()
        loader = None
        try:
            if suffix == '.pdf':
                loader = PyPDFLoader(str(f))
            elif suffix in ['.txt']:
                loader = TextLoader(str(f))
            elif suffix in ['.csv']:
                loader = CSVLoader(str(f))
            else:
                loader = UnstructuredFileLoader(str(f))
        except Exception as e:
            print(f'Skipping {f}: {e}')
            continue

        docs = loader.load()
        for d in docs:
            chunks = split_text(d.page_content)
            for chunk in chunks:
                emb = embeddings.embed_documents([chunk])[0]
                collection.add(
                    documents=[chunk],
                    metadatas=[{'source': str(f)}],
                    ids=[f'{f.name}-{doc_id}'],
                    embeddings=[emb]
                )
                doc_id += 1
    print('Ingestion complete')

if __name__ == '__main__':
    ingest_folder()