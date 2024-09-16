import bpy
import math
import yaml
import argparse
from src.augmentation_node import Material
from src.camera import Camera_node
from src.derph_node import Depth_node


config_file = "config.yaml"

def load_config(path: str):
    """
        Загрузка настроек из YAML файла.
    """
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def render_from_cameras(camera_1: dict,
                        camera_2: dict,
                        config: dict,
                        figure: str,
                        frames: int,
                        radius: float,
                        x_offset: float,
                        cycle :int, output_depth):
    """
        Функция создает рендеринг по установленным параметрам
    """
    for frame in range(frames):
        # Рассчитываем угол вращения
        angle = 2 * math.pi * (frame / frames)

        # Позиция первой камеры (слева)
        camera_1.location.x = radius * math.cos(angle - math.radians(x_offset))
        camera_1.location.y = radius * math.sin(angle - math.radians(x_offset))
        camera_1.location.z = 0

        # Позиция второй камеры (справа)
        camera_2.location.x = radius * math.cos(angle + math.radians(x_offset))
        camera_2.location.y = radius * math.sin(angle + math.radians(x_offset))
        camera_2.location.z = 0

        # Устанавливаем ключевые кадры для положения камер
        camera_1.keyframe_insert(data_path="location", frame=frame)
        camera_2.keyframe_insert(data_path="location", frame=frame)

        # Устанавливаем текущий кадр
        bpy.context.scene.frame_set(frame)

        # Рендеринг с камеры 1
        bpy.context.scene.camera = camera_1
        bpy.context.scene.render.filepath = f"./{config['render_output_path']}_{figure}_{cycle}_camera_1_{frame:03d}.png"
        output_depth.file_slots[0].path = f"./{config['depth_output_path']}_{figure}_{cycle}_camera_1_depth_"
        bpy.ops.render.render(write_still=True)

        # Рендеринг с камеры 2
        bpy.context.scene.camera = camera_2
        bpy.context.scene.render.filepath = f"{config['render_output_path']}_{figure}_{cycle}_camera_2_{frame:03d}.png"
        output_depth.file_slots[0].path = f"{config['depth_output_path']}_{figure}_{cycle}_camera_2_depth_"
        bpy.ops.render.render(write_still=True)


def main(path, config, figure):
    """
        Основная функция, принимает параметры
        и циклом создает рендер и карты глубин
        заданное количество разза цикл
    """
    frames_in_cycle = config['frames_in_cycle']
    cycles = config['cycles']
    for cycle in range(cycles):
        x_offset = config['cameras']['camera_1']['rotation'][2]
        radius = config['cameras']['camera_1']['location'][1]

        # Открываем файл .blend
        bpy.ops.wm.open_mainfile(filepath=path)
        obj = bpy.data.objects[figure]
        augmentation_node = Material(config)
        augmentation_node.create_material(obj)

        # карта глубины
        deth_node = Depth_node(config['depth_map'])
        output_depth =deth_node.create_depth()

        # Устанавливаем начальное положение камеры
        bpy.context.scene.frame_start = config['frame_start']
        bpy.context.scene.frame_end = frames_in_cycle

        camera_1_handler = Camera_node(config['cameras']['camera_1'])
        camera_1 = camera_1_handler.load_camera()
        camera_1_constraint = camera_1_handler.load_constant(obj)

        camera_2_handler = Camera_node(config['cameras']['camera_2'])
        camera_2 = camera_2_handler.load_camera()
        camera_2_constraint = camera_2_handler.load_constant(obj)

        render_from_cameras(camera_1, camera_2, config, figure, frames_in_cycle, radius, x_offset, cycle, output_depth)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--figure', type=str, help='Фигура для рендеринга')
    args = parser.parse_args()
    file_path = args.figure
    figure = file_path.split('/')[-1].split('.')[0]
    config_data = load_config(config_file)
    print(config_data)
    main(file_path, config_data, figure)

