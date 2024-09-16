import streamlit as st
from PIL import Image
from src.depth_estimation import run_inference_marked_grid, run_inference_marked_town
# from src.visualize_3d import create_3d_plot
from src.config import config

st.title("northGeom3d")

tab1, tab2, tab3 = st.tabs([tab['name'] for tab in config['tabs']])

def process_images(process_function: callable, left_image: Image, right_image: Image):
    """
    Process a pair of images with the given function and display the results.

    Parameters
    ----------
    process_function : callable
        A function that takes two images and returns two images and two depth maps.
    left_image : PIL.Image
        The left image.
    right_image : PIL.Image
        The right image.
    """
    left_image_mask, right_image_mask, map1, map2 = process_function(left_image, right_image)
    st.image(left_image_mask, caption=config['image_upload']['caption_left'], use_column_width=True)
    st.image(right_image_mask, caption=config['image_upload']['caption_right'], use_column_width=True)
    st.image(map1, caption=config['depth_map_captions']['depth_map_1'], use_column_width=True)
    st.image(map2, caption=config['depth_map_captions']['depth_map_2'], use_column_width=True)


with tab1:
    left_image_file = st.file_uploader("Левое изображение ", type=config['image_upload']['allowed_types'])
    right_image_file = st.file_uploader("Правое изображение ", type=config['image_upload']['allowed_types'])

    if left_image_file and right_image_file:
        left_image = Image.open(left_image_file).convert('RGB')
        right_image = Image.open(right_image_file).convert('RGB')

        st.image(left_image, caption=config['image_upload']['caption_left'], use_column_width=True)
        st.image(right_image, caption=config['image_upload']['caption_right'], use_column_width=True)

        if st.button(config['image_upload']['button_label']):
            process_images(run_inference_marked_grid, left_image, right_image)


with tab2:
    left_image_file = st.file_uploader("Левое изображение", type=config['image_upload']['allowed_types'])
    right_image_file = st.file_uploader("Правое изображение", type=config['image_upload']['allowed_types'])

    if left_image_file and right_image_file:
        left_image = Image.open(left_image_file).convert('RGB')
        right_image = Image.open(right_image_file).convert('RGB')

        st.image(left_image, caption=config['image_upload']['caption_left'], use_column_width=True)
        st.image(right_image, caption=config['image_upload']['caption_right'], use_column_width=True)

        if st.button(config['image_upload']['button_label']):
            process_images(run_inference_marked_town, left_image, right_image)


with tab3:
    st.write("Нету, в дорожную карту заложено")
