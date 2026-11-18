# =====================================================================================================
#  STAGE 3: SQLALCHEMY (ORM)
#  Final version — all routes go through the SQLAlchemy ORM session instead of raw SQL or an in-memory list.
# =====================================================================================================

from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post , user ,auth , vote
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
# Root health-check route
@app.get("/")
def home():
    """Health check endpoint that returns a simple greeting message."""
    return {"message": "Hello World"}

