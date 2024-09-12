import os
import json
import numpy as np
import trimesh
import pyrender
from PIL import Image

def look_at(camera_position, target_position, up_vector=np.array([0, 0, 1])):
    # Calculate the forward vector (z-axis)
    forward = target_position - camera_position
    forward = forward / np.linalg.norm(forward)

    # Calculate the right vector (x-axis)
    right = np.cross(up_vector, forward)
    right = right / np.linalg.norm(right)

    # Recalculate the up vector (y-axis)
    up = np.cross(forward, right)
    up = up / np.linalg.norm(up)

    # Create the rotation matrix
    rotation_matrix = np.array([
        [right[0],      right[1],       right[2],       0],
        [up[0],         up[1],          up[2],          0],
        [-forward[0],   -forward[1],    -forward[2],       0],
        [0, 0, 0, 1]
    ])

    m = rotation_matrix[:3, :3]
    rotation_matrix[:3, :3] = m.T
    rotation_matrix[:3, -1] = camera_position

    # Create the translation matrix
    translation_matrix = np.array([
        [1, 0, 0, -camera_position[0]],
        [0, 1, 0, -camera_position[1]],
        [0, 0, 1, -camera_position[2]],
        [0, 0, 0, 1]
    ])

    # Combine the rotation and translation matrices
    #view_matrix = rotation_matrix @ translation_matrix

    return rotation_matrix

def capture_views(stl_file, num_views, output_dir):
    # Загрузка STL-файла
    mesh = trimesh.load(stl_file)
    scene = pyrender.Scene()
    mesh_pr = pyrender.Mesh.from_trimesh(mesh)
    scene.add(pyrender.Mesh.from_trimesh(mesh, smooth=False, wireframe=False))

    # Настройка камеры
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
    camera_node = scene.add(camera)
    print(np.array(mesh_pr.centroid))

    # Настройка света
    light = pyrender.PointLight(color=[.5, 0.5, 0.5], intensity=2000.0)
    light_node = scene.add(light)
    light_pos = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 10],
        [0, 0, 0, 1]
    ]
    scene.set_pose(light_node, light_pos)

    # Создание рендерера
    r = pyrender.OffscreenRenderer(viewport_width=640, viewport_height=480)

    transforms = []

    for i in range(num_views):
        # Вычисление позиции камеры
        angle = (2 * np.pi * i) / num_views
        camera_pos = np.array([
            np.cos(angle)*50, 
            np.sin(angle)*50, 
            5])
        # camera_pose = np.eye(4)
        # camera_pose[:3, 3] = camera_pos
        # camera_pose[:3, :3] = pyrender.math.look_at(camera_pos, [0, 0, 0], [0, 0, 1])
        #camera_pos += np.array(mesh_pr.centroid)
        camera_pose = look_at(camera_pos, np.array(mesh_pr.centroid)*[1, 1, 0])

        # Установка позиции камеры
        scene.set_pose(camera_node, camera_pose)

        # Рендеринг
        color, depth = r.render(scene)
        normal, _ = r._renderer._read_main_framebuffer(scene, flags=pyrender.RenderFlags.FACE_NORMALS)

        # Сохранение изображений
        Image.fromarray(color).save(os.path.join(output_dir, 'train', f'r_{i}.png'))
        Image.fromarray(color).save(os.path.join(output_dir, 'test', f'r_{i}.png'))
        Image.fromarray(color).save(os.path.join(output_dir, 'val', f'r_{i}.png'))

        Image.fromarray((depth * 255).astype(np.uint8)).save(os.path.join(output_dir, 'test', f'r_{i}_depth.png'))
        Image.fromarray(normal).save(os.path.join(output_dir, 'test', f'r_{i}normal.png'))

        # Сохранение информации о трансформации
        transform = {
            'file_path': f'./r_{i}.png',
            'transform_matrix': camera_pose.tolist()
        }
        transforms.append(transform)

    # Сохранение конфигурационных файлов
    with open(os.path.join(output_dir, 'transforms_train.json'), 'w') as f:
        json.dump({'frames': transforms[:int(0.7*num_views)]}, f)

    with open(os.path.join(output_dir, 'transforms_val.json'), 'w') as f:
        json.dump({'frames': transforms[int(0.7*num_views):int(0.85*num_views)]}, f)

    with open(os.path.join(output_dir, 'transforms_test.json'), 'w') as f:
        json.dump({'frames': transforms[int(0.85*num_views):]}, f)

# Использование функции
stl_file = './Pyramid Small.stl'
num_views = 500
output_dir = '.'

# Создание необходимых директорий
os.makedirs(os.path.join(output_dir, 'train'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'test'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'val'), exist_ok=True)

capture_views(stl_file, num_views, output_dir)