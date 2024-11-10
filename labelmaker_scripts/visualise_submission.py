import glob
import json
import os
import shutil
from pathlib import Path

import numpy as np

import open3d as o3d
import pyviz3d.visualizer as viz
from metrics import ConfusionMatrix, IoU
from pointcept.datasets.preprocessing.scannet.meta_data.scannet200_constants import CLASS_LABELS_20, CLASS_LABELS_200, VALID_CLASS_IDS_20, VALID_CLASS_IDS_200, SCANNET_COLOR_MAP_20, SCANNET_COLOR_MAP_200
from tqdm import tqdm


def viz_pyviz(
    submission_dir: str,
    scannet_data_dir: str,
    labelspace: str = "scannet",
):
    ignore_label = 255
    submission_dir: Path = Path(submission_dir)
    scannet_data_dir: Path = Path(scannet_data_dir)
    files = submission_dir.glob("*.txt")

    valid_ids = VALID_CLASS_IDS_20 if labelspace == "scannet" else VALID_CLASS_IDS_200
    label_names = CLASS_LABELS_20 if labelspace == "scannet" else CLASS_LABELS_200
    color_map = SCANNET_COLOR_MAP_20 if labelspace == "scannet" else SCANNET_COLOR_MAP_200

    pyviz_save_dir = submission_dir.parent / "pyviz"
    if pyviz_save_dir.exists():
        shutil.rmtree(str(pyviz_save_dir))
    os.makedirs(str(pyviz_save_dir), exist_ok=True)

    for file in tqdm(files):
        scene_id = file.stem
        pred_labels = np.loadtxt(file, dtype=int).reshape(-1)

        mesh_pth = glob.glob(os.path.join(str(scannet_data_dir), f"**/**/{scene_id}_vh_clean_2.ply"))[0]

        color_mesh = o3d.io.read_triangle_mesh(mesh_pth)

        point_positions = np.asarray(color_mesh.vertices)
        point_positions = point_positions - point_positions.mean(axis=0).reshape(1, 3)
        point_colors = np.asarray(color_mesh.vertex_colors) * 255
        color_mesh.compute_vertex_normals()
        point_normals = np.asarray(color_mesh.vertex_normals)
        point_semantic_colors = np.asarray(np.vectorize(color_map.get)(pred_labels)).transpose()

        point_size = 35.0

        v = viz.Visualizer()
        v.add_points("RGB Color", point_positions, point_colors, point_normals, point_size=point_size, visible=False)
        v.add_points("Semantics", point_positions, point_semantic_colors, point_normals, point_size=point_size)

        save_dir = str(pyviz_save_dir / scene_id)
        v.save(save_dir)
