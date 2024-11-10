"""
Preprocessing Script for Matterport3D (Unzipping)
adatpted from https://github.com/pengsongyou/openscene/blob/main/scripts/preprocess/preprocess_3d_matterport.py

Author: Chongjie Ye (chongjieye@link.cuhk.edu.cn)
Modified by: Xiaoyang Wu (xiaoyang.wu.cs@gmail.com)
Please cite our work if the code is helpful to you.
"""

import os
import argparse
import glob
import plyfile
import numpy as np
import pandas as pd
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from pathlib import Path
import torch

MATTERPORT_CLASS_REMAP = np.zeros(41)
MATTERPORT_CLASS_REMAP[1] = 1
MATTERPORT_CLASS_REMAP[2] = 2
MATTERPORT_CLASS_REMAP[3] = 3
MATTERPORT_CLASS_REMAP[4] = 4
MATTERPORT_CLASS_REMAP[5] = 5
MATTERPORT_CLASS_REMAP[6] = 6
MATTERPORT_CLASS_REMAP[7] = 7
MATTERPORT_CLASS_REMAP[8] = 8
MATTERPORT_CLASS_REMAP[9] = 9
MATTERPORT_CLASS_REMAP[10] = 10
MATTERPORT_CLASS_REMAP[11] = 11
MATTERPORT_CLASS_REMAP[12] = 12
MATTERPORT_CLASS_REMAP[14] = 13
MATTERPORT_CLASS_REMAP[16] = 14
MATTERPORT_CLASS_REMAP[22] = 21  # DIFFERENCE TO SCANNET!
MATTERPORT_CLASS_REMAP[24] = 15
MATTERPORT_CLASS_REMAP[28] = 16
MATTERPORT_CLASS_REMAP[33] = 17
MATTERPORT_CLASS_REMAP[34] = 18
MATTERPORT_CLASS_REMAP[36] = 19
MATTERPORT_CLASS_REMAP[39] = 20

MATTERPORT_LABELS_21 = (
    "wall",
    "floor",
    "cabinet",
    "bed",
    "chair",
    "sofa",
    "table",
    "door",
    "window",
    "bookshelf",
    "picture",
    "counter",
    "desk",
    "curtain",
    "refrigerator",
    "shower curtain",
    "toilet",
    "sink",
    "bathtub",
    "other",
    "ceiling",
)
MATTERPORT_ALLOWED_NYU_CLASSES = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    14,
    16,
    22,
    24,
    28,
    33,
    34,
    36,
    39,
]


def handle_process(
    mesh_path,
    output_path,
    mapping_nyu40,
    mapping_mpcat40,
    mapping_os40,
    mapping_os80,
    mapping_os160,
    train_scenes,
    val_scenes,
):
    # Get the scene id and region name from the mesh path
    scene_id = Path(mesh_path).parent.parent.name
    region_id = Path(mesh_path).stem.removeprefix("region")
    data_name = f"{scene_id}_{int(region_id):02d}"

    output_path = Path(output_path)
    # Check which split the scene belongs to (train, val, or test)
    if scene_id in train_scenes:
        output_folder = output_path / "train" / data_name
        split = "train"
    elif scene_id in val_scenes:
        output_folder = output_path / "val" / data_name
        split = "val"
    else:
        output_folder = output_path / "test" / data_name
        split = "test"

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    print(f"Processing: {data_name} in {split}")

    # Load the vertex data
    with open(mesh_path, "rb") as f:
        plydata = plyfile.PlyData.read(f)
    vertex_data = plydata["vertex"].data

    # Get the coordinates, colors, and normals from the vertex data
    coords = np.vstack([vertex_data["x"], vertex_data["y"], vertex_data["z"]]).T

    # Load the face data
    face_data = plydata["face"].data
    category_id = face_data["category_id"]

    # Replace -1 with 0 in category_id
    category_id[category_id == -1] = 0

    # Map the labels according to NYU40ID
    mapped_labels_nyu40 = mapping_nyu40[category_id]
    mapped_labels = mapped_labels_nyu40.copy()

    # Replace labels not in MATTERPORT_ALLOWED_NYU_CLASSES with 0
    mapped_labels[np.logical_not(np.isin(mapped_labels, MATTERPORT_ALLOWED_NYU_CLASSES))] = 0

    # Remap the labels to ScanNet 20 categories + ceiling
    remapped_labels = MATTERPORT_CLASS_REMAP[mapped_labels].astype(int)  # scannet20 ext

    mapped_labels_mpcat40 = mapping_mpcat40[category_id]
    mapped_labels_openscene_40 = mapping_os40[category_id]
    mapped_labels_openscene_80 = mapping_os80[category_id]
    mapped_labels_openscene_160 = mapping_os160[category_id]

    # Calculate per-vertex labels
    triangles = face_data["vertex_indices"]
    vertex_labels_cat_id = np.zeros((coords.shape[0], 1660), dtype=np.int32)
    # vertex_labels_nyu40 = np.zeros((coords.shape[0], 41), dtype=np.int32)
    vertex_labels_scannet20_ext = np.zeros((coords.shape[0], 22), dtype=np.int32)
    vertex_labels_mpcat40 = np.zeros((coords.shape[0], 42), dtype=np.int32)
    vertex_labels_os40 = np.zeros((coords.shape[0], 41), dtype=np.int32)
    vertex_labels_os80 = np.zeros((coords.shape[0], 81), dtype=np.int32)
    vertex_labels_os160 = np.zeros((coords.shape[0], 161), dtype=np.int32)
    # calculate per-vertex labels
    for row_id in range(triangles.shape[0]):
        for i in range(3):
            vertex_labels_scannet20_ext[triangles[row_id][i], remapped_labels[row_id]] += 1

            vertex_labels_cat_id[triangles[row_id][i], category_id[row_id]] += 1
            # vertex_labels_nyu40[triangles[row_id][i], mapped_labels_nyu40[row_id]] += 1
            vertex_labels_mpcat40[triangles[row_id][i], mapped_labels_mpcat40[row_id]] += 1
            vertex_labels_os40[triangles[row_id][i], mapped_labels_openscene_40[row_id]] += 1
            vertex_labels_os80[triangles[row_id][i], mapped_labels_openscene_80[row_id]] += 1
            vertex_labels_os160[triangles[row_id][i], mapped_labels_openscene_160[row_id]] += 1

    # Get the most frequent label for each vertex
    vertex_labels_scannet20_ext = np.argmax(vertex_labels_scannet20_ext, axis=1)
    vertex_labels_scannet20_ext -= 1

    vertex_labels_cat_id = np.argmax(vertex_labels_cat_id, axis=1)
    # vertex_labels_nyu40 = np.argmax(vertex_labels_nyu40, axis=1)
    vertex_labels_mpcat40 = np.argmax(vertex_labels_mpcat40, axis=1)
    vertex_labels_os40 = np.argmax(vertex_labels_os40, axis=1)
    vertex_labels_os80 = np.argmax(vertex_labels_os80, axis=1)
    vertex_labels_os160 = np.argmax(vertex_labels_os160, axis=1)

    np.savetxt(output_folder / "scannet20_ext.txt", vertex_labels_scannet20_ext, fmt="%d")

    np.savetxt(output_folder / "scannet20_ext.txt", vertex_labels_cat_id, fmt="%d")
    # np.savetxt(output_folder / "nyu40.txt", vertex_labels_nyu40, fmt="%d")
    np.savetxt(output_folder / "mpcat40.txt", vertex_labels_mpcat40, fmt="%d")
    np.savetxt(output_folder / "openscene_cat40.txt", vertex_labels_os40, fmt="%d")
    np.savetxt(output_folder / "openscene_cat80.txt", vertex_labels_os80, fmt="%d")
    np.savetxt(output_folder / "openscene_cat160.txt", vertex_labels_os160, fmt="%d")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_root",
        required=True,
        help="Path to the Matterport3D dataset containing scene folders",
    )
    parser.add_argument(
        "--output_root",
        required=True,
        help="Output path where train/val folders will be located",
    )
    parser.add_argument(
        "--num_workers",
        default=mp.cpu_count(),
        type=int,
        help="Num workers for preprocessing.",
    )
    opt = parser.parse_args()
    meta_root = Path(os.path.dirname(__file__)) / "../pointcept/datasets/preprocessing/matterport3d/meta_data"
    curr_root = Path(os.path.dirname(__file__))

    # Load label map
    category_mapping = pd.read_csv(
        curr_root / "matterport3d_with_openscene_label.tsv",
        sep="\t",
        header=0,
    )
    mapping_nyu40 = np.insert(category_mapping[["nyu40id"]].to_numpy().astype(int).flatten(), 0, 0, axis=0)
    mapping_mpcat40 = np.insert(category_mapping[["mpcat40index"]].to_numpy().astype(int).flatten(), 0, 0, axis=0)
    mapping_os40 = np.insert(category_mapping[["OpenSceneMatterport3D40Index"]].to_numpy().astype(int).flatten(), 0, 0, axis=0)
    mapping_os80 = np.insert(category_mapping[["OpenSceneMatterport3D80Index"]].to_numpy().astype(int).flatten(), 0, 0, axis=0)
    mapping_os160 = np.insert(category_mapping[["OpenSceneMatterport3D160Index"]].to_numpy().astype(int).flatten(), 0, 0, axis=0)

    # Load train/val splits
    with open(meta_root / "scenes_train.txt") as train_file:
        train_scenes = train_file.read().splitlines()
    with open(meta_root / "scenes_val.txt") as val_file:
        val_scenes = val_file.read().splitlines()
    with open(meta_root / "scenes_test.txt") as test_file:
        test_scenes = test_file.read().splitlines()

    # Create output directories
    os.makedirs(opt.output_root, exist_ok=True)
    train_output_dir = os.path.join(opt.output_root, "train")
    os.makedirs(train_output_dir, exist_ok=True)
    val_output_dir = os.path.join(opt.output_root, "val")
    os.makedirs(val_output_dir, exist_ok=True)
    test_output_dir = os.path.join(opt.output_root, "test")
    os.makedirs(test_output_dir, exist_ok=True)

    # Load scene paths
    scene_paths = sorted(glob.glob(os.path.join(opt.dataset_root, "v1", "scans", "*", "region_segmentations", "*.ply")))

    # Preprocess data.
    pool = ProcessPoolExecutor(max_workers=opt.num_workers)
    print("Processing scenes...")
    _ = list(
        pool.map(
            handle_process,
            scene_paths,
            repeat(opt.output_root),
            repeat(mapping_nyu40),
            repeat(mapping_mpcat40),
            repeat(mapping_os40),
            repeat(mapping_os80),
            repeat(mapping_os160),
            repeat(train_scenes),
            repeat(val_scenes),
        )
    )
