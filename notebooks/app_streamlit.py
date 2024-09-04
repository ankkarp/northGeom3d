import streamlit as st
import yaml
from PIL import Image
import plotly.graph_objects as go

# Функция для чтения YAML файла
def load_yaml(file):
    return yaml.safe_load(file)

# Заглушка для расчета диаметра окружностей
def calculate_diameters(left_image, right_image, optical_scheme):
    # Здесь должен быть код для обработки изображений
    # Возвращаем список диаметров окружностей (заглушка)
    return [5.0, 10.0, 15.0]

# Заглушка для расчета расстояний между точками
def calculate_distances(diameters):
    # Здесь должен быть код для вычисления расстояний
    # Возвращаем список расстояний между точками (заглушка)
    return [2.0, 4.0, 6.0]

# Функция для построения 3D модели
def plot_3d_model(diameters, distances):
    # Создание заглушки для 3D модели
    fig = go.Figure()

    # Пример: Создаем 3 точки в 3D пространстве
    x = [1, 2, 3]
    y = [1, 2, 3]
    z = [1, 2, 3]

    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers'))

    # Настройка отображения 3D модели
    fig.update_layout(scene=dict(
                        xaxis_title='X',
                        yaxis_title='Y',
                        zaxis_title='Z'),
                      width=700, margin=dict(r=20, b=10, l=10, t=10))
    return fig

# Интерфейс Streamlit
st.title("northGeom3d")

# Загрузка изображений и файла с оптической схемой
left_image_file = st.file_uploader("Левое изображение", type=["jpg", "jpeg", "png"])
right_image_file = st.file_uploader("Правое изображение", type=["jpg", "jpeg", "png"])
yaml_file = st.file_uploader("Загрузите YAML файл с оптической схемой", type=["yaml"])

if left_image_file and right_image_file and yaml_file:
    # Отображение загруженных изображений
    left_image = Image.open(left_image_file)
    right_image = Image.open(right_image_file)

    st.image(left_image, caption="Левое изображение", use_column_width=True)
    st.image(right_image, caption="Правое изображение", use_column_width=True)

    # Загрузка и отображение YAML файла
    optical_scheme = load_yaml(yaml_file)
    st.write("Оптическая схема:", optical_scheme)

    if st.button("Обработать"):
        # Выполнение расчетов
        diameters = calculate_diameters(left_image, right_image, optical_scheme)
        distances = calculate_distances(diameters)

        # Вывод результатов расчетов
        st.write("Диаметры окружностей:", diameters)
        st.write("Расстояния между точками:", distances)

        # Построение и вывод 3D модели
        fig = plot_3d_model(diameters, distances)
        st.plotly_chart(fig)