# Dataset Preprocessing
Camera pose dataset preprocessing for use with NeRF models
 * Split dataset and generate respective transforms
 * Generates depth of test images using [MiDas model](https://github.com/HJacksons/MiDaS)
 * Generates additional features
   * Camera angle
   * Rotation
## Usage
* Only the images directory with the images for the scene is required. You dont need the train, test and val as the algorithm generates them.
* You must have the corresponding transforms.json file present for the images in the image directory. The other transforms are generated together with train, test and val, respectively

   * Run the only .py file in the src directory
   * For generating depth images for the test images,
      * copy the test images directory to the MiDas repository and run test_depth.py
      * resulting depth images in the output directory in Midas can be copied to the test images directory and transferred to the dataset preprocessing project repository
