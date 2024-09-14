import plotly.graph_objs as go
import numpy as np
from PIL import Image
from transformers import pipeline
import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
device = "cuda"
checkpoint = "depth-anything/Depth-Anything-V2-base-hf"
pipe = pipeline("depth-estimation", model=checkpoint, device=device)
image_left = Image.open(r"D:\projects\northGeom3d\notebooks\Cam1_10.jpg").convert('RGB')


predictions_left = pipe(image_left)
depth_array = np.array(predictions_left["depth"])

## Create a meshgrid for x and y coordinates
x = np.linspace(0, depth_array.shape[1], depth_array.shape[1])
y = np.linspace(0, depth_array.shape[0], depth_array.shape[0])
x, y = np.meshgrid(x, y)

# Use the depth values as z coordinates, normalizing for better visualization
z = depth_array / np.max(depth_array)

# Plotting the 3D surface
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Create the 3D surface plot
ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')

# Set labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Depth (Z axis)')
ax.set_title('3D Model from Depth Map')

plt.show()