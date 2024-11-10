from pointcept.datasets.preprocessing.scannet.meta_data.scannet200_constants import (
    CLASS_LABELS_200, )

_base_ = ["../_base_/default_runtime.py"]

# misc custom setting
batch_size = 12  # bs: total bs in all gpus
num_worker = 24
mix_prob = 0
empty_cache = False
enable_amp = True
evaluate = True
find_unused_parameters = True
weight = "exp/scannet/semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-no-val/model/model_mod_insseg.pth"

class_names = CLASS_LABELS_200
num_classes = 200
segment_ignore_index = (-1, 0, 2)  # in scannet 20 this is (-1, 0, 1)

model = dict(
    type="PG-v1m1",
    backbone=dict(
        type="PPT-v1m2",
        backbone=dict(
            type="PT-v3m1",
            in_channels=6,
            order=("z", "z-trans", "hilbert", "hilbert-trans"),
            stride=(2, 2, 2, 2),
            enc_depths=(3, 3, 3, 6, 3),
            enc_channels=(48, 96, 192, 384, 512),
            enc_num_head=(3, 6, 12, 24, 32),
            enc_patch_size=(1024, 1024, 1024, 1024, 1024),
            dec_depths=(3, 3, 3, 3),
            dec_channels=(64, 96, 192, 384),
            dec_num_head=(4, 6, 12, 24),
            dec_patch_size=(1024, 1024, 1024, 1024),
            mlp_ratio=4,
            qkv_bias=True,
            qk_scale=None,
            attn_drop=0.0,
            proj_drop=0.0,
            drop_path=0.3,
            shuffle_orders=True,
            pre_norm=True,
            enable_rpe=False,
            enable_flash=True,
            upcast_attention=False,
            upcast_softmax=False,
            cls_mode=False,
            pdnorm_bn=True,
            pdnorm_ln=True,
            pdnorm_decouple=True,
            pdnorm_adaptive=False,
            pdnorm_affine=True,
            pdnorm_conditions=(
                "ScanNet",
                "ScanNet200",
                "ScanNet++",
                "Structured3D",
                "ALC",
            ),
        ),
        criteria=[
            dict(type="CrossEntropyLoss", loss_weight=1.0, ignore_index=-1),
            dict(type="LovaszLoss",
                 mode="multiclass",
                 loss_weight=1.0,
                 ignore_index=-1)
        ],
        backbone_out_channels=64,
        backbone_mode=True,
        context_channels=256,
        conditions=(
            "ScanNet",
            "ScanNet200",
            "ScanNet++",
            "Structured3D",
            "ALC",
        ),
        num_classes=(20, 200, 100, 25, 185),
    ),
    backbone_out_channels=64,
    semantic_num_classes=num_classes,
    semantic_ignore_index=-1,
    segment_ignore_index=segment_ignore_index,
    instance_ignore_index=-1,
    cluster_thresh=1.5,
    cluster_closed_points=300,
    cluster_propose_points=100,
    cluster_min_points=50,
    freeze_backbone=True,
    # freeze_backbone=False,
)

# scheduler settings
epoch = 800
optimizer = dict(
    type="SGD",
    lr=0.1,
    momentum=0.9,
    weight_decay=0.0001,
    nesterov=True,
)
scheduler = dict(type="PolyLR")

# dataset settings
dataset_type = "ScanNet200DatasetV2"
data_root = "data/scannet"

data = dict(
    num_classes=num_classes,
    ignore_index=-1,
    names=class_names,
    train=dict(
        type=dataset_type,
        split="train",
        data_root=data_root,
        transform=[
            dict(type="CenterShift", apply_z=True),
            dict(type="RandomDropout",
                 dropout_ratio=0.2,
                 dropout_application_ratio=0.5),
            # dict(type="RandomRotateTargetAngle", angle=(1/2, 1, 3/2), center=[0, 0, 0], axis='z', p=0.75),
            dict(type="RandomRotate",
                 angle=[-1, 1],
                 axis="z",
                 center=[0, 0, 0],
                 p=0.5),
            dict(type="RandomRotate", angle=[-1 / 64, 1 / 64], axis="x",
                 p=0.5),
            dict(type="RandomRotate", angle=[-1 / 64, 1 / 64], axis="y",
                 p=0.5),
            dict(type="RandomScale", scale=[0.9, 1.1]),
            # dict(type="RandomShift", shift=[0.2, 0.2, 0.2]),
            dict(type="RandomFlip", p=0.5),
            dict(type="RandomJitter", sigma=0.005, clip=0.02),
            dict(type="ElasticDistortion",
                 distortion_params=[[0.2, 0.4], [0.8, 1.6]]),
            dict(type="ChromaticAutoContrast", p=0.2, blend_factor=None),
            dict(type="ChromaticTranslation", p=0.95, ratio=0.1),
            dict(type="ChromaticJitter", p=0.95, std=0.05),
            # dict(type="HueSaturationTranslation", hue_max=0.2, saturation_max=0.2),
            # dict(type="RandomColorDrop", p=0.2, color_augment=0.0),
            dict(
                type="GridSample",
                grid_size=0.02,
                hash_type="fnv",
                mode="train",
                return_grid_coord=True,
                keys=("coord", "color", "normal", "segment", "instance"),
            ),
            dict(type="SphereCrop", sample_rate=0.8, mode="random"),
            dict(type="NormalizeColor"),
            dict(
                type="InstanceParser",
                segment_ignore_index=segment_ignore_index,
                instance_ignore_index=-1,
            ),
            dict(type="Add", keys_dict={"condition": "ScanNet200"}),
            dict(type="ToTensor"),
            dict(
                type="Collect",
                keys=(
                    "coord",
                    "grid_coord",
                    "segment",
                    "instance",
                    "instance_centroid",
                    "bbox",
                    "condition",
                ),
                feat_keys=("color", "normal"),
            ),
        ],
        test_mode=False,
    ),
    val=dict(
        type=dataset_type,
        split="val",
        data_root=data_root,
        transform=[
            dict(type="CenterShift", apply_z=True),
            dict(
                type="Copy",
                keys_dict={
                    "coord": "origin_coord",
                    "segment": "origin_segment",
                    "instance": "origin_instance",
                },
            ),
            dict(
                type="GridSample",
                grid_size=0.02,
                hash_type="fnv",
                mode="train",
                return_grid_coord=True,
                keys=("coord", "color", "normal", "segment", "instance"),
            ),
            # dict(type="SphereCrop", point_max=1000000, mode='center'),
            dict(type="CenterShift", apply_z=False),
            dict(type="NormalizeColor"),
            dict(
                type="InstanceParser",
                segment_ignore_index=segment_ignore_index,
                instance_ignore_index=-1,
            ),
            dict(type="Add", keys_dict={"condition": "ScanNet200"}),
            dict(type="ToTensor"),
            dict(
                type="Collect",
                keys=(
                    "coord",
                    "grid_coord",
                    "segment",
                    "instance",
                    "origin_coord",
                    "origin_segment",
                    "origin_instance",
                    "instance_centroid",
                    "bbox",
                    "condition",
                ),
                feat_keys=("color", "normal"),
                offset_keys_dict=dict(offset="coord",
                                      origin_offset="origin_coord"),
            ),
        ],
        test_mode=False,
    ),
    test=dict(),  # currently not available
)

hooks = [
    dict(type="CheckpointLoader", keywords="module.", replacement="module."),
    dict(type="IterationTimer", warmup_iter=2),
    dict(type="InformationWriter"),
    dict(
        type="InsSegEvaluator",
        segment_ignore_index=segment_ignore_index,
        instance_ignore_index=-1,
    ),
    dict(type="CheckpointSaver", save_freq=None),
]
