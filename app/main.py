from fastapi import FastAPI
from pydantic import BaseModel, Field
from .service import Service

app = FastAPI(title="Semantic LLM Cache", version="0.1.0")
service = Service()

class Request(BaseModel):
    value: str = Field(min_length=1, max_length=4000)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/run")
def run(req: Request):
    return service.run(req.value)
