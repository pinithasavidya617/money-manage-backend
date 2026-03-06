from fastapi import FastAPI
from routes.transaction_router import router as transaction_router

app = FastAPI(
    title="Money Management API",
    description="A FastAPI backend for a money management mobile app.",
    version="1.0.0",
)

app.include_router(transaction_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Money Management API"}
