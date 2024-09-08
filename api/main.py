from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import plotly.graph_objs as go
import plotly.offline as pyo
import numpy as np
from stl import mesh
import yaml
import json

app = FastAPI()

def create_3d_plot():
    # Create a simple 3D plot
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    z = np.sin(np.sqrt(x**2 + y**2))

    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    plot_html = pyo.plot(fig, include_plotlyjs=True, output_type='div')
    return plot_html

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
    return stl_path

@app.post("/api/test/stl")
async def response_stl(image1: UploadFile = File(...), image2: UploadFile = File(...), yaml_file: UploadFile = File(...)):
    if not image1 or not image2 or not yaml_file:
        raise HTTPException(status_code=400, detail="Missing files")

    # Dummy processing: read YAML
    yaml_content = yaml.safe_load(yaml_file.file)

    # Generate STL file
    stl_file_path = create_stl_file()

    return FileResponse(stl_file_path, filename='object.stl')

@app.post("/api/test/ply")
async def response_ply(image1: UploadFile = File(...), image2: UploadFile = File(...), yaml_file: UploadFile = File(...)):
    if not image1 or not image2 or not yaml_file:
        raise HTTPException(status_code=400, detail="Missing files")

    # Dummy processing: read YAML
    yaml_content = yaml.safe_load(yaml_file.file)

    # Generate 3D plot
    plot_html = create_3d_plot()

    return HTMLResponse(content=plot_html)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')