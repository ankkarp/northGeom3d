import streamlit as st
import yaml
from PIL import Image
import plotly.graph_objects as go

from transformers import pipeline
import torch
import numpy as np
from PIL import Image
import time
device = "cuda"
checkpoint = "depth-anything/Depth-Anything-V2-base-hf"
pipe = pipeline("depth-estimation", model=checkpoint, device=device)

def run_inference(left_image,right_image):
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

    print(time.time() - time_start)
    return np_mask_left,np_mask_right
    

# Интерфейс Streamlit
st.title("northGeom3d")

# Загрузка изображений и файла с оптической схемой
left_image_file = st.file_uploader("Левое изображение", type=["jpg", "jpeg", "png"])
right_image_file = st.file_uploader("Правое изображение", type=["jpg", "jpeg", "png"])
# yaml_file = st.file_uploader("Загрузите YAML файл с оптической схемой", type=["yaml"])

if left_image_file and right_image_file:
    # Отображение загруженных изображений
    left_image = Image.open(left_image_file).convert('RGB')
    right_image = Image.open(right_image_file).convert('RGB')

    st.image(left_image, caption="Левое изображение", use_column_width=True)
    st.image(right_image, caption="Правое изображение", use_column_width=True)
    

    if st.button("Обработать"):
        left_image_mask,right_image_mask = run_inference(left_image,right_image)

        # Вывод результатов расчетов
        st.image(left_image_mask, caption="Левое изображение", use_column_width=True)
        st.image(right_image_mask, caption="Правое изображение", use_column_width=True)
       
