import math

import bpy

class Camera:
    """    Класс создания камеры.
    """
    def __init__(self, camera_config: dict):
        # Создаем новый материал
        self.config = camera_config
        self.camera = None

    def load_camera(self):
        """
        Загрузка параметров камеры
        """
        self.camera = bpy.data.objects[self.config['name']]
        self.camera.location = self.config['location']
        rotation = self.config['rotation']

        self.camera.rotation_euler = (
            math.radians(rotation[0]),
            math.radians(rotation[1]),
            math.radians(rotation[2]),
        )
        return self.camera

    def load_constant(self, object):
        # Применяем трек к объекту для обеих камер
        camera_constraint = self.camera.constraints.new(type='TRACK_TO')
        camera_constraint.target = object
        camera_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        camera_constraint.up_axis = 'UP_Y'
        return  camera_constraint