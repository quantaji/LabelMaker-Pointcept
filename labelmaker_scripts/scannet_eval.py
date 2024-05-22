import glob
import json
import os
from pathlib import Path

import numpy as np

from pointcept.datasets.preprocessing.scannet.meta_data.scannet200_constants import (
    CLASS_LABELS_20,
    CLASS_LABELS_200,
    VALID_CLASS_IDS_20,
    VALID_CLASS_IDS_200,
)
from metrics import ConfusionMatrix, IoU
from tqdm import tqdm


def eval_mIoU(
    submission_dir: str,
    scannet_processed_data_dir: str = "/home/guangda/repos/labelmaker-mix3d/data/processed/scannet",
    labelspace: str = "scannet",
):
    ignore_label = 255
    submission_dir: Path = Path(submission_dir)
    scannet_processed_data_dir: Path = Path(scannet_processed_data_dir)
    files = submission_dir.glob("*.txt")

    assert labelspace in ["scannet", "scannet200"]

    num_labels = 20 if labelspace == "scannet" else 200
    valid_ids = VALID_CLASS_IDS_20 if labelspace == "scannet" else VALID_CLASS_IDS_200
    label_names = CLASS_LABELS_20 if labelspace == "scannet" else CLASS_LABELS_200

    def remap_label(label):
        new_label = np.ones_like(label) * ignore_label
        for i, idx in enumerate(valid_ids):
            new_label[label == idx] = i

        return new_label

    confusion = ConfusionMatrix(
        num_classes=num_labels,
        ignore_label=ignore_label,
    )
    confusion.reset()
    iou = IoU()

    preds, gts = [], []

    for file in tqdm(files):
        scene_id = file.stem
        pred_labels = np.loadtxt(file, dtype=int).reshape(-1)

        gt_pth = glob.glob(os.path.join(str(scannet_processed_data_dir), f"**/{scene_id.replace('scene', '')}.npy"))[0]
        gt_labels = np.load(gt_pth)[:, 9].reshape(-1)

        preds.append(remap_label(pred_labels))
        gts.append(remap_label(gt_labels))

    preds = np.hstack(preds)
    gts = np.hstack(gts)

    print(preds.shape, gts.shape)

    confusion.add(predicted=preds, target=gts)
    confusion_matrix = confusion.value()
    results_iou = iou.value(confusion_matrix)

    results = {"mIoU": np.nan_to_num(results_iou).mean()}
    for i, k in enumerate(label_names):
        results[k] = results_iou[i]

    print(json.dumps(results, indent=4))

    with open(str(submission_dir.parent / "eval_results.json"), "w") as f:
        json.dump(results, f, indent=4)
