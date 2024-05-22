from pointcept.datasets.preprocessing.scannet.meta_data.scannet200_constants import CLASS_LABELS_200

_base_ = ["../_base_/default_runtime.py"]

# misc custom setting
batch_size = 24  # bs: total bs in all gpus
num_worker = 36
mix_prob = 0.8
empty_cache = False
enable_amp = True
find_unused_parameters = True

# trainer
train = dict(
    type="MultiDatasetTrainer",
)

# model
model = dict(
    type="PPT-v1m1",
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
            "S3DIS",
            "Structured3D",
            "ALC",
            "ScanNet200",
        ),
    ),
    criteria=[dict(type="CrossEntropyLoss", loss_weight=1.0, ignore_index=-1), dict(type="LovaszLoss", mode="multiclass", loss_weight=1.0, ignore_index=-1)],
    backbone_out_channels=64,
    context_channels=256,
    conditions=("Structured3D", "ScanNet", "S3DIS", "ALC", "ScanNet200"),
    template="[x]",
    clip_model="ViT-B/16",
    class_name=(
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
        "bookcase",
        "picture",
        "counter",
        "desk",
        "shelves",
        "curtain",
        "dresser",
        "pillow",
        "mirror",
        "ceiling",
        "refrigerator",
        "television",
        "shower curtain",
        "nightstand",
        "toilet",
        "sink",
        "lamp",
        "bathtub",
        "garbagebin",
        "board",
        "beam",
        "column",
        "clutter",
        "otherstructure",
        "otherfurniture",
        "otherprop",
        "book",
        "ashcan",
        "display",
        "cushion",
        "box",
        "doorframe",
        "swivel chair",
        "towel",
        "backpack",
        "chest of drawers",
        "apparel",
        "armchair",
        "plant",
        "radiator",
        "toilet tissue",
        "shoe",
        "bag",
        "bottle",
        "countertop",
        "coffee table",
        "computer keyboard",
        "fridge",
        "stool",
        "computer",
        "mug",
        "telephone",
        "light",
        "jacket",
        "microwave",
        "footstool",
        "baggage",
        "laptop",
        "printer",
        "shower stall",
        "soap dispenser",
        "stove",
        "fan",
        "paper",
        "stand",
        "bench",
        "wardrobe",
        "blanket",
        "booth",
        "duplicator",
        "bar",
        "soap dish",
        "switch",
        "coffee maker",
        "decoration",
        "range hood",
        "blackboard",
        "clock",
        "railing",
        "mat",
        "seat",
        "bannister",
        "container",
        "mouse",
        "person",
        "stairway",
        "basket",
        "dumbbell",
        "bucket",
        "windowsill",
        "signboard",
        "dishwasher",
        "loudspeaker",
        "washer",
        "paper towel",
        "clothes hamper",
        "piano",
        "sack",
        "handcart",
        "blind",
        "dish rack",
        "mailbox",
        "bicycle",
        "ladder",
        "rack",
        "tray",
        "toaster",
        "paper cutter",
        "plunger",
        "dryer",
        "guitar",
        "fire extinguisher",
        "pitcher",
        "pipe",
        "plate",
        "vacuum",
        "bowl",
        "hat",
        "rod",
        "water cooler",
        "kettle",
        "oven",
        "scale",
        "broom",
        "hand blower",
        "coatrack",
        "teddy",
        "alarm clock",
        "ironing board",
        "fire alarm",
        "machine",
        "music stand",
        "fireplace",
        "furniture",
        "vase",
        "vent",
        "candle",
        "crate",
        "dustpan",
        "earphone",
        "jar",
        "projector",
        "gat",
        "step",
        "step stool",
        "vending machine",
        "coat",
        "coat hanger",
        "drinking fountain",
        "hamper",
        "thermostat",
        "banner",
        "iron",
        "soap",
        "chopping board",
        "kitchen island",
        "shirt",
        "sleeping bag",
        "tire",
        "toothbrush",
        "bathrobe",
        "faucet",
        "slipper",
        "thermos",
        "tripod",
        "dispenser",
        "heater",
        "pool table",
        "remote control",
        "stapler",
        "treadmill",
        "beanbag",
        "dartboard",
        "metronome",
        "rope",
        "sewing machine",
        "shredder",
        "toolbox",
        "water heater",
        "brush",
        "control",
        "dais",
        "dollhouse",
        "envelope",
        "food",
        "frying pan",
        "helmet",
        "tennis racket",
        "umbrella",
        "couch",
        "shelf",
        "office chair",
        "monitor",
        "kitchen cabinet",
        "clothes",
        "tv",
        "end table",
        "dining table",
        "keyboard",
        "toilet paper",
        "tv stand",
        "whiteboard",
        "trash can",
        "closet",
        "stairs",
        "computer tower",
        "bin",
        "ottoman",
        "washing machine",
        "copier",
        "sofa chair",
        "file cabinet",
        "shower",
        "paper towel dispenser",
        "blinds",
        "suitcase",
        "rail",
        "recycling bin",
        "laundry basket",
        "clothes dryer",
        "toilet paper holder",
        "speaker",
        "bathroom stall",
        "shower wall",
        "cup",
        "storage bin",
        "paper towel roll",
        "bulletin board",
        "kitchen counter",
        "toilet paper dispenser",
        "mini fridge",
        "ball",
        "shower curtain rod",
        "shower door",
        "pillar",
        "ledge",
        "toaster oven",
        "toilet seat cover dispenser",
        "cart",
        "storage container",
        "tissue box",
        "light switch",
        "power outlet",
        "sign",
        "closet door",
        "vacuum cleaner",
        "stuffed animal",
        "headphones",
        "guitar case",
        "hair dryer",
        "water bottle",
        "handicap bar",
        "purse",
        "shower floor",
        "water pitcher",
        "paper bag",
        "projector screen",
        "divider",
        "laundry detergent",
        "bathroom counter",
        "object",
        "bathroom vanity",
        "closet wall",
        "laundry hamper",
        "bathroom stall door",
        "ceiling light",
        "trash bin",
        "stair rail",
        "tube",
        "bathroom cabinet",
        "cd case",
        "closet rod",
        "coffee kettle",
        "structure",
        "shower head",
        "keyboard piano",
        "case of water bottles",
        "coat rack",
        "storage organizer",
        "folded chair",
        "power strip",
        "calendar",
        "poster",
        "potted plant",
        "luggage",
        "mattress",
    ),
    valid_index=(
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 20, 22, 24, 25, 27, 34),
        (0, 1, 4, 5, 6, 7, 8, 10, 19, 29, 30, 31, 32),
        (
            0,
            4,
            36,
            2,
            7,
            1,
            37,
            6,
            8,
            9,
            38,
            39,
            40,
            11,
            19,
            41,
            13,
            42,
            43,
            5,
            25,
            44,
            26,
            45,
            46,
            47,
            3,
            15,
            18,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            24,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            27,
            22,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            91,
            92,
            93,
            94,
            95,
            96,
            97,
            31,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            52,
            112,
            113,
            114,
            115,
            116,
            117,
            118,
            119,
            120,
            121,
            122,
            123,
            124,
            125,
            126,
            127,
            128,
            129,
            130,
            131,
            132,
            133,
            134,
            135,
            136,
            137,
            138,
            139,
            140,
            141,
            142,
            143,
            144,
            145,
            146,
            147,
            148,
            149,
            150,
            151,
            152,
            153,
            154,
            155,
            156,
            157,
            158,
            159,
            160,
            161,
            162,
            163,
            164,
            165,
            166,
            167,
            168,
            169,
            170,
            171,
            172,
            173,
            174,
            175,
            176,
            177,
            178,
            179,
            180,
            181,
            182,
            183,
            184,
            185,
            186,
            187,
            188,
            189,
            190,
            191,
            192,
            193,
            194,
            195,
            196,
            197,
            198,
        ),
        (
            0,
            4,
            1,
            6,
            7,
            199,
            2,
            200,
            13,
            201,
            3,
            17,
            25,
            11,
            8,
            24,
            9,
            202,
            15,
            36,
            47,
            55,
            40,
            20,
            26,
            203,
            43,
            204,
            205,
            23,
            12,
            16,
            58,
            39,
            48,
            19,
            27,
            206,
            207,
            208,
            52,
            44,
            209,
            68,
            210,
            211,
            77,
            22,
            212,
            213,
            214,
            64,
            71,
            51,
            215,
            53,
            216,
            217,
            75,
            29,
            218,
            18,
            219,
            96,
            220,
            221,
            72,
            67,
            222,
            73,
            94,
            223,
            131,
            224,
            114,
            124,
            86,
            106,
            225,
            226,
            49,
            227,
            92,
            76,
            70,
            61,
            98,
            87,
            74,
            62,
            228,
            123,
            229,
            120,
            230,
            90,
            231,
            31,
            112,
            113,
            232,
            233,
            234,
            63,
            235,
            83,
            101,
            236,
            140,
            89,
            99,
            80,
            116,
            237,
            138,
            142,
            81,
            238,
            41,
            239,
            240,
            121,
            241,
            127,
            242,
            129,
            117,
            115,
            243,
            244,
            245,
            246,
            93,
            247,
            143,
            248,
            249,
            132,
            250,
            251,
            147,
            252,
            84,
            253,
            151,
            254,
            255,
            146,
            118,
            256,
            257,
            110,
            133,
            258,
            85,
            148,
            259,
            260,
            261,
            262,
            145,
            263,
            264,
            111,
            126,
            265,
            137,
            141,
            266,
            267,
            268,
            269,
            270,
            271,
            272,
            273,
            274,
            275,
            276,
            97,
            277,
            278,
            279,
            280,
            281,
            282,
            283,
            284,
            285,
            286,
            287,
            288,
            289,
            139,
            290,
            291,
            292,
            293,
            294,
            295,
        ),
    ),
    backbone_mode=False,
)

# optimizer
epoch = 1600
eval_epoch = 1600
optimizer = dict(type="AdamW", lr=0.005, weight_decay=0.05)
scheduler = dict(
    type="OneCycleLR",
    max_lr=[0.005, 0.0005],
    pct_start=0.05,
    anneal_strategy="cos",
    div_factor=10.0,
    final_div_factor=1000.0,
)
param_dicts = [dict(keyword="block", lr=0.0005)]

# datasets
data = dict(
    num_classes=200,
    ignore_index=-1,
    names=CLASS_LABELS_200,
    train=dict(
        type="ConcatDataset",
        datasets=[
            dict(
                type="Structured3DDataset",
                split=["train", "val", "test"],
                data_root="data/structured3d",
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
                data_root="data/scannet",
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
                data_root="data/s3dis",
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
            dict(
                type="ARKitScenesLabelMakerConsensusDataset",
                split=["train", "val"],
                data_root="data/alc",
                transform=[
                    dict(type="CenterShift", apply_z=True),
                    dict(type="RandomDropout", dropout_ratio=0.2, dropout_application_ratio=0.2),
                    # dict(type="RandomRotateTargetAngle", angle=(1/2, 1, 3/2), center=[0, 0, 0], axis="z", p=0.75),
                    dict(type="RandomRotate", angle=[-1, 1], axis="z", center=[0, 0, 0], p=0.5),
                    dict(type="RandomRotate", angle=[-1 / 64, 1 / 64], axis="x", p=0.5),
                    dict(type="RandomRotate", angle=[-1 / 64, 1 / 64], axis="y", p=0.5),
                    dict(type="RandomScale", scale=[0.9, 1.1]),
                    # dict(type="RandomShift", shift=[0.2, 0.2, 0.2]),
                    dict(type="RandomFlip", p=0.5),
                    dict(type="RandomJitter", sigma=0.005, clip=0.02),
                    dict(type="ElasticDistortion", distortion_params=[[0.2, 0.4], [0.8, 1.6]]),
                    dict(type="ChromaticAutoContrast", p=0.2, blend_factor=None),
                    dict(type="ChromaticTranslation", p=0.95, ratio=0.05),
                    dict(type="ChromaticJitter", p=0.95, std=0.05),
                    # dict(type="HueSaturationTranslation", hue_max=0.2, saturation_max=0.2),
                    # dict(type="RandomColorDrop", p=0.2, color_augment=0.0),
                    dict(
                        type="GridSample",
                        grid_size=0.02,
                        hash_type="fnv",
                        mode="train",
                        return_grid_coord=True,
                    ),
                    dict(type="SphereCrop", point_max=102400, mode="random"),
                    dict(type="CenterShift", apply_z=False),
                    dict(type="NormalizeColor"),
                    # dict(type="ShufflePoint"),
                    dict(type="Add", keys_dict=dict(condition="ALC")),
                    dict(type="ToTensor"),
                    dict(
                        type="Collect",
                        keys=("coord", "grid_coord", "segment", "condition"),
                        feat_keys=("color", "normal"),
                    ),
                ],
                test_mode=False,
            ),
        ],
        loop=1,
    ),
    val=dict(
        type="ScanNet200Dataset",
        split="val",
        data_root="data/scannet",
        transform=[
            dict(type="CenterShift", apply_z=True),
            dict(type="GridSample", grid_size=0.02, hash_type="fnv", mode="train", return_grid_coord=True),
            dict(type="CenterShift", apply_z=False),
            dict(type="NormalizeColor"),
            dict(type="ToTensor"),
            dict(type="Add", keys_dict=dict(condition="ScanNet200")),
            dict(type="Collect", keys=("coord", "grid_coord", "segment", "condition"), feat_keys=("color", "normal")),
        ],
        test_mode=False,
    ),
    test=dict(
        type="ScanNet200Dataset",
        split="val",
        data_root="data/scannet",
        transform=[dict(type="CenterShift", apply_z=True), dict(type="NormalizeColor")],
        test_mode=True,
        test_cfg=dict(
            voxelize=dict(type="GridSample", grid_size=0.02, hash_type="fnv", mode="test", keys=("coord", "color", "normal"), return_grid_coord=True),
            crop=None,
            post_transform=[
                dict(type="CenterShift", apply_z=False),
                dict(type="Add", keys_dict=dict(condition="ScanNet200")),
                dict(type="ToTensor"),
                dict(type="Collect", keys=("coord", "grid_coord", "index", "condition"), feat_keys=("color", "normal")),
            ],
            aug_transform=[
                [{"type": "RandomRotateTargetAngle", "angle": [0], "axis": "z", "center": [0, 0, 0], "p": 1}],
                [{"type": "RandomRotateTargetAngle", "angle": [0.5], "axis": "z", "center": [0, 0, 0], "p": 1}],
                [{"type": "RandomRotateTargetAngle", "angle": [1], "axis": "z", "center": [0, 0, 0], "p": 1}],
                [{"type": "RandomRotateTargetAngle", "angle": [1.5], "axis": "z", "center": [0, 0, 0], "p": 1}],
                [{"type": "RandomRotateTargetAngle", "angle": [0], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [0.95, 0.95]}],
                [{"type": "RandomRotateTargetAngle", "angle": [0.5], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [0.95, 0.95]}],
                [{"type": "RandomRotateTargetAngle", "angle": [1], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [0.95, 0.95]}],
                [{"type": "RandomRotateTargetAngle", "angle": [1.5], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [0.95, 0.95]}],
                [{"type": "RandomRotateTargetAngle", "angle": [0], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [1.05, 1.05]}],
                [{"type": "RandomRotateTargetAngle", "angle": [0.5], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [1.05, 1.05]}],
                [{"type": "RandomRotateTargetAngle", "angle": [1], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [1.05, 1.05]}],
                [{"type": "RandomRotateTargetAngle", "angle": [1.5], "axis": "z", "center": [0, 0, 0], "p": 1}, {"type": "RandomScale", "scale": [1.05, 1.05]}],
                [{"type": "RandomFlip", "p": 1}],
            ],
        ),
    ),
)
