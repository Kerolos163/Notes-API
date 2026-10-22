from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from app.database import get_db, create_tables, engine
from pydantic import BaseModel
from app.models import Note
from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
