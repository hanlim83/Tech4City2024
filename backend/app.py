from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """ """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """

    :param item_id: int:
    :param q: str:  (Default value = None)
    :param item_id: int:
    :param q: str:  (Default value = None)

    """
    return {"item_id": item_id, "q": q}
