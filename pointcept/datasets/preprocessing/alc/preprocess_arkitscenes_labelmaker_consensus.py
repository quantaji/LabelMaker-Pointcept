import warnings

import torch

warnings.filterwarnings("ignore", category=DeprecationWarning)

import argparse
import glob
import json
import multiprocessing as mp
import os
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from pathlib import Path

import numpy as np
import open3d as o3d
import pandas as pd
import plyfile
from labelmaker import label_mappings
from labelmaker.label_data import get_wordnet
from labelmaker.scannet_200_labels import VALID_CLASS_IDS_200
from tqdm import tqdm

IGNORE_INDEX = -1


def get_wordnet_to_scannet200_mapping():
    table = pd.read_csv(Path(os.path.dirname(os.path.realpath(label_mappings.__file__))) / "mappings" / "label_mapping.csv")
    wordnet = get_wordnet()
    wordnet_keys = [x["name"] for x in wordnet]
    mapping = {}
    for row in table.index:
        if table["wnsynsetkey"][row] not in wordnet_keys:
            continue
        scannet_id = table.loc[row, "id"]
        wordnet199_id = next(x for x in wordnet if x["name"] == table["wnsynsetkey"][row])["id"]

        if scannet_id in VALID_CLASS_IDS_200:
            mapping.setdefault(wordnet199_id, set()).add(scannet_id)

    wn199_size = np.array([x["id"] for x in wordnet]).max() + 1
    mapping_array = np.zeros(shape=(wn199_size,), dtype=np.uint16)
    for wordnet199_id in mapping.keys():
        mapping_array[wordnet199_id] = min(mapping[wordnet199_id])

    return mapping_array


def get_wordnet_compact_mapping():
    wordnet_info = get_wordnet()[1:]
    wordnet_info = sorted(wordnet_info, key=lambda x: x["id"])

    class2id = np.array([item["id"] for item in wordnet_info])
    id2class = np.array([IGNORE_INDEX] * (class2id.max() + 1))
    for class_, id_ in enumerate(class2id):
        id2class[id_] = class_

    return class2id, id2class


def get_scannet200_compact_mapping():
    class2id = np.array(VALID_CLASS_IDS_200)
    id2class = np.array([IGNORE_INDEX] * (class2id.max() + 1))
    for class_, id_ in enumerate(VALID_CLASS_IDS_200):
        id2class[id_] = class_

    return class2id, id2class


def read_plypcd(filepath):
    """Read ply file and return it as numpy array. Returns None if emtpy."""

    with open(filepath, "rb") as f:
        plydata = plyfile.PlyData.read(f)
    if plydata.elements:
        data = plydata.elements[0].data
        coords = np.array([data["x"], data["y"], data["z"]], dtype=np.float32).T

        colors = None
        if ({"red", "green", "blue"} - set(data.dtype.names)) == set():
            colors = np.array([data["red"], data["green"], data["blue"]], dtype=np.uint8).T

        normals = None
        if ({"nx", "ny", "nz"} - set(data.dtype.names)) == set():
            normals = np.array([data["nx"], data["ny"], data["nz"]], dtype=np.float32).T

        return coords, colors, normals


def handle_process(
    scene_dir: str,
    output_path: str,
    label_mapping,
    wn199_id2class,
    scannet200_id2class,
):
    scene_dir = Path(scene_dir)

    print(f"Processing: {scene_dir.name} in {scene_dir.parent.name}")

    coords, colors, normals = read_plypcd(str(scene_dir / "pcd_downsampled.ply"))
    save_dict = dict(
        coord=coords,
        color=colors,
        scene_id=scene_dir.name,
        normal=normals,
    )

    label_file = scene_dir / "labels_downsampled.txt"
    wordnet_label = np.loadtxt(str(label_file), dtype=np.uint8).reshape(-1, 1)
    scannet200_label = label_mapping[wordnet_label]
    save_dict["semantic_pseudo_gt_wn199"] = wn199_id2class[wordnet_label]
    save_dict["semantic_pseudo_gt_scannet200"] = scannet200_id2class[scannet200_label]

    torch.save(save_dict, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_root",
        required=True,
        help="Path to the ScanNet dataset containing scene folders",
    )
    parser.add_argument(
        "--output_root",
        required=True,
        help="Output path where train/val folders will be located",
    )
    config = parser.parse_args()

    # Create output directories
    train_output_dir = os.path.join(config.output_root, "train")
    os.makedirs(train_output_dir, exist_ok=True)
    val_output_dir = os.path.join(config.output_root, "val")
    os.makedirs(val_output_dir, exist_ok=True)

    # Load label map
    wn_scannet200_label_mapping = get_wordnet_to_scannet200_mapping()
    _, wn199_id2class = get_wordnet_compact_mapping()
    _, scannet200_id2class = get_scannet200_compact_mapping()

    scene_dirs = []
    output_paths = []

    # Load train/val splits
    train_folder = Path(config.dataset_root) / "Training"
    train_scene_names = os.listdir(str(train_folder))
    for scene in tqdm(train_scene_names):
        file_path = train_folder / scene / "pcd_downsampled.ply"
        if file_path.exists() and os.path.getsize(str(file_path)) <= 50 * 1024 * 1024:
            scene_dirs.append(str(train_folder / scene))
            output_paths.append(str(Path(config.output_root) / "train" / f"{scene}.pth"))

    val_folder = Path(config.dataset_root) / "Validation"
    val_scene_names = os.listdir(str(val_folder))
    for scene in tqdm(val_scene_names):
        file_path = val_folder / scene / "pcd_downsampled.ply"
        if file_path.exists() and os.path.getsize(str(file_path)) <= 50 * 1024 * 1024:
            scene_dirs.append(str(val_folder / scene))
            output_paths.append(str(Path(config.output_root) / "val" / f"{scene}.pth"))

    # Preprocess data.
    print("Processing scenes...")
    pool = ProcessPoolExecutor(max_workers=mp.cpu_count())
    print(f"Using {mp.cpu_count()} cores")
    # pool = ProcessPoolExecutor(max_workers=1)
    _ = list(
        pool.map(
            handle_process,
            scene_dirs,
            output_paths,
            repeat(wn_scannet200_label_mapping),
            repeat(wn199_id2class),
            repeat(scannet200_id2class),
        )
    )
