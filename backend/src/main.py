from fastapi import FastAPI
from database import engine
from models.models import Post, User
from api.posts import router as post_router
from api.users import router as user_router
from api.ways import router as way_router
from api.s3storage import router as s3_router
from api.profile import router as profile_router
from fastapi.staticfiles import StaticFiles
from models.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(way_router)
app.include_router(s3_router)
app.include_router(profile_router)
app.mount('/static', StaticFiles(directory='./static', html=True))