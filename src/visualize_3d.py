import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import torch
import requests
from diffusers import DiffusionPipeline
from PIL import Image
import open3d as o3d

def create_3d_plot(depth_array):

    pipeline = DiffusionPipeline.from_pretrained(
    "dylanebert/LGM-full",
    custom_pipeline="dylanebert/LGM-full",
    torch_dtype=torch.float16,
    trust_remote_code=True,
    ).to("cuda")

    
    input_image = np.array(depth_array, dtype=np.float32) / 255.0
    result = pipeline("", input_image)

    mesh = o3d.io.read_triangle_mesh(result)
    o3d.visualization.draw_geometries([mesh])
    
    

if __name__ == "__main__":
    image = Image.open(r"D:\projects\northGeom3d\docs\depth_map.png")
    depth_array = np.array(image)
    create_3d_plot(depth_array)
    
    
