import uvicorn
from fastapi import FastAPI

from api.routers.users_router import router
from task_fast_api.config import Settings

settings = Settings()
app = FastAPI()

app.include_router(router, prefix="/users", tags=["users"])

# print('hello')
@app.get("/info")
async def info():
    return settings


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
