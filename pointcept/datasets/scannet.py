"""
ScanNet20 / ScanNet200 / ScanNet Data Efficient Dataset

Author: Xiaoyang Wu (xiaoyang.wu.cs@gmail.com)
Please cite our work if the code is helpful to you.
"""

import glob
import os
from collections.abc import Sequence
from copy import deepcopy

import numpy as np
import torch
from torch.utils.data import Dataset

from pointcept.utils.cache import shared_dict
from pointcept.utils.logger import get_root_logger

from .builder import DATASETS
from .defaults import DefaultDatasetV2
from .preprocessing.scannet.meta_data.scannet200_constants import VALID_CLASS_IDS_20, VALID_CLASS_IDS_200
from .transform import TRANSFORMS, Compose


@DATASETS.register_module()
class ScanNetDataset(Dataset):
    class2id = np.array(VALID_CLASS_IDS_20)

    def __init__(
        self,
        split="train",
        data_root="data/scannet",
        transform=None,
        lr_file=None,
        la_file=None,
        ignore_index=-1,
        test_mode=False,
        test_cfg=None,
        cache=False,
        loop=1,
    ):
        super(ScanNetDataset, self).__init__()
        self.data_root = data_root
        self.split = split
        self.transform = Compose(transform)
        self.cache = cache
        self.loop = loop if not test_mode else 1  # force make loop = 1 while in test mode
        self.test_mode = test_mode
        self.test_cfg = test_cfg if test_mode else None

        if test_mode:
            self.test_voxelize = TRANSFORMS.build(self.test_cfg.voxelize)
            self.test_crop = TRANSFORMS.build(
                self.test_cfg.crop) if self.test_cfg.crop else None
            self.post_transform = Compose(self.test_cfg.post_transform)
            self.aug_transform = [
                Compose(aug) for aug in self.test_cfg.aug_transform
            ]

        if lr_file:
            self.data_list = [
                os.path.join(data_root, "train", name + ".pth")
                for name in np.loadtxt(lr_file, dtype=str)
            ]
        else:
            self.data_list = self.get_data_list()
        self.la = torch.load(la_file) if la_file else None
        self.ignore_index = ignore_index
        logger = get_root_logger()
        logger.info("Totally {} x {} samples in {} set.".format(
            len(self.data_list), self.loop, split))

    def get_data_list(self):
        if isinstance(self.split, str):
            data_list = glob.glob(
                os.path.join(self.data_root, self.split, "*.pth"))
        elif isinstance(self.split, Sequence):
            data_list = []
            for split in self.split:
                data_list += glob.glob(
                    os.path.join(self.data_root, split, "*.pth"))
        else:
            raise NotImplementedError
        return data_list

    def get_data(self, idx):
        data_path = self.data_list[idx % len(self.data_list)]
        if not self.cache:
            data = torch.load(data_path)
        else:
            data_name = data_path.replace(os.path.dirname(self.data_root),
                                          "").split(".")[0]
            cache_name = "pointcept" + data_name.replace(os.path.sep, "-")
            data = shared_dict(cache_name)
        coord = data["coord"]
        color = data["color"]
        normal = data["normal"]
        scene_id = data["scene_id"]
        if "semantic_gt20" in data.keys():
            segment = data["semantic_gt20"].reshape([-1])
        else:
            segment = np.ones(coord.shape[0]) * -1
        if "instance_gt" in data.keys():
            instance = data["instance_gt"].reshape([-1])
        else:
            instance = np.ones(coord.shape[0]) * -1
        data_dict = dict(
            coord=coord,
            normal=normal,
            color=color,
            segment=segment,
            instance=instance,
            scene_id=scene_id,
        )
        if self.la:
            sampled_index = self.la[self.get_data_name(idx)]
            mask = np.ones_like(segment).astype(np.bool)
            mask[sampled_index] = False
            segment[mask] = self.ignore_index
            data_dict["segment"] = segment
            data_dict["sampled_index"] = sampled_index
        return data_dict

    def get_data_name(self, idx):
        return os.path.basename(
            self.data_list[idx % len(self.data_list)]).split(".")[0]

    def prepare_train_data(self, idx):
        # load data
        data_dict = self.get_data(idx)
        data_dict = self.transform(data_dict)
        return data_dict

    def prepare_test_data(self, idx):
        # load data
        data_dict = self.get_data(idx)
        segment = data_dict.pop("segment")
        data_dict = self.transform(data_dict)
        data_dict_list = []
        for aug in self.aug_transform:
            data_dict_list.append(aug(deepcopy(data_dict)))

        input_dict_list = []
        for data in data_dict_list:
            data_part_list = self.test_voxelize(data)
            for data_part in data_part_list:
                if self.test_crop:
                    data_part = self.test_crop(data_part)
                else:
                    data_part = [data_part]
                input_dict_list += data_part

        for i in range(len(input_dict_list)):
            input_dict_list[i] = self.post_transform(input_dict_list[i])
        data_dict = dict(fragment_list=input_dict_list,
                         segment=segment,
                         name=self.get_data_name(idx))
        return data_dict

    def __getitem__(self, idx):
        if self.test_mode:
            return self.prepare_test_data(idx)
        else:
            return self.prepare_train_data(idx)

    def __len__(self):
        return len(self.data_list) * self.loop


@DATASETS.register_module()
class ScanNet200Dataset(ScanNetDataset):
    class2id = np.array(VALID_CLASS_IDS_200)

    def get_data(self, idx):
        data = torch.load(self.data_list[idx % len(self.data_list)])
        coord = data["coord"]
        color = data["color"]
        normal = data["normal"]
        scene_id = data["scene_id"]
        if "semantic_gt200" in data.keys():
            segment = data["semantic_gt200"].reshape([-1])
        else:
            segment = np.ones(coord.shape[0]) * -1
        if "instance_gt" in data.keys():
            instance = data["instance_gt"].reshape([-1])
        else:
            instance = np.ones(coord.shape[0]) * -1
        data_dict = dict(
            coord=coord,
            normal=normal,
            color=color,
            segment=segment,
            instance=instance,
            scene_id=scene_id,
        )
        if self.la:
            sampled_index = self.la[self.get_data_name(idx)]
            segment[sampled_index] = self.ignore_index
            data_dict["segment"] = segment
            data_dict["sampled_index"] = sampled_index
        return data_dict


@DATASETS.register_module()
class ScanNetDatasetV2(DefaultDatasetV2):
    VALID_ASSETS = [
        "coord",
        "color",
        "normal",
        "segment20",
        "instance",
    ]
    class2id = np.array(VALID_CLASS_IDS_20)

    def __init__(
        self,
        lr_file=None,
        la_file=None,
        **kwargs,
    ):
        self.lr = np.loadtxt(lr_file,
                             dtype=str) if lr_file is not None else None
        self.la = torch.load(la_file) if la_file is not None else None
        super().__init__(**kwargs)

    def get_data_list(self):
        if self.lr is None:
            data_list = super().get_data_list()
        else:
            data_list = [
                os.path.join(self.data_root, "train", name) for name in self.lr
            ]
        return data_list

    def get_data(self, idx):
        data_path = self.data_list[idx % len(self.data_list)]
        name = self.get_data_name(idx)
        if self.cache:
            cache_name = f"pointcept-{name}"
            return shared_dict(cache_name)

        data_dict = {}
        assets = os.listdir(data_path)
        for asset in assets:
            if not asset.endswith(".npy"):
                continue
            if asset[:-4] not in self.VALID_ASSETS:
                continue
            data_dict[asset[:-4]] = np.load(os.path.join(data_path, asset))
        data_dict["name"] = name
        data_dict["coord"] = data_dict["coord"].astype(np.float32)
        data_dict["color"] = data_dict["color"].astype(np.float32)
        data_dict["normal"] = data_dict["normal"].astype(np.float32)

        if "segment20" in data_dict.keys():
            data_dict["segment"] = (data_dict.pop("segment20").reshape(
                [-1]).astype(np.int32))
        elif "segment200" in data_dict.keys():
            data_dict["segment"] = (data_dict.pop("segment200").reshape(
                [-1]).astype(np.int32))
        else:
            data_dict["segment"] = (
                np.ones(data_dict["coord"].shape[0], dtype=np.int32) * -1)

        if "instance" in data_dict.keys():
            data_dict["instance"] = (data_dict.pop("instance").reshape(
                [-1]).astype(np.int32))
        else:
            data_dict["instance"] = (
                np.ones(data_dict["coord"].shape[0], dtype=np.int32) * -1)
        if self.la:
            sampled_index = self.la[self.get_data_name(idx)]
            mask = np.ones_like(data_dict["segment"], dtype=bool)
            mask[sampled_index] = False
            data_dict["segment"][mask] = self.ignore_index
            data_dict["sampled_index"] = sampled_index
        return data_dict


@DATASETS.register_module()
class ScanNet200DatasetV2(ScanNetDatasetV2):
    VALID_ASSETS = [
        "coord",
        "color",
        "normal",
        "segment200",
        "instance",
    ]
    class2id = np.array(VALID_CLASS_IDS_200)
