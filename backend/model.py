from ultralytics import YOLO

annotated_image_directory = "annotated_images"
# Load the custom YOLOv8 model
model = YOLO("/app/backend/model.pt")


def predict(image_path):
    """

    :param image_path: 

    """
    # Perform inference on the image
    results = model(image_path)
    # Save the annotated image
    results.img[0].save(f"{annotated_image_directory}/{image_path.split('/')[-1]}")
    return results.img[0]
