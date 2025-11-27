from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.retriever import build_qa_chain
from src.llm import get_llm
from src.chroma_client import get_or_create_collection
from src.utils import split_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='src/static'), name='static')

qa = build_qa_chain()

class Query(BaseModel):
    question: str

@app.get('/')
async def index():
    with open('src/static/index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.post('/api/chat')
async def chat(q: Query):
    res = qa.run(q.question)
    return {'answer': res}

@app.get('/health')
async def health():
    return {'status': 'okay'}