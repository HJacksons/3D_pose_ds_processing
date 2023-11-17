# Dataset Preprocessing for NeRF Models

This repository provides tools for preprocessing camera pose datasets for use with Neural Radiance Fields (NeRF) models.

## Features

- **Split Dataset**: Automatically splits the dataset into training, testing, and validation subsets.
- **Depth Generation**: Utilizes the MiDaS model to generate depth information for test images.
- **Additional Features Generation**:
  - Camera Angle
  - Rotation

## Usage

### Prerequisites

- **Images Directory**: Ensure you have a directory containing all the images for the scene.
- **Transforms File**: A `transforms.json` file must be present along images directory. The additional transforms for training, testing, and validation will be generated automatically.

### Steps

1. **Run Preprocessing Script**:
   - Navigate to the `src` directory.
   - Run the only `.py` file present to start preprocessing.

2. **Generate Depth Images** (for test images):
   - Copy the test images directory to the MiDaS repository.
   - Run `test_depth.py` in the MiDaS repository.
   - The resulting depth images in MiDaS's "output" directory should be moved back to the test images directory in your dataset preprocessing project.

### Notes

- The algorithm automatically generates `train`, `test`, and `val` directories. You don't need to create these manually.
- Make sure to transfer the processed depth images from MiDaS to the appropriate directory in your dataset preprocessing project.
