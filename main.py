# app/main.py
from fastapi import FastAPI
from routers import batches

app = FastAPI(
    title="Preorder Forecast API",
    description="周邊預購數量／成本／毛利試算 API",
    version="0.1.0",
)

# register routers
app.include_router(batches.router, prefix="/batches", tags=["batches"])

# health check
@app.get("/health")
def health():
    return {"status": "ok"}
