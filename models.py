import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))

if DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

is_sqlite = DATABASE_URL.startswith("sqlite")
is_localhost = "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL

engine_kwargs = {"future": True}
if not is_sqlite and not is_localhost:
    engine_kwargs["connect_args"] = {"sslmode": "require"}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WorkbenchProject(Base):
    __tablename__ = "bw_project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(240), nullable=False)
    raw_notes = Column(Text, nullable=False)
    preferences = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    snapshots = relationship("PlanningSnapshot", back_populates="project", cascade="all, delete-orphan")


class PlanningSnapshot(Base):
    __tablename__ = "bw_snapshot"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("bw_project.id"), nullable=False, index=True)
    title = Column(String(240), nullable=False)
    summary = Column(Text, nullable=False)
    brief_json = Column(Text, nullable=False)
    change_summary = Column(Text, nullable=True)
    thumbnail_text = Column(String(280), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    project = relationship("WorkbenchProject", back_populates="snapshots")


class SeedPrompt(Base):
    __tablename__ = "bw_seed_prompt"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180), nullable=False, unique=True)
    notes = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
