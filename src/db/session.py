from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

config = Config()
engine = create_engine(config.MYSQL_URI, pool_pre_ping=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
