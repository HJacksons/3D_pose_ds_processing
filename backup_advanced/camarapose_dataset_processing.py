import os
import json
import shutil
import random


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def update_frame_paths(frames, target_dir):
    for frame in frames:
        base_name = 'r_' + os.path.basename(frame['file_path'])
        frame['file_path'] = './{}/{}'.format(target_dir, base_name)


def move_images(frames, source_dir, target_dir, is_test=False):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for frame in frames:
        src_path = os.path.join(source_dir, os.path.basename(frame['file_path']).replace('r_', ''))
        dst_path = os.path.join(target_dir, frame['file_path'].split('/')[-1])
        shutil.copy(src_path, dst_path)  # Use shutil.move(src_path, dst_path) to move files instead
        if is_test:
            # Assuming the depth and normal images follow a specific naming convention
            depth_img = src_path.replace('.png', '_depth_0000.png')
            normal_img = src_path.replace('.png', '_normal_0000.png')
            depth_dst = dst_path.replace('.png', '_depth_0000.png')
            normal_dst = dst_path.replace('.png', '_normal_0000.png')
            # Copy depth and normal images if they exist
            if os.path.exists(depth_img):
                shutil.copy(depth_img, depth_dst)
            if os.path.exists(normal_img):
                shutil.copy(normal_img, normal_dst)


# Path to the original transforms JSON file
original_json_path = '../src/transforms.json'

# Loading the original transforms data
transforms_data = load_json(original_json_path)

# Split ratios
train_ratio = 0.70
val_ratio = 0.20
test_ratio = 0.10

# Extracting the frame data
frames = transforms_data['frames']
total_frames = len(frames)

# Calculating the number of frames for each split
num_train = int(total_frames * train_ratio)
num_val = int(total_frames * val_ratio)
num_test = total_frames - num_train - num_val

# Randomly shuffling the frames
random.shuffle(frames)

# Splitting the frames and updating file paths
train_frames = frames[:num_train]
update_frame_paths(train_frames, '../src/train')
val_frames = frames[num_train:num_train + num_val]
update_frame_paths(val_frames, '../src/val')
test_frames = frames[num_train + num_val:]
update_frame_paths(test_frames, '../src/test')

# Copying the common camera parameters
common_params = {key: transforms_data[key] for key in transforms_data.keys() if key != "frames"}

# Creating JSON structure for training, validation, and testing
train_json = {**common_params, "frames": train_frames}
val_json = {**common_params, "frames": val_frames}
test_json = {**common_params, "frames": test_frames}

# Saving the split JSON data
save_json(train_json, '../src/transforms_train.json')
save_json(val_json, '../src/transforms_val.json')
save_json(test_json, '../src/transforms_test.json')

# Source directory where original images are stored
source_dir = '../src/images'

# Moving images to respective directories
move_images(train_frames, source_dir, '../src/train')
move_images(val_frames, source_dir, '../src/val')
move_images(test_frames, source_dir, '../src/test', is_test=True)

print("Dataset has been split and images have been organized into train, val, and test directories.")
