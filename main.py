from fastapi import FastAPI
from endpoints import items

app = FastAPI()

app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
