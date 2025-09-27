#!/bin/bash

# Usage: ./gen-ply.sh <project_directory>
# It is necessary to have a folder named "images" inside
# the specified project directory containing all images
# to be processed.

colmap feature_extractor \
   --database_path "$1/database.db" \
   --image_path "$1/images" \
   --SiftExtraction.estimate_affine_shape=true \
   --SiftExtraction.domain_size_pooling=true \

colmap sequential_matcher \
   --database_path "$1/database.db" \
   --SiftMatching.max_ratio=0.7 \
   --SiftMatching.max_distance=0.7 \

mkdir "$1/sparse"

colmap mapper \
    --database_path "$1/database.db" \
    --image_path "$1/images" \
    --output_path "$1/sparse"

colmap model_converter \
    --input_path "$1/sparse/0" \
    --output_path "$1/sparse/0/points3D.ply" \
    --output_type PLY

mkdir -p "$1/dense"

colmap image_undistorter \
    --image_path "$1/images" \
    --input_path "$1/sparse/0" \
    --output_path "$1/dense" \
    --output_type COLMAP

colmap patch_match_stereo \
    --workspace_path "$1/dense" \
    --workspace_format COLMAP \
    --PatchMatchStereo.geom_consistency=true \
    --PatchMatchStereo.gpu_index=0 \
	--PatchMatchStereo.max_image_size 1000 \
	--PatchMatchStereo.cache_size 6

colmap stereo_fusion \
    --workspace_path "$1/dense" \
    --output_path "$1/dense/fused.ply"
