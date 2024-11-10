import os
import sys

sys.path.append("/cluster/project/cvg/labelmaker/LabelMaker-Pointcept")

from tqdm import trange

from pointcept.datasets import (
    ARKitScenesLabelMakerConsensusDataset,
    ConcatDataset,
    S3DISDataset,
    ScanNet200Dataset,
    ScanNetDataset,
    Structured3DDataset,
)

train_dataset = ConcatDataset(
    datasets=[
        dict(
            type="Structured3DDataset",
            split=["train", "val", "test"],
            data_root="/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/structured3d",
            transform=[
                dict(type="CenterShift", apply_z=True),
                dict(type="RandomDropout", dropout_ratio=0.2, dropout_application_ratio=0.2),
                dict(type="RandomRotate", angle=[-1, 1], axis="z", center=[0, 0, 0], p=0.5),
                dict(type="RandomRotate", angle=[-0.015625, 0.015625], axis="x", p=0.5),
                dict(type="RandomRotate", angle=[-0.015625, 0.015625], axis="y", p=0.5),
                dict(type="RandomScale", scale=[0.9, 1.1]),
                dict(type="RandomFlip", p=0.5),
                dict(type="RandomJitter", sigma=0.005, clip=0.02),
                dict(type="ElasticDistortion", distortion_params=[[0.2, 0.4], [0.8, 1.6]]),
                dict(type="ChromaticAutoContrast", p=0.2, blend_factor=None),
                dict(type="ChromaticTranslation", p=0.95, ratio=0.05),
                dict(type="ChromaticJitter", p=0.95, std=0.05),
                dict(type="GridSample", grid_size=0.02, hash_type="fnv", mode="train", return_grid_coord=True),
                dict(type="SphereCrop", sample_rate=0.8, mode="random"),
                dict(type="SphereCrop", point_max=102400, mode="random"),
                dict(type="CenterShift", apply_z=False),
                dict(type="NormalizeColor"),
                dict(type="Add", keys_dict=dict(condition="Structured3D")),
                dict(type="ToTensor"),
                dict(type="Collect", keys=("coord", "grid_coord", "segment", "condition"), feat_keys=("color", "normal")),
            ],
            test_mode=False,
            loop=1,
        ),
        dict(
            type="ScanNet200Dataset",
            split="train",
            data_root="/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/scannet",
            transform=[
                dict(type="CenterShift", apply_z=True),
                dict(type="RandomDropout", dropout_ratio=0.2, dropout_application_ratio=0.2),
                dict(type="RandomRotate", angle=[-1, 1], axis="z", center=[0, 0, 0], p=0.5),
                dict(type="RandomRotate", angle=[-0.015625, 0.015625], axis="x", p=0.5),
                dict(type="RandomRotate", angle=[-0.015625, 0.015625], axis="y", p=0.5),
                dict(type="RandomScale", scale=[0.9, 1.1]),
                dict(type="RandomFlip", p=0.5),
                dict(type="RandomJitter", sigma=0.005, clip=0.02),
                dict(type="ElasticDistortion", distortion_params=[[0.2, 0.4], [0.8, 1.6]]),
                dict(type="ChromaticAutoContrast", p=0.2, blend_factor=None),
                dict(type="ChromaticTranslation", p=0.95, ratio=0.05),
                dict(type="ChromaticJitter", p=0.95, std=0.05),
                dict(type="GridSample", grid_size=0.02, hash_type="fnv", mode="train", return_grid_coord=True),
                dict(type="SphereCrop", point_max=102400, mode="random"),
                dict(type="CenterShift", apply_z=False),
                dict(type="NormalizeColor"),
                dict(type="ShufflePoint"),
                dict(type="Add", keys_dict=dict(condition="ScanNet200")),
                dict(type="ToTensor"),
                dict(type="Collect", keys=("coord", "grid_coord", "segment", "condition"), feat_keys=("color", "normal")),
            ],
            test_mode=False,
            loop=1,
        ),
        dict(
            type="S3DISDataset",
            split=("Area_1", "Area_2", "Area_3", "Area_4", "Area_6"),
            data_root="/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/s3dis",
            transform=[
                dict(type="CenterShift", apply_z=True),
                dict(type="RandomDropout", dropout_ratio=0.2, dropout_application_ratio=0.2),
                dict(type="RandomRotate", angle=[-1, 1], axis="z", center=[0, 0, 0], p=0.5),
                dict(type="RandomRotate", angle=[-0.015625, 0.015625], axis="x", p=0.5),
                dict(type="RandomRotate", angle=[-0.015625, 0.015625], axis="y", p=0.5),
                dict(type="RandomScale", scale=[0.9, 1.1]),
                dict(type="RandomFlip", p=0.5),
                dict(type="RandomJitter", sigma=0.005, clip=0.02),
                dict(type="ChromaticAutoContrast", p=0.2, blend_factor=None),
                dict(type="ChromaticTranslation", p=0.95, ratio=0.05),
                dict(type="ChromaticJitter", p=0.95, std=0.05),
                dict(type="GridSample", grid_size=0.02, hash_type="fnv", mode="train", return_grid_coord=True),
                dict(type="SphereCrop", sample_rate=0.6, mode="random"),
                dict(type="SphereCrop", point_max=204800, mode="random"),
                dict(type="CenterShift", apply_z=False),
                dict(type="NormalizeColor"),
                dict(type="Add", keys_dict=dict(condition="S3DIS")),
                dict(type="ToTensor"),
                dict(type="Collect", keys=("coord", "grid_coord", "segment", "condition"), feat_keys=("color", "normal")),
            ],
            test_mode=False,
            loop=1,
        ),
    ],
    loop=1,
)


for i in trange(len(train_dataset)):
    try:
        data = train_dataset.get_data(i)
    except:
        dataset_idx, data_idx = train_dataset.data_list[i % len(train_dataset.data_list)]

        print(f"{i} {dataset_idx} {data_idx}")
