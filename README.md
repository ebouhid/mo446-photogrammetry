# COLMAP 3D Reconstruction Pipeline

This project contains a COLMAP-based 3D reconstruction pipeline using the `run.sh` script.

## Overview

The `run.sh` script automates the complete COLMAP photogrammetry pipeline, from feature extraction to 3D point cloud generation.

## Usage

```bash
./run.sh <project_directory>
```

**Requirements:**
- The specified project directory must contain a folder named `images` with all images to be processed
- COLMAP must be installed on your system


### Build COLMAP from Source

```bash
# Clone the official repository
git clone https://github.com/colmap/colmap.git
cd colmap

# Create a build directory
mkdir build
cd build

# Configure the build with Ninja
# CRITICAL: Specify the CUDA architecture for your GPU (e.g., RTX 3090 is 8.6)
cmake .. -GNinja -DCMAKE_CUDA_ARCHITECTURES=86

# Compile the code using Ninja
ninja

# Install COLMAP system-wide
sudo ninja install
```

**Note:** Adjust the `DCMAKE_CUDA_ARCHITECTURES` value according to your GPU model.

## What the Script Does

The script performs the following COLMAP operations:

1. **Feature Extraction** - Detects and extracts keypoints from all images
2. **Feature Matching** - Matches features between image pairs using exhaustive matching
3. **3D Reconstruction** - Creates sparse 3D model from matched features
4. **Model Export** - Converts the 3D model to PLY format for visualization

## Output

After successful execution, you'll find:
- `database.db` - COLMAP database with features and matches
- `<project_directory>/sparse/0/` - Sparse 3D reconstruction files
- `<project_directory>/sparse/0/points3D.ply` - 3D point cloud in PLY format

## COLMAP Installation

These steps compile COLMAP from source and only need to be done once.

### Install Dependencies

On Ubuntu, install COLMAP's dependencies:

```bash
sudo apt-get install \
    git \
    cmake \
    ninja-build \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev
```

## Example

```bash
# Process images in the buddha dataset
./run.sh dataset_buddha/buddha

# Process images in the temple ring dataset  
./run.sh dataset_templeRing
```
