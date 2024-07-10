import torch
from PIL import Image, ImageDraw

model_path = "model.pt"


def load_model(model_path):
    """
    Load the model from a given path.

    Parameters:
    - model_path (str): The path to the model file.

    Returns:
    - model: The loaded YOLOv8 model.
    """
    model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path)
    return model


def make_prediction(model, image_path):
    """
    Make a prediction on a single image using the loaded model.

    Parameters:
    - model: The loaded YOLOv8 model.
    - image_path (str): The path to the image file.

    Returns:
    - results: The prediction results.
    """
    img = Image.open(image_path)
    results = model(img)
    return results


def draw_prediction_bb(image_path, results):
    """
    Draw bounding boxes on the image based on the prediction results.

    Parameters:
    - image_path (str): The path to the image file.
    - results: The prediction results from the model.

    Returns:
    - img: The image with bounding boxes drawn.
    """
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    for *xyxy, conf, cls in results.xyxy[0]:
        label = results.names[int(cls)]
        draw.rectangle(xyxy, outline=(255, 0, 0), width=2)
        draw.text((xyxy[0], xyxy[1]), f"{label} {conf:.2f}", fill=(255, 0, 0))
    return img
