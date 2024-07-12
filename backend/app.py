from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import database  # Import the database module

app = FastAPI()

class Image(BaseModel):
    filename: str
    label: str
    recognition_result: str

@app.on_event("startup")
def startup():
    database.create_tables()  # Ensure the tables are created on startup

@app.get("/images", response_model=List[Image])
def get_images():
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT filename, label, recognition_result FROM images')
    rows = cursor.fetchall()
    conn.close()
    return [{"filename": row[0], "label": row[1], "recognition_result": row[2]} for row in rows]

@app.post("/images", status_code=201)
def create_image(image: Image):
    conn = database.get_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO images (filename, label, recognition_result)
    VALUES (?, ?, ?)
    ''', (image.filename, image.label, image.recognition_result))
    conn.commit()
    conn.close()
    return {"message": "Image metadata inserted successfully"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     """

#     :param item_id: int:
#     :param q: str:  (Default value = None)

#     """
#     return {"item_id": item_id, "q": q}
