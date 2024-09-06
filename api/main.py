from flask import Flask, request, jsonify, send_file
import plotly.graph_objs as go
import plotly.offline as pyo
import numpy as np
from stl import mesh
import yaml
import json
import io

app = Flask(__name__)

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

    # Convert STL to JSON format
    stl_io = './data/stl_mesh.stl'
    cube.save(stl_io)
    stl_io = open(stl_io, 'rb')
    stl_io.seek(0)
    return stl_io

@app.route('/api/test/stl', methods=['POST'])
def response_stl():
    if 'image1' not in request.files or 'image2' not in request.files or 'yaml_file' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']
    yaml_file = request.files['yaml_file']

    

    # Dummy processing: read YAML
    yaml_content = yaml.safe_load(yaml_file)

    # Generate 3D plot and STL file
    stl_file = create_stl_file()

    return send_file(stl_file, download_name='object.stl')


@app.route('/api/test/ply', methods=['POST'])
def response_ply():
    if 'image1' not in request.files or 'image2' not in request.files or 'yaml_file' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']
    yaml_file = request.files['yaml_file']

    

    # Dummy processing: read YAML
    yaml_content = yaml.safe_load(yaml_file)

    # Generate 3D plot and STL file
    plot_html = create_3d_plot()

    return jsonify({'plot_html': plot_html})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=420)