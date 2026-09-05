import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from the .env file")


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    business = Column(String(255), nullable=False)
    requirement = Column(Text, nullable=False)
    recommended_service = Column(String(255), nullable=False)
    timeline = Column(String(255), nullable=False)
    budget = Column(String(255), nullable=False)
    lead_status = Column(String(20), nullable=False)
    summary = Column(Text, nullable=False)
    next_action = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("PostgreSQL leads table created successfully.")