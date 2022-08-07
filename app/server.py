from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "data link": "/data",
        "stats link": "/stats"
            }

@app.get("/data")
async def root_data():
    return {"message": "data"}

@app.post("/data")
async def root_data_post():
    return {"message": "Hello World"}

@app.get("/stats")
async def root_stats():
    return {"message": "Stats"}