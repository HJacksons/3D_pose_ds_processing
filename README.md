# Dataset Preprocessing
Camera pose dataset preprocessing for use with NeRF models
 * Split dataset and generate respective transforms
 * Generates depth of test images using [MiDas model](https://github.com/HJacksons/MiDaS)
 * Generates additional features
   * Camera angle
   * Rotation
## Usage
* Only the images directory with the images for the scene is required. You dont need the train, test and val as the algorithm generates them.
* You must have the corresponding transforms.json file present for the images in the image directory. the other transforms are generated together with train, test and val, respectively

   * Run the only .py file in the src directory
