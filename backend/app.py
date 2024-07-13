from . import model
import uvicorn
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///image_recognition.db"
Base = declarative_base()


class Upload(Base):
    """ """
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploadPath = Column(String, nullable=False)
    results = relationship("Result", back_populates="upload")


class Result(Base):
    """ """
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    label = Column(String)
    recognition_result = Column(String)
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    upload = relationship("Upload", back_populates="results")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Serve the frontend files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


class Image(BaseModel):
    """ """
    filename: str
    label: str
    recognition_result: str


@app.on_event("startup")
def startup():
    """ """
    Base.metadata.create_all(bind=engine)


@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        # Here you can save the file or process it
        filename = file.filename
        # For example, save the file to disk
        with open(f"uploads/{filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = model.predict(f"uploads/{filename}")
        # Return a response or processing result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getAllResults", status_code=200)
def getAllResults():
    """ """
    db = SessionLocal()
    try:
        results = db.query(Result).all()
        return [
            Image(
                filename=result.filename,
                label=result.label,
                recognition_result=result.recognition_result,
            ) for result in results
        ]
    finally:
        db.close()


@app.get("/test", status_code=200)
def test():
    """ """
    return "hello world"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
