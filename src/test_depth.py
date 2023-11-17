import cv2
import torch
from torchvision.transforms import Compose
from midas.midas_net import MidasNet
from midas.transforms import Resize, NormalizeImage, PrepareForNet
import os

# Initialize MiDaS model
model_type = "DPT_Large"  # or "MiDaS_small"
midas = torch.hub.load("intel-isl/MiDaS", model_type)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
midas.to(device)
midas.eval()

# Load transforms
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.default_transform

def process_image(image_path, output_path):
    # Read and transform the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    input_batch = transform(img).to(device)

    # Predict and create the depth map
    with torch.no_grad():
        prediction = midas(input_batch)

        # Convert prediction to numpy array
        prediction = prediction.squeeze().cpu().numpy()
        depth_map = (prediction * 255).astype('uint8')

    # Save the depth map
    cv2.imwrite(output_path, depth_map)

# Directory containing test images
test_image_dir = 'path/to/test/images'
output_dir = 'path/to/save/depth_images'

# Process each test image
for image_name in os.listdir(test_image_dir):
    # Filter out non-standard images if necessary
    if not image_name.endswith('.png'):  # Example condition
        continue

    image_path = os.path.join(test_image_dir, image_name)
    depth_image_name = image_name.replace('.png', '_depth_0000.png')
    depth_image_path = os.path.join(output_dir, depth_image_name)

    process_image(image_path, depth_image_path)

print("Depth maps for test images generated.")
