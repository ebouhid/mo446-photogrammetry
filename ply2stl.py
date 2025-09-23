import os
import argparse

from plyfile import PlyData, PlyElement
from stl import mesh

import numpy as np

from scipy.spatial import ConvexHull

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='Input PLY file')
parser.add_argument('-o', '--output', type=str, required=True, help='Output STL path')
args = parser.parse_args()

with open(args.input, 'rb') as f:
    plydata = PlyData.read(f)

vertices = np.array(plydata['vertex'][['x', 'y', 'z']].tolist())

hull = ConvexHull(vertices)

m = mesh.Mesh(np.zeros(len(hull.simplices), dtype=mesh.Mesh.dtype))

for i, simplex in enumerate(hull.simplices):
    for j in range(len('xyz')):
        m.vectors[i][j] = vertices[simplex[j]]

m.save(args.output)
