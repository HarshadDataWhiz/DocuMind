from fastapi import FastAPI, Query
from app.pdfLoader import load_pages
from app.vectorStore import vectorStore
from app.chain import Chain
from pathlib import Path
import os

app = FastAPI()

# Global variable to store vector stores
vs_store_dict = {}

def create_store(folder_loc=os.path.join(os.curdir, 'data', 'Documents')):
    vs_store_dict_local = {}
    for filepath in Path(folder_loc).glob("*.pdf"):
        document_pages = load_pages(filepath)
        # splitting
        document_pages_split = vectorStore.split_text(document_pages)
        # creating the vector store
        vs_store_dict_local[filepath.name] = vectorStore.create_vector_store(document_pages_split)
    return vs_store_dict_local

def answer_pipeline(question: str, filename: str):
    pages_data = vectorStore.search(question, vs_store_dict[filename])
    chain = Chain()
    answer = chain.get_answer(question=question, docs_data=pages_data)
    return answer

# Load vector store only once at startup
@app.on_event("startup")
def startup_event():
    global vs_store_dict
    vs_store_dict = create_store()
    print("Vector store created at startup ✅")

@app.get("/ask")
def ask_question(question: str = Query(..., description="User's question"),
                 filename: str = Query(..., description="PDF filename to search in")):
    if filename not in vs_store_dict:
        return {"error": f"Filename '{filename}' not found"}
    answer = answer_pipeline(question, filename)
    return {"filename": filename, "question": question, "answer": answer}
