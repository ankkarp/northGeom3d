import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import torch
import requests
from diffusers import DiffusionPipeline
from PIL import Image
import open3d as o3d
from src.config import config

device = config['device']
checkpoint = config['3d_model']['repo_hf']
task = config['3d_model']['pipeline_task']
pipeline = DiffusionPipeline.from_pretrained(
    checkpoint,
    custom_pipeline=task,
    torch_dtype=torch.float16,
    trust_remote_code=True,
    ).to(device)

def create_3d_plot(depth_array):
    """
    Create a 3D plot from a given depth array.

    Parameters
    ----------
    depth_array : numpy.ndarray
        The depth array to be plotted.

    Returns
    -------
    None
    """
    
    input_image = np.array(depth_array, dtype=np.float32) / 255.0
    result = pipeline("", input_image)

    mesh = o3d.io.read_triangle_mesh(result)
    o3d.visualization.draw_geometries([mesh])
    
    
if __name__ == "__main__":
    image = Image.open(r"D:\projects\northGeom3d\docs\depth_map.png")
    depth_array = np.array(image)
    create_3d_plot(depth_array)
    
    
