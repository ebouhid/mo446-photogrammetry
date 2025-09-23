# THIS VERSION USES PYVISTA TO PERFORM INTERPOLATION INSTEAD OF A CONVEX HULL.

import os
import argparse

from plyfile import PlyData, PlyElement

import pyvista as pv

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='Input PLY file')
parser.add_argument('-o', '--output', type=str, required=True, help='Output STL path')
parser.add_argument('-a', '--alpha', type=float, default=2.0, help='Interpolation alpha value')
args = parser.parse_args()

with open(args.input, 'rb') as f:
    plydata = PlyData.read(f)

vertices = np.array(plydata['vertex'][['x', 'y', 'z']].tolist()) * 10

cloud = pv.PolyData(vertices)
vol = cloud.delaunay_3d(alpha=args.alpha)
shell = vol.extract_surface().extract_largest()
shell.save(args.output, binary=True)
