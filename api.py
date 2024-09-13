from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, Response
from fastapi.encoders import jsonable_encoder
import plotly.graph_objs as go
import plotly.offline as pyo
import numpy as np
import trimesh
from stl import mesh
import yaml
import json
import os
from src.depth_estimation import run_inference_marked_grid, run_inference_marked_town
import base64
from PIL import Image

app = FastAPI()
DIR = os.path.dirname(__file__)


@app.post("/api/circle_distance")
async def response_circle(left_image: UploadFile = File(...), right_image: UploadFile = File(...)):
    if not left_image or not right_image:
        raise HTTPException(status_code=400, detail="Missing files")
    
    left_image = Image.open(left_image.file)
    right_image = Image.open(right_image.file)

    left_image_mask, right_image_mask, map1, map2 = run_inference_marked_grid(left_image, right_image)

    res = {
        'left_image':left_image_mask.tolist(),
        'right_image':right_image_mask.tolist(),
        'left_map':map1.tolist(),
        'right_map':map2.tolist(),
    }

    res = jsonable_encoder(res)

    return JSONResponse(content=res)


@app.post("/api/distance")
async def response_distance(left_image: UploadFile = File(...), right_image: UploadFile = File(...)):
    if not left_image or not right_image:
        raise HTTPException(status_code=400, detail="Missing files")

    left_image = Image.open(left_image.file)
    right_image = Image.open(right_image.file)

    left_image_mask, right_image_mask, map1, map2 = run_inference_marked_town(left_image, right_image)

    res = {
        'left_image':left_image_mask.tolist(),
        'right_image':right_image_mask.tolist(),
        'left_map':map1.tolist(),
        'right_map':map2.tolist(),
    }

    res = jsonable_encoder(res)

    return JSONResponse(content=res)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=1337)