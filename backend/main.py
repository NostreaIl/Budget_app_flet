from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Budget API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Budget FastAPI backend ready!", "db": "postgres ready soon"}

@app.get("/api/transactions")
async def get_transactions():
    # TODO: connect PostgreSQL
    return [{"id": 1, "date": "2026-01-11", "montant": -2.5, "categorie": "Pain"}]
