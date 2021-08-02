import uvicorn
from fastapi import FastAPI

from api.routers import users_router
from api.routers import items_router
from task_fast_api.config import Settings

settings = Settings()
app = FastAPI()

app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(items_router.router, prefix="/items", tags=["items"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
