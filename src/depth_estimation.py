import time
import numpy as np
from transformers import pipeline
from src.image_processing import find_circle, find_circle_and_line
from src.config import config

device = config['device']
checkpoint = config['depth_model']['repo_hf']
task = config['depth_model']['pipeline_task']
pipe = pipeline(task=task, model=checkpoint, device=device)

def run_inference_marked_grid(left_image, right_image):
    time_start = time.time()
    predictions_right = pipe(right_image)
    predictions_left = pipe(left_image)

    left_image_mask = np.array(predictions_left["depth"])
    right_image_mask = np.array(predictions_right["depth"])

    clear_mask_left = left_image_mask.copy()
    clear_mask_left[clear_mask_left < 100] = 0

    clear_mask_right = right_image_mask.copy()
    clear_mask_right[clear_mask_right < 100] = 0

    np_mask_left = np.array(left_image)
    np_mask_left = np_mask_left[:, :, ::-1].copy()

    np_mask_right = np.array(right_image)
    np_mask_right = np_mask_right[:, :, ::-1].copy()

    np_mask_left[clear_mask_left == 0] = 0
    np_mask_right[clear_mask_right == 0] = 0

    np_mask_left = find_circle_and_line(np_mask_left)
    np_mask_right = find_circle_and_line(np_mask_right)

    print(time.time() - time_start)
    return np_mask_left, np_mask_right, clear_mask_left, clear_mask_right

def run_inference_marked_town(left_image, right_image):
    time_start = time.time()
    predictions_right = pipe(right_image)
    predictions_left = pipe(left_image)

    left_image_mask = np.array(predictions_left["depth"])
    right_image_mask = np.array(predictions_right["depth"])

    clear_mask_left = left_image_mask.copy()
    clear_mask_left[clear_mask_left < 100] = 0

    clear_mask_right = right_image_mask.copy()
    clear_mask_right[clear_mask_right < 100] = 0

    np_mask_left = np.array(left_image)
    np_mask_left = np_mask_left[:, :, ::-1].copy()

    np_mask_right = np.array(right_image)
    np_mask_right = np_mask_right[:, :, ::-1].copy()

    np_mask_left[clear_mask_left == 0] = 0
    np_mask_right[clear_mask_right == 0] = 0

    np_mask_left = find_circle(np_mask_left)
    np_mask_right = find_circle(np_mask_right)

    print(time.time() - time_start)
    return np_mask_left, np_mask_right, clear_mask_left, clear_mask_right
