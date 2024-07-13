import os
from datetime import datetime

import model
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from starlette.staticfiles import StaticFiles

DATABASE_URL = "sqlite:///image_recognition.db"
frontend_folder = "../frontend"
uploads_folder = "./uploads"
annotated_results_folder = "./results"
if not os.path.exists(uploads_folder):
    os.makedirs(uploads_folder)
if not os.path.exists(annotated_results_folder):
    os.makedirs(annotated_results_folder)
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


class Image(BaseModel):
    """ """

    filename: str
    label: str
    recognition_result: str


class CustomStaticFiles(StaticFiles):
    """ """
    async def lookup(self, path):
        if path == "":
            # Serve index.html for the root URL
            return os.path.join(self.directory, "index.html")
        else:
            return await super().lookup(path)


@app.on_event("startup")
def startup():
    """ """
    model.load_model()
    Base.metadata.create_all(bind=engine)


@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        # Here you can save the file or process it
        filename = "_".join([datetime.now().strftime("%Y%m%d_%H%M%S"), file.filename])
        # For example, save the file to disk
        with open(f"uploads/{filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        results = model.predict(f"uploads/{filename}")
        # Return the prediction results
        return JSONResponse(content=results)
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
            )
            for result in results
        ]
    finally:
        db.close()


@app.get("/test", status_code=200)
def test():
    """ """
    return "hello world"


app.mount("/files/uploads", StaticFiles(directory=uploads_folder), name="uploads")
app.mount(
    "/files/results", StaticFiles(directory=annotated_results_folder), name="results"
)
app.mount("/", CustomStaticFiles(directory=frontend_folder, html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
