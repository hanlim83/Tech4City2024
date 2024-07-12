from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///image_recognition.db"
Base = declarative_base()

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploadPath = Column(String, nullable=False)
    results = relationship("Result", back_populates="upload")

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    label = Column(String)
    recognition_result = Column(String)
    upload_id = Column(Integer, ForeignKey('uploads.id'))
    upload = relationship("Upload", back_populates="results")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

class Image(BaseModel):
    filename: str
    label: str
    recognition_result: str

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/getAllResults", status_code=200)
def getAllResults():
    db = SessionLocal()
    try:
        results = db.query(Result).all()
        return [Image(filename=result.filename, label=result.label, recognition_result=result.recognition_result) for result in results]
    finally:
        db.close()

@app.get("/test", status_code=200)
def test():
    return "hello world"