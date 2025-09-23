import argparse
import numpy as np
import open3d as o3d

from plyfile import PlyData

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str,
                    required=True, help='Input PLY file')
parser.add_argument('-o', '--output', type=str,
                    required=True, help='Output STL path')
parser.add_argument('-s', '--scale', type=float, default=1.0,
                    help='Scaling factor (bump it up if the model is too small)')

args = parser.parse_args()

with open(args.input, 'rb') as f:
    plydata = PlyData.read(f)

points = np.array(plydata['vertex'][['x', 'y', 'z']].tolist()) * args.scale

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# ajustar valores para remover outliers e ruido
cl, ind = pcd.remove_statistical_outlier(nb_neighbors=30, std_ratio=2.0)
pcd = pcd.select_by_index(ind)

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamKNN(
    knn=30))  # maior = normais mais suaves
# empiricamente 100 fica melhor. nao pergunte!
pcd.orient_normals_consistent_tangent_plane(100)

mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd, depth=15)  # mais depth = maior resolucao, mas é mais lento e usa muita RAM

bbox = pcd.get_axis_aligned_bounding_box()
mesh = mesh.crop(bbox)

mesh.compute_vertex_normals()

o3d.io.write_triangle_mesh(args.output, mesh)
