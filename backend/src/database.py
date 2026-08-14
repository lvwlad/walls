from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from schemas.schemas import Base
import dotenv
import os

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



