from fastapi import FastAPI

app = FastAPI(title="Arbitrage Scout")

@app.get("/")
def home():
    return {"ok": True, "app": "Arbitrage Scout", "message": "Service is running."}

@app.get("/health")
def health():
    return {"status": "healthy"}
