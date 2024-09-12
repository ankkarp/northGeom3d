from transformers import DPTImageProcessor, DPTForDepthEstimation
import torch
import numpy as np
from PIL import Image, ImageFile
import cv2
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import open3d as o3d

path = '/content/photo_2024-09-01_12-38-07.jpg'

if 'jpg' not in path:
  image = cv2.imread(path)
  cv2.imwrite('image_converted.jpg', image)
  image = Image.open('image_converted.jpg')
else: 
  image = Image.open(path)

processor = DPTImageProcessor.from_pretrained("Intel/dpt-large")
model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large")

inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    predicted_depth = outputs.predicted_depth

prediction = torch.nn.functional.interpolate(
    predicted_depth.unsqueeze(1),
    size=image.size[::-1],
    mode="bicubic",
    align_corners=False,
)

output = prediction.squeeze().cpu().numpy()
formatted = (output * 255 / np.max(output)).astype("uint8")
depth = Image.fromarray(formatted)
cv2.imwrite('depth_map.png', np.array(depth))

image_8 = cv2.imread('/content/depth_map.png', cv2.IMREAD_UNCHANGED)
image_16 = np.uint16(image_8) * 256
cv2.imwrite('depth_map16.png', image_16)

image_16 = cv2.imread('/content/depth_map16.png', cv2.IMREAD_UNCHANGED)

depth_image = o3d.geometry.Image(image_16)

height, width = image_16.shape[:2]
intrisnic = o3d.camera.PinholeCameraIntrinsic()
intrisnic.set_intrinsics(width = width, height = height,
                         fx = 500, fy = 500, 
                         cx = width/2, cy = height/2)

extrinsic = np.eye(4)

pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_image, intrisnic,
                                                      extrinsic, depth_scale = 1000, depth_trunc =3,
                                                      project_valid_depth_only = True)

vis = o3d.visualization.Visualizer()
vis.create_window(visible = False)

vis.add_geometry(pcd)
vis.poll_events()
vis.update_renderer()
vis.capture_screen_image('rendered_image.png')
vis.distroy_window()
points = np.asarray(pcd.points)