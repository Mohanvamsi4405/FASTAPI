# Core SQLAlchemy imports for database connection and ORM setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from urllib.parse import quote_plus

from .config import settings

db_password = quote_plus(settings.db_password)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_user}:{db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# Create a database engine that manages connections to PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)



# SessionLocal: factory for creating database sessions; autocommit=False means explicit commits required, autoflush=False prevents automatic flush before queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# Base: declarative base class for all ORM models to inherit from; enables SQLAlchemy to track model metadata
Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Retry loop: keep trying to connect to Postgres until it succeeds
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='FastAPI',
#             user='postgres',
#             password="8106710994Amma@",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database Connection was Successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error", error)
#         time.sleep(5)
