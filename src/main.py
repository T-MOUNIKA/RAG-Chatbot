from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import logging
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='src/static'), name='static')

# Initialize components
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    collection_name=os.getenv('CHROMA_COLLECTION_NAME', 'rag_pdf_collection'),
    embedding_function=embeddings,
    persist_directory=os.getenv('CHROMA_PERSIST_DIR', './chroma_data'),
)
llm = ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o-mini"), temperature=0.0)

# Create prompt template
prompt_template = PromptTemplate(
    template="""Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the provided context, just say "I don't have information about that in the provided documents."
Do not make up an answer or use information outside of the provided context.

Context:
{context}

Question: {question}
Answer:""",
    input_variables=["context", "question"]
)

chain = LLMChain(llm=llm, prompt=prompt_template)

class Query(BaseModel):
    question: str

@app.get('/')
async def index():
    with open('src/static/index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.post('/api/chat')
async def chat(q: Query):
    try:
        logging.info(f"Received question: {q.question}")
        
        # Get relevant documents
        docs = vectorstore.similarity_search(q.question, k=4)
        
        if not docs:
            return {'answer': "I don't have information about that in the provided documents."}
        
        # Combine document content as context
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate response using the chain
        response = chain.run(context=context, question=q.question)
        
        logging.info(f"Generated response: {response}")
        return {'answer': response}
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/health')
async def health():
    return {'status': 'okay'}