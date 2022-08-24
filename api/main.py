from fastapi import FastAPI
from api.auth import router as auth_router
from api.post import post_router as post_router
from api.categories.router import cat_router as cat_router
from api.user.router import user_router
from api import models
from api.database.database_connect import engine

app = FastAPI()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="Api{TestFastApi}",
    description="Testing python fastapi",
    version=0.10,
    openapi_url="/openapi.json"
)


def create_tables():  # new
    models.Base.metadata.create_all(bind=engine)


def start_application():
    create_tables()  # new
    return app


app.include_router(auth_router.router, tags=["Auth"])
app.include_router(user_router, tags=["User"])
app.include_router(post_router.post_router, tags=["Post"])
app.include_router(cat_router, tags=["Category"])
app = start_application()
