import streamlit as st
from PIL import Image
from src.depth_estimation import run_inference_marked_grid, run_inference_marked_town
from src.visualize_3d import create_3d_plot

st.title("northGeom3d")

tab1, tab2, tab3 = st.tabs(["Расстояние между точками, диаметр окружности", "Расстояние между точками", "Листовой прокат"])

with tab1:
    left_image_file = st.file_uploader("Левое изображение ", type=["jpg", "jpeg", "png"])
    right_image_file = st.file_uploader("Правое изображение ", type=["jpg", "jpeg", "png"])

    if left_image_file and right_image_file:
        left_image = Image.open(left_image_file).convert('RGB')
        right_image = Image.open(right_image_file).convert('RGB')

        st.image(left_image, caption="Левое изображение", use_column_width=True)
        st.image(right_image, caption="Правое изображение", use_column_width=True)

        if st.button("Обработать "):
            left_image_mask, right_image_mask, map1, map2 = run_inference_marked_grid(left_image, right_image)
            st.image(left_image_mask, caption="Левое изображение", use_column_width=True)
            st.image(right_image_mask, caption="Правое изображение", use_column_width=True)
            st.image(map1, caption="Карта глубины", use_column_width=True)
            st.image(map2, caption="Карта глубины", use_column_width=True)

with tab2:
    left_image_file = st.file_uploader("Левое изображение", type=["jpg", "jpeg", "png"])
    right_image_file = st.file_uploader("Правое изображение", type=["jpg", "jpeg", "png"])

    if left_image_file and right_image_file:
        left_image = Image.open(left_image_file).convert('RGB')
        right_image = Image.open(right_image_file).convert('RGB')

        st.image(left_image, caption="Левое изображение", use_column_width=True)
        st.image(right_image, caption="Правое изображение", use_column_width=True)

        if st.button("Обработать"):
            left_image_mask, right_image_mask, map1, map2 = run_inference_marked_town(left_image, right_image)
            st.image(left_image_mask, caption="Левое изображение", use_column_width=True)
            st.image(right_image_mask, caption="Правое изображение", use_column_width=True)
            st.image(map1, caption="Карта глубины", use_column_width=True)
            st.image(map2, caption="Карта глубины", use_column_width=True)


            # fig_3d_1 = create_3d_plot(map1)
            # fig_3d_2 = create_3d_plot(map2)
            # st.pyplot(fig_3d_1)
            # st.pyplot(fig_3d_2)


with tab3:
    st.write("None")
