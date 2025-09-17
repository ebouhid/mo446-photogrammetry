#!/bin/bash

# Usage: ./run_colmap.sh <project_directory>
# It is necessary to have a folder named "images" inside
# the specified project directory containing all images
# to be processed.

colmap feature_extractor \
   --database_path "$1/database.db" \
   --image_path "$1/images"

colmap exhaustive_matcher \
   --database_path "$1/database.db"

mkdir "$1/sparse"

colmap mapper \
    --database_path "$1/database.db" \
    --image_path "$1/images" \
    --output_path "$1/sparse"

colmap model_converter \
    --input_path "$1/sparse/0" \
    --output_path "$1/sparse/0/points3D.ply" \
    --output_type PLY
