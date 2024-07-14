import os
from datetime import datetime

import shutil
import uvicorn
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from starlette.staticfiles import StaticFiles

import model

DATABASE_URL = "sqlite:///database.db"
frontend_folder = "../frontend"
uploads_folder = "./uploads"
results_folder = "./results"
if not os.path.exists(uploads_folder):
    os.makedirs(uploads_folder)
if not os.path.exists(results_folder):
    os.makedirs(results_folder)
Base = declarative_base()
yolo_model = None

### initalise database tables and columns ###


class Upload(Base):
    """ """

    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, nullable=False)
    results = relationship("Result", back_populates="upload")


class Result(Base):
    """ """

    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, nullable=False)
    fire = Column(Float, nullable=True)
    default = Column(Float, nullable=True)
    smoke = Column(Float, nullable=True)
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### initialise the model on standup ###


@app.on_event("startup")
def startup():
    """ """
    global yolo_model
    Base.metadata.create_all(bind=engine)
    yolo_model = model.load_model()

### anaylses uploaded images and determine if they is a fire within the image ###


@app.post("/analyze", status_code=200)
async def analyseUploadedImage(file: UploadFile = File(...)):
    try:
        db = SessionLocal()
        # Here you can save the file or process it
        filename = "_".join(
            [datetime.now().strftime("%Y%m%d_%H%M%S"), file.filename])
        # For example, save the file to disk
        with open(f"uploads/{filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        db_upload = Upload(filename=filename)
        db.add(db_upload)
        db.commit()
        results = model.predict(yolo_model, f"{uploads_folder}/{filename}")
        db_result = None
        # saves results from model prediction to our database.db
        for r in results:
            r.save(os.path.join(os.path.dirname(
                __file__), results_folder, filename))
            db_result = Result(
                filename=filename,
                upload_id=db_upload.id,
            )
            # puts the accuracy score into one of three columns (fire, default, smoke)
            for box in r.boxes:
                if r.names[box.cls.item()] == "fire" or r.names[box.cls.item()] == "Fire":
                    db_result.fire = box.conf.item()
                elif r.names[box.cls.item()] == "smoke" or r.names[box.cls.item()] == "Smoke":
                    db_result.smoke = box.conf.item()
            if db_result.fire == None and db_result.smoke == None:
                db_result.default = 1
            db.add(db_result)
        db.commit()
        return JSONResponse(content={
            "filename": db_result.filename,
            "fire": db_result.fire,
            "smoke": db_result.smoke,
            "default": db_result.default,
            "downloadPath": f"/files/results/{filename}"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### returns all past results predict results and their accuracy score ###


@app.get("/results", status_code=200)
def getAllResults():
    """ """
    try:
        db = SessionLocal()
        results = db.query(Result).all()
        return JSONResponse(content=[{
            "filename": result.filename,
            "fire": result.fire,
            "smoke": result.smoke,
            "default": result.default,
            "downloadPath": f"/files/results/{result.filename}",
            "linked_upload_id": result.upload_id
        } for result in results])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### creates folders to store the results for our model's analyse ###
app.mount("/files/uploads",
          StaticFiles(directory=uploads_folder),
          name="uploads")
app.mount("/files/results",
          StaticFiles(directory=results_folder),
          name="results")
app.mount("/", CustomStaticFiles(directory=frontend_folder, html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
