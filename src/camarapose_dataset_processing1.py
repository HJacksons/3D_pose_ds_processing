import json
import os
import random
import shutil
from math import atan2, degrees
import numpy as np
from scipy.spatial.transform import Rotation as R


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def update_frame_paths_and_add_rotation(frames, target_dir, camera_angle_x):
    for frame in frames:
        base_name = 'r_' + os.path.basename(frame['file_path'])
        frame['file_path'] = './{}/{}'.format(target_dir, base_name)
        rotation_matrix = np.array(frame['transform_matrix'][:3])
        r = R.from_matrix(rotation_matrix[:3, :3])
        frame['rotation'] = r.as_euler('xyz', degrees=True)[0]  # Assuming rotation around x-axis


def move_images(frames, source_dir, target_dir, is_test=False):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for frame in frames:
        src_path = os.path.join(source_dir, os.path.basename(frame['file_path']).replace('r_', ''))
        dst_path = os.path.join(target_dir, frame['file_path'].split('/')[-1])
        shutil.copy(src_path, dst_path)
        if is_test:
            depth_img = src_path.replace('.png', '_depth_0000.png')
            normal_img = src_path.replace('.png', '_normal_0000.png')
            depth_dst = dst_path.replace('.png', '_depth_0000.png')
            normal_dst = dst_path.replace('.png', '_normal_0000.png')
            if os.path.exists(depth_img):
                shutil.copy(depth_img, depth_dst)
            if os.path.exists(normal_img):
                shutil.copy(normal_img, normal_dst)


original_json_path = 'transforms.json'
transforms_data = load_json(original_json_path)

fl_x = transforms_data.get('fl_x', 0)
w = transforms_data.get('w', 0)
camera_angle_x = 2 * degrees(atan2(w, (2 * fl_x)))

train_ratio = 0.70
val_ratio = 0.20
test_ratio = 0.10

frames = transforms_data['frames']
total_frames = len(frames)

random.shuffle(frames)
train_frames = frames[:int(total_frames * train_ratio)]
val_frames = frames[int(total_frames * train_ratio):int(total_frames * (train_ratio + val_ratio))]
test_frames = frames[int(total_frames * (train_ratio + val_ratio)):]

update_frame_paths_and_add_rotation(train_frames, 'train', camera_angle_x)
update_frame_paths_and_add_rotation(val_frames, 'val', camera_angle_x)
update_frame_paths_and_add_rotation(test_frames, 'test', camera_angle_x)

train_json = {"camera_angle_x": camera_angle_x, "frames": train_frames}
val_json = {"camera_angle_x": camera_angle_x, "frames": val_frames}
test_json = {"camera_angle_x": camera_angle_x, "frames": test_frames}

save_json(train_json, 'transforms_train.json')
save_json(val_json, 'transforms_val.json')
save_json(test_json, 'transforms_test.json')

source_dir = 'images'
move_images(train_frames, source_dir, 'train')
move_images(val_frames, source_dir, 'val')
move_images(test_frames, source_dir, 'test', is_test=True)

print("Dataset processing complete.")
