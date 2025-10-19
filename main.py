# main.py
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from ebay_api import fetch_sold_data, USE_MOCK_DATA

app = FastAPI()

@app.get("/sold")
def get_sold_items(q: str = Query(..., description="Search term")):
    data = fetch_sold_data(q)
    if USE_MOCK_DATA:
        return JSONResponse({"source": "mock", "results": data})
    else:
        return JSONResponse({"source": "live", "results": data})


@app.get("/")
def root():
    status = "mock" if USE_MOCK_DATA else "live"
    return {"message": f"API ready. Current mode: {status}"}