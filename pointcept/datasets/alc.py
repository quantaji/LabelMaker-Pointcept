import glob
import os
from collections.abc import Sequence
from copy import deepcopy

import numpy as np
import torch
from labelmaker.label_data import get_wordnet
from torch.utils.data import Dataset

from pointcept.utils.cache import shared_dict
from pointcept.utils.logger import get_root_logger

from .builder import DATASETS
from .preprocessing.alc.preprocess_arkitscenes_labelmaker_consensus import get_wordnet_compact_mapping
from .preprocessing.scannet.meta_data.scannet200_constants import VALID_CLASS_IDS_20, VALID_CLASS_IDS_200
from .transform import TRANSFORMS, Compose


@DATASETS.register_module()
class ARKitScenesLabelMakerConsensusDataset(Dataset):

    label_key = "semantic_pseudo_gt_wn199"

    def __init__(
        self,
        split="train",
        data_root="data/alc",
        transform=None,
        ignore_index=-1,
        test_mode=False,
        test_cfg=None,
        cache=False,
        loop=1,
    ):
        super(ARKitScenesLabelMakerConsensusDataset, self).__init__()
        self.get_class_to_id()

        self.data_root = data_root
        self.split = split
        self.transform = Compose(transform)
        self.cache = cache
        self.loop = loop if not test_mode else 1  # force make loop = 1 while in test mode
        self.test_mode = test_mode
        self.test_cfg = test_cfg if test_mode else None

        if test_mode:
            self.test_voxelize = TRANSFORMS.build(self.test_cfg.voxelize)
            self.test_crop = TRANSFORMS.build(self.test_cfg.crop) if self.test_cfg.crop else None
            self.post_transform = Compose(self.test_cfg.post_transform)
            self.aug_transform = [Compose(aug) for aug in self.test_cfg.aug_transform]

        self.data_list = self.get_data_list()

        self.ignore_index = ignore_index

        logger = get_root_logger()
        logger.info(
            "Totally {} x {} samples in {} set.".format(
                len(self.data_list),
                self.loop,
                split,
            )
        )

    def get_class_to_id(self):
        self.class2id = get_wordnet_compact_mapping()[0]

    def get_data_list(self):
        if isinstance(self.split, str):
            data_list = glob.glob(os.path.join(self.data_root, self.split, "*.pth"))
        elif isinstance(self.split, Sequence):
            data_list = []
            for split in self.split:
                data_list += glob.glob(os.path.join(self.data_root, split, "*.pth"))
        else:
            raise NotImplementedError
        return data_list

    def get_data(self, idx):
        data_path = self.data_list[idx % len(self.data_list)]

        if not self.cache:
            data = torch.load(data_path)
        else:
            data_name = data_path.replace(os.path.dirname(self.data_root), "").split(".")[0]
            cache_name = "pointcept" + data_name.replace(os.path.sep, "-")
            data = shared_dict(cache_name)

        coord = data["coord"]
        color = data["color"]
        normal = data["normal"]
        scene_id = data["scene_id"]
        if self.label_key in data.keys():
            segment = data[self.label_key].reshape(-1)
        else:
            segment = np.ones(coord.shape[0]) * -1
        instance = np.ones(coord.shape[0]) * -1

        data_dict = dict(
            coord=coord,
            color=color,
            segment=segment,
            instance=instance,
            scene_id=scene_id,
        )

        if normal is not None:
            data_dict["normal"] = normal

        return data_dict

    def get_data_name(self, idx):
        return os.path.basename(self.data_list[idx % len(self.data_list)]).split(".")[0]

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
        data_dict = dict(fragment_list=input_dict_list, segment=segment, name=self.get_data_name(idx))
        return data_dict

    def __getitem__(self, idx):
        if self.test_mode:
            return self.prepare_test_data(idx)
        else:
            return self.prepare_train_data(idx)

    def __len__(self):
        return len(self.data_list) * self.loop


@DATASETS.register_module()
class ARKitScenesLabelMakerScanNet200Dataset(ARKitScenesLabelMakerConsensusDataset):
    label_key = "semantic_pseudo_gt_scannet200"

    def get_class_to_id(self):
        self.class2id = np.array(VALID_CLASS_IDS_200)
