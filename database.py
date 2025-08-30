from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Local SQLite DB (offline storage)
SQLITE_URL = "sqlite:///./local.db"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class WaterResult(Base):
    __tablename__ = "water_results"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    hpi = Column(Float, nullable=True)
    hei = Column(Float, nullable=True)
    synced = Column(Integer, default=0)  # 0 = not synced, 1 = synced
Base.metadata.create_all(bind=engine)

