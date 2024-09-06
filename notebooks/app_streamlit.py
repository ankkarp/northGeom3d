import streamlit as st
import yaml
from PIL import Image
import plotly.graph_objects as go
import cv2
from transformers import pipeline
import torch
import numpy as np
from PIL import Image
import time
device = "cuda"
checkpoint = "depth-anything/Depth-Anything-V2-base-hf"
pipe = pipeline("depth-estimation", model=checkpoint, device=device)


def find_circle(img):
    """
    Find circles in a binary image and draw them to the original image.

    Parameters
    ----------
    img : numpy array
        Input image.

    Returns
    -------
    img : numpy array
        Image with drawn circles.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_radius = 20
    max_radius = 1000

    centers = []

    for contour in contours:

        (x, y), radius = cv2.minEnclosingCircle(contour)
        if min_radius <= radius <= max_radius:
            cv2.circle(img, (int(x), int(y)), int(radius), (255, 0, 0), 2)
            centers.append((int(x), int(y)))

    for i in range(len(centers) - 1):
        cv2.line(img, centers[i], centers[i + 1], (0, 255, 0), 2)

    return img

def run_inference(left_image,right_image):
    """
    Runs depth estimation on the given left and right images.

    Args:
        left_image (PIL.Image): The left image.
        right_image (PIL.Image): The right image.

    Returns:
        A tuple of two numpy arrays, where the first element is the processed left image and the second element is the processed right image.
    """
    time_start = time.time()
    predictions_right = pipe(right_image)
    predictions_left = pipe(left_image)

    left_image_mask = np.array(predictions_left["depth"])
    right_image_mask = np.array(predictions_right["depth"])


    clear_mask_left = left_image_mask.copy()
    clear_mask_left[clear_mask_left<100] = 0

    clear_mask_right = right_image_mask.copy()
    clear_mask_right[clear_mask_right<100] = 0

    np_mask_left = np.array(left_image)
    np_mask_left = np_mask_left[:, :, ::-1].copy()

    np_mask_right = np.array(right_image)
    np_mask_right = np_mask_right[:, :, ::-1].copy()

    np_mask_left[clear_mask_left == 0] = 0
    np_mask_right[clear_mask_right == 0] = 0



    np_mask_left = find_circle(np_mask_left)
    np_mask_right = find_circle(np_mask_right)



    print(time.time() - time_start)
    return np_mask_left,np_mask_right
    


st.title("northGeom3d")


left_image_file = st.file_uploader("Левое изображение", type=["jpg", "jpeg", "png"])
right_image_file = st.file_uploader("Правое изображение", type=["jpg", "jpeg", "png"])
# yaml_file = st.file_uploader("Загрузите YAML файл с оптической схемой", type=["yaml"])

if left_image_file and right_image_file:

    left_image = Image.open(left_image_file).convert('RGB')
    right_image = Image.open(right_image_file).convert('RGB')

    st.image(left_image, caption="Левое изображение", use_column_width=True)
    st.image(right_image, caption="Правое изображение", use_column_width=True)
    

    if st.button("Обработать"):
        left_image_mask,right_image_mask = run_inference(left_image,right_image)
        st.image(left_image_mask, caption="Левое изображение", use_column_width=True)
        st.image(right_image_mask, caption="Правое изображение", use_column_width=True)
       
