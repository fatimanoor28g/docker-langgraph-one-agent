"""FastAPI: website + health + chat + saved tickets."""
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from .database import init_db, list_tickets
from .graph import graph

WEB_PAGE = Path(__file__).resolve().parent.parent / "web" / "index.html"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Docker + LangGraph Classroom Demo", lifespan=lifespan)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=1000)


@app.get("/")
def homepage():
    return FileResponse(WEB_PAGE)


@app.get("/health")
def health():
    return {"status": "ok", "service": "langgraph-university-agent"}


@app.post("/chat")
def chat(request: ChatRequest):
    result = graph.invoke(
        {"messages": [HumanMessage(content=request.message)]},
        config={"configurable": {"thread_id": request.session_id}},
    )
    answer = result["messages"][-1].content
    return {"session_id": request.session_id, "answer": answer}


@app.get("/tickets")
def tickets():
    return {"tickets": list_tickets()}
