import torch

# Function to load the custom pre-trained YOLOv5 model
def load_custom_model(model_path):
    # Load the custom model
    model = torch.load(model_path)
    # Ensure it's in evaluation mode
    model.eval()
    return model

# Function to perform inference
def perform_inference(model, image_path):
    # Load an image
    img = torch.zeros((1, 3, 640, 640))  # Example image tensor, replace with actual image loading code
    # Perform inference
    results = model(img)
    # Process results, for example, print or plot them
    results.print()

# Example usage
if __name__ == "__main__":
    # Path to your custom trained model file
    model_path = 'path/to/your/custom_model.pt'
    
    # Load the custom model
    model = load_custom_model(model_path)
    
    # Path to your image
    image_path = 'path/to/your/image.jpg'
    
    # Perform inference
    perform_inference(model, image_path)