# northGeom3d

## Описание
`northGeom3d` - проект по измерению объектов в рамках хакатона ИТМО и Ai Talent Hub - AI Product Hack

## Возможности
- **Расстояние между точками, диаметр окружности:** Измерение расстояния между черными точками и измерение диаметра белых окружностей
- **Расстояние между точками:** Измерение расстояния между черными точками (маркерные башни)
- **Листовой прокат:** (TODO: Road map)

## Установка

1. Клонирование проекта:
    ```bash
    git clone https://github.com/ankkarp/northGeom3d.git
    cd northgeom3d
    ```

2. Установка зависимостей:
    ```bash
    pip install -r requirements.txt
    ```

## Использование

1. Запуск приложения:
    ```bash
    streamlit run app.py --server.port=<НОМЕР_ПОРТА>
    ```

2. Откройте приложение по адресу `http://localhost:<НОМЕР_ПОРТА>`.

3. Выберите вкладку с нужным режимом

4. Загрузите изображения

5. Нажмите кнопку "Обработать"


## Acknowledgements
- Оценка глубины модель HuggingFace: `depth-anything/Depth-Anything-V2-base-hf`
- Библиотеки: Streamlit, Pillow, OpenCV, NumPy, Transformers, Torch
