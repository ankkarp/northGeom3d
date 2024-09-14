import bpy
import math
import yaml
import argparse

config_file = "config.yaml"

def load_config(path: str):
    """
    Загрузка настроек из YAML файла.
    """
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_camera(camera_conf):
    """
    Загрузка параметров камеры
    """
    camera = bpy.data.objects[camera_conf['name']]
    camera.location = camera_conf['location']
    rotation = camera_conf['rotation']

    camera.rotation_euler = (
        math.radians(rotation[0]),
        math.radians(rotation[1]),
        math.radians(rotation[2]),
    )
    return camera


def main(path, config, figure):
    """
        Основная функци, принимает параметры
        и циклом создает рендер
    """
    frames = config['frames']
    x_offset = config['cameras']['camera_1']['rotation'][2]
    radius = 0

    # Открываем файл .blend
    bpy.ops.wm.open_mainfile(filepath=path)
    obj = bpy.data.objects[figure]
    camera_1 = load_camera(config['cameras']['camera_1'])
    camera_2 = load_camera(config['cameras']['camera_2'])

    # Устанавливаем начальное положение камеры
    bpy.context.scene.frame_start = config['frame_start']
    bpy.context.scene.frame_end = frames

    # Применяем трек к объекту для обеих камер
    camera_1_constraint = camera_1.constraints.new(type='TRACK_TO')
    camera_1_constraint.target = obj
    camera_1_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    camera_1_constraint.up_axis = 'UP_Y'

    camera_2_constraint = camera_2.constraints.new(type='TRACK_TO')
    camera_2_constraint.target = obj
    camera_2_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    camera_2_constraint.up_axis = 'UP_Y'

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
        bpy.context.scene.render.filepath = f"{config['output_path']}_{figure}_camera_1_{frame:03d}.png"
        bpy.ops.render.render(write_still=True)

        # Рендеринг с камеры 2
        bpy.context.scene.camera = camera_2
        bpy.context.scene.render.filepath = f"{config['output_path']}_{figure}_camera_2_{frame:03d}.png"
        bpy.ops.render.render(write_still=True)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--figure', type=str, help='Фигура для рендеринга')
    args = parser.parse_args()
    file_path = args.figure
    figure = file_path.split('/')[-1].split('.')[0]
    config_data = load_config(config_file)
    print(config_data)
    main(file_path, config_data, figure)

