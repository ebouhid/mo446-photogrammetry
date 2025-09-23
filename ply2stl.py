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
parser.add_argument('-d', '--depth', type=float, default=15,
                    help='Poisson reconstruction depth, higher = more detailed but slower and uses more RAM')
parser.add_argument('-on', '--outlier-neighbors', type=int, default=30,
                    help='Number of neighbors to analyze for outlier removal, higher = more aggressive')
parser.add_argument('-osr', '--outlier-std-ratio', type=float, default=2.0,
                    help='Standard deviation ratio for outlier removal, higher = more aggressive')
parser.add_argument('-k', '--knn', type=int, default=30,
                    help='Number of nearest neighbors for normal estimation, higher = smoother normals')
parser.add_argument('-tp', '--tangent-plane', type=int, default=100,
                    help='Number of nearest neighbors for tangent plane estimation, higher = smoother normals')

args = parser.parse_args()

with open(args.input, 'rb') as f:
    plydata = PlyData.read(f)

points = np.array(plydata['vertex'][['x', 'y', 'z']].tolist()) * args.scale

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# ajustar valores para remover outliers e ruido
cl, ind = pcd.remove_statistical_outlier(
    nb_neighbors=args.outlier_neighbors, std_ratio=args.outlier_std_ratio)
pcd = pcd.select_by_index(ind)

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamKNN(
    knn=args.knn))
pcd.orient_normals_consistent_tangent_plane(args.tangent_plane)

mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd, depth=args.depth)

bbox = pcd.get_axis_aligned_bounding_box()
mesh = mesh.crop(bbox)

mesh.compute_vertex_normals()

o3d.io.write_triangle_mesh(args.output, mesh)
