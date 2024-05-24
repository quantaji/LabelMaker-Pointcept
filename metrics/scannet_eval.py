import glob
import json
import os
from pathlib import Path

import numpy as np
from tqdm import tqdm

from metrics import ConfusionMatrix, IoU
from pointcept.datasets.preprocessing.scannet.meta_data.scannet200_constants import (
    CLASS_LABELS_20,
    CLASS_LABELS_200,
    VALID_CLASS_IDS_20,
    VALID_CLASS_IDS_200,
)
from pointcept.datasets.preprocessing.scannet.meta_data.scannet200_splits import (
    COMMON_CATS_SCANNET_200,
    HEAD_CATS_SCANNET_200,
    TAIL_CATS_SCANNET_200,
    VALID_CLASS_IDS_200_VALIDATION,
)


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

    # print(list(files))
    # assert False

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

    results = {
        "mIoU": np.nan_to_num(results_iou).mean(),
        "label_mIoU": {},
        "split_mIoU": {},
    }
    for i, k in enumerate(label_names):
        results["label_mIoU"][k] = results_iou[i]

    if labelspace == "scannet200":
        common_scores = []
        for label in COMMON_CATS_SCANNET_200:
            if label in results["label_mIoU"].keys():
                common_scores.append(results["label_mIoU"][label])
        common_scores = np.array(common_scores)

        head_scores = []
        for label in HEAD_CATS_SCANNET_200:
            if label in results["label_mIoU"].keys():
                head_scores.append(results["label_mIoU"][label])
        head_scores = np.array(head_scores)

        tail_scores = []
        for label in TAIL_CATS_SCANNET_200:
            if label in results["label_mIoU"].keys():
                tail_scores.append(results["label_mIoU"][label])
        tail_scores = np.array(tail_scores)

        # print(common_scores, head_scores, tail_scores)

        results["split_mIoU"] = {
            "head_mIoU": np.nan_to_num(head_scores).mean(),
            "common_mIoU": np.nan_to_num(common_scores).mean(),
            "tail_mIoU": np.nan_to_num(tail_scores).mean(),
        }

    print(json.dumps(results, indent=4))
    # print(results["label_mIoU"]["candle"])

    with open(str(submission_dir.parent / "eval_results.json"), "w") as f:
        json.dump(results, f, indent=4)
