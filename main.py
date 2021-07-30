import uvicorn
from fastapi import FastAPI

from task_fast_api.config import Settings

settings = Settings()
app = FastAPI()


@app.get("/info")
async def info():
    return settings


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
