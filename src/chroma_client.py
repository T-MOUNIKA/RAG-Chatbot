import os
import chromadb

CHROMA_DIR = os.getenv('CHROMA_PERSIST_DIR', '/app/chroma_data')

def get_chroma_client(persist_directory=None):
    persist_directory = persist_directory or CHROMA_DIR
    # Only the path parameter is necessary for local persistence
    client = chromadb.PersistentClient(path=persist_directory)
    return client

def get_or_create_collection(name, embedding_function=None, persist_directory=None):
    client = get_chroma_client(persist_directory)
    try:
        collection = client.get_collection(name)
    except Exception:
        collection = client.create_collection(name=name, embedding_function=embedding_function)
    return collection
