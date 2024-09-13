from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import plotly.graph_objs as go
import plotly.offline as pyo
import numpy as np
import trimesh
from stl import mesh
import yaml
import json
import os
import time

app = FastAPI()
DIR = os.path.dirname(__file__)

def create_3d_plot():
    # Параметры шара
    num_points = 10000  # Количество точек
    radius = 1  # Радиус шара

    # Генерация случайных точек на поверхности шара
    phi = np.random.uniform(0, np.pi * 2, num_points)
    theta = np.random.uniform(0, np.pi, num_points)

    # Преобразование сферических координат в декартовы
    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)

    res = {
        'x':x.tolist(),
        'y':y.tolist(),
        'z':z.tolist()
    }

    res['colors'] = z.tolist()

    return res

def create_stl_file():
    # Create a simple STL mesh
    vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ])
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j], :]

    # Save STL to a file
    stl_path = './data/stl_mesh.stl'
    cube.save(stl_path)
    return 'data/Back_Shell.stl'


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.post("/api/test/stl")
async def response_stl(image1: UploadFile = File(...), image2: UploadFile = File(...), yaml_file: UploadFile = File(...)):
    if not image1 or not image2 or not yaml_file:
        raise HTTPException(status_code=400, detail="Missing files")

    # Dummy processing: read YAML
    yaml_content = yaml.safe_load(yaml_file.file)

    # Generate STL file
    stl_file_path = create_stl_file()
    time.sleep(5)

    return FileResponse(stl_file_path, filename='object.stl', media_type='model/stl')

@app.post("/api/test/ply")
async def response_ply(image1: UploadFile = File(...), image2: UploadFile = File(...), yaml_file: UploadFile = File(...)):
    if not image1 or not image2 or not yaml_file:
        raise HTTPException(status_code=400, detail="Missing files")

    # Dummy processing: read YAML
    yaml_content = yaml.safe_load(yaml_file.file)

    # Generate 3D plot
    plot_html = create_3d_plot()
    time.sleep(2)

    return JSONResponse(content=plot_html)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')