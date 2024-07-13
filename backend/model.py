import os

from ultralytics import YOLO


def load_model():
    """ """
    # Load the model
    model = YOLO(os.path.join(os.path.dirname(__file__), "model.pt"))
    return model


def predict(model, image_path):
    """

    :param image_path: param model:
    :param model:

    """
    # Perform inference on the image
    results = model(image_path)
    for result in results:
        print(result.names)
        for box in result.boxes:
            print(result.names[box.cls.item()])
            print(box.conf.item())
        result.save(
            os.path.join(os.path.dirname(__file__), "results",
                         image_path.split("/")[-1]))
    return results
