import os

from ultralytics import YOLO

annotated_image_directory = "annotated_images"


def load_model():
    """ """
    # Load the model
    model = YOLO(os.path.join(os.path.dirname(__file__), "model.pt"))
    return model


def predict(model, image_path):
    """

    :param image_path:
    :param model:

    """
    # Perform inference on the image
    results = model(image_path)
    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb
        result.save(f"{annotated_image_directory}/{image_path.split('/')[-1]}")
    return results
