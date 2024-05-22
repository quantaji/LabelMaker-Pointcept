import glob
import json
import os
import shutil
import sys
from pathlib import Path

import numpy as np

from plyfile import PlyData, PlyElement
from tqdm import tqdm


def load_segments(file_path):
    with open(file_path, "r") as file:
        segments = json.load(file)
    segments = np.array(segments["segIndices"])
    segment_ids = np.unique(segments, return_inverse=True)[1]
    return segment_ids


def segment_labelling(labels, scene, scannet_root):
    segment_file = glob.glob(os.path.join(scannet_root, f"**/**/{scene}_vh_clean_2.0.010000.segs.json"))[0]
    segments = load_segments(segment_file)
    for sg in np.unique(segments):
        vote, count = np.unique(labels[segments == sg], return_counts=True)
        max_count = np.argmax(count)
        max_vote = vote[max_count]
        labels[segments == sg] = max_vote
    return labels


def oversegmentation_refine(
    submission_dir: str,
    scannet_data_dir: str,
):
    submission_dir: Path = Path(submission_dir)
    files = submission_dir.glob("*.txt")

    new_save_dir = submission_dir.parent / (submission_dir.stem + "_oversegmentation_refined")
    if new_save_dir.exists():
        shutil.rmtree(str(new_save_dir))
    os.makedirs(str(new_save_dir), exist_ok=True)

    for file in tqdm(files):
        scene_id = file.stem
        save_pth = new_save_dir / file.name

        labels = np.loadtxt(file, dtype=int)

        refined_labels = segment_labelling(
            labels=labels,
            scene=scene_id,
            scannet_root=scannet_data_dir,
        )

        np.savetxt(
            str(save_pth),
            refined_labels,
            fmt="%d",
        )
