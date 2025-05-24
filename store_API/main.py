from fastapi import FastAPI

from store_API.routers.post import router as post_router

app = FastAPI()

app.include_router(post_router)
