from fastapi import FastAPI
from .router import router as auth_router, profile
from .db import Base, engine

app = FastAPI()

app.include_router(auth_router)
app.include_router(profile)

Base.metadata.create_all(bind=engine)