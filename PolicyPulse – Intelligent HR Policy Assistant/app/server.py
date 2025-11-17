# app/server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from app.rag_chain import generate_answer, clear_memory, get_memory

app = FastAPI(title="PolicyPulse API")

class Query(BaseModel):
    user: str
    question: str

@app.post("/ask")
def ask_question(query: Query):
    if not query.user:
        raise HTTPException(status_code=400, detail="user field required")
    answer, sources = generate_answer(query.user, query.question)
    return {"answer": answer, "sources": sources}

class UserObj(BaseModel):
    user: str

@app.post("/memory/clear")
def api_clear_memory(u: UserObj):
    clear_memory(u.user)
    return {"status": "ok", "message": f"Memory cleared for user {u.user}"}

@app.post("/memory/view")
def api_view_memory(u: UserObj):
    mem = get_memory(u.user)
    return {"status": "ok", "memory": mem}
