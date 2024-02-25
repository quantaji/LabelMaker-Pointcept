weight = 'exp/scannet/semseg-pt-v3m1-1-ppt-extreme/model/model_best.pth'
resume = False
evaluate = True
test_only = False
seed = 44350923
save_path = 'exp/scannet/semseg-pt-v3m1-1-ppt-extreme'
num_worker = 48
batch_size = 24
batch_size_val = None
batch_size_test = None
epoch = 100
eval_epoch = 100
sync_bn = False
enable_amp = True
empty_cache = False
find_unused_parameters = True
mix_prob = 0.8
param_dicts = [dict(keyword='block', lr=0.0005)]
hooks = [
    dict(type='CheckpointLoader'),
    dict(type='IterationTimer', warmup_iter=2),
    dict(type='InformationWriter'),
    dict(type='SemSegEvaluator'),
    dict(type='CheckpointSaver', save_freq=None),
    dict(type='PreciseEvaluator', test_last=False)
]
train = dict(type='MultiDatasetTrainer')
test = dict(type='SemSegTester', verbose=True)
model = dict(
    type='PPT-v1m1',
    backbone=dict(
        type='PT-v3m1',
        in_channels=6,
        order=('z', 'z-trans', 'hilbert', 'hilbert-trans'),
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
        pdnorm_conditions=('ScanNet', 'S3DIS', 'Structured3D')),
    criteria=[
        dict(type='CrossEntropyLoss', loss_weight=1.0, ignore_index=-1),
        dict(
            type='LovaszLoss',
            mode='multiclass',
            loss_weight=1.0,
            ignore_index=-1)
    ],
    backbone_out_channels=64,
    context_channels=256,
    conditions=('Structured3D', 'ScanNet', 'S3DIS'),
    template='[x]',
    clip_model='ViT-B/16',
    class_name=('wall', 'floor', 'cabinet', 'bed', 'chair', 'sofa', 'table',
                'door', 'window', 'bookshelf', 'bookcase', 'picture',
                'counter', 'desk', 'shelves', 'curtain', 'dresser', 'pillow',
                'mirror', 'ceiling', 'refrigerator', 'television',
                'shower curtain', 'nightstand', 'toilet', 'sink', 'lamp',
                'bathtub', 'garbagebin', 'board', 'beam', 'column', 'clutter',
                'otherstructure', 'otherfurniture', 'otherprop'),
    valid_index=((0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 13, 14, 15, 16, 17, 18, 19,
                  20, 21, 23, 25, 26, 33, 34, 35),
                 (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 20, 22, 24, 25,
                  27, 34), (0, 1, 4, 5, 6, 7, 8, 10, 19, 29, 30, 31, 32)),
    backbone_mode=False)
optimizer = dict(type='AdamW', lr=0.005, weight_decay=0.05)
scheduler = dict(
    type='OneCycleLR',
    max_lr=[0.005, 0.0005],
    pct_start=0.05,
    anneal_strategy='cos',
    div_factor=10.0,
    final_div_factor=1000.0)
data = dict(
    num_classes=20,
    ignore_index=-1,
    names=[
        'wall', 'floor', 'cabinet', 'bed', 'chair', 'sofa', 'table', 'door',
        'window', 'bookshelf', 'picture', 'counter', 'desk', 'curtain',
        'refridgerator', 'shower curtain', 'toilet', 'sink', 'bathtub',
        'otherfurniture'
    ],
    train=dict(
        type='ConcatDataset',
        datasets=[
            dict(
                type='Structured3DDataset',
                split=['train', 'val', 'test'],
                data_root='data/structured3d',
                transform=[
                    dict(type='CenterShift', apply_z=True),
                    dict(
                        type='RandomDropout',
                        dropout_ratio=0.2,
                        dropout_application_ratio=0.2),
                    dict(
                        type='RandomRotate',
                        angle=[-1, 1],
                        axis='z',
                        center=[0, 0, 0],
                        p=0.5),
                    dict(
                        type='RandomRotate',
                        angle=[-0.015625, 0.015625],
                        axis='x',
                        p=0.5),
                    dict(
                        type='RandomRotate',
                        angle=[-0.015625, 0.015625],
                        axis='y',
                        p=0.5),
                    dict(type='RandomScale', scale=[0.9, 1.1]),
                    dict(type='RandomFlip', p=0.5),
                    dict(type='RandomJitter', sigma=0.005, clip=0.02),
                    dict(
                        type='ElasticDistortion',
                        distortion_params=[[0.2, 0.4], [0.8, 1.6]]),
                    dict(
                        type='ChromaticAutoContrast', p=0.2,
                        blend_factor=None),
                    dict(type='ChromaticTranslation', p=0.95, ratio=0.05),
                    dict(type='ChromaticJitter', p=0.95, std=0.05),
                    dict(
                        type='GridSample',
                        grid_size=0.02,
                        hash_type='fnv',
                        mode='train',
                        return_grid_coord=True),
                    dict(type='SphereCrop', sample_rate=0.8, mode='random'),
                    dict(type='SphereCrop', point_max=102400, mode='random'),
                    dict(type='CenterShift', apply_z=False),
                    dict(type='NormalizeColor'),
                    dict(type='Add', keys_dict=dict(condition='Structured3D')),
                    dict(type='ToTensor'),
                    dict(
                        type='Collect',
                        keys=('coord', 'grid_coord', 'segment', 'condition'),
                        feat_keys=('color', 'normal'))
                ],
                test_mode=False,
                loop=2),
            dict(
                type='ScanNetDataset',
                split='train',
                data_root='data/scannet',
                transform=[
                    dict(type='CenterShift', apply_z=True),
                    dict(
                        type='RandomDropout',
                        dropout_ratio=0.2,
                        dropout_application_ratio=0.2),
                    dict(
                        type='RandomRotate',
                        angle=[-1, 1],
                        axis='z',
                        center=[0, 0, 0],
                        p=0.5),
                    dict(
                        type='RandomRotate',
                        angle=[-0.015625, 0.015625],
                        axis='x',
                        p=0.5),
                    dict(
                        type='RandomRotate',
                        angle=[-0.015625, 0.015625],
                        axis='y',
                        p=0.5),
                    dict(type='RandomScale', scale=[0.9, 1.1]),
                    dict(type='RandomFlip', p=0.5),
                    dict(type='RandomJitter', sigma=0.005, clip=0.02),
                    dict(
                        type='ElasticDistortion',
                        distortion_params=[[0.2, 0.4], [0.8, 1.6]]),
                    dict(
                        type='ChromaticAutoContrast', p=0.2,
                        blend_factor=None),
                    dict(type='ChromaticTranslation', p=0.95, ratio=0.05),
                    dict(type='ChromaticJitter', p=0.95, std=0.05),
                    dict(
                        type='GridSample',
                        grid_size=0.02,
                        hash_type='fnv',
                        mode='train',
                        return_grid_coord=True),
                    dict(type='SphereCrop', point_max=102400, mode='random'),
                    dict(type='CenterShift', apply_z=False),
                    dict(type='NormalizeColor'),
                    dict(type='ShufflePoint'),
                    dict(type='Add', keys_dict=dict(condition='ScanNet')),
                    dict(type='ToTensor'),
                    dict(
                        type='Collect',
                        keys=('coord', 'grid_coord', 'segment', 'condition'),
                        feat_keys=('color', 'normal'))
                ],
                test_mode=False,
                loop=1)
        ],
        loop=1),
    val=dict(
        type='ScanNetDataset',
        split='val',
        data_root='data/scannet',
        transform=[
            dict(type='CenterShift', apply_z=True),
            dict(
                type='GridSample',
                grid_size=0.02,
                hash_type='fnv',
                mode='train',
                return_grid_coord=True),
            dict(type='CenterShift', apply_z=False),
            dict(type='NormalizeColor'),
            dict(type='ToTensor'),
            dict(type='Add', keys_dict=dict(condition='ScanNet')),
            dict(
                type='Collect',
                keys=('coord', 'grid_coord', 'segment', 'condition'),
                feat_keys=('color', 'normal'))
        ],
        test_mode=False),
    test=dict(
        type='ScanNetDataset',
        split='val',
        data_root='data/scannet',
        transform=[
            dict(type='CenterShift', apply_z=True),
            dict(type='NormalizeColor')
        ],
        test_mode=True,
        test_cfg=dict(
            voxelize=dict(
                type='GridSample',
                grid_size=0.02,
                hash_type='fnv',
                mode='test',
                keys=('coord', 'color', 'normal'),
                return_grid_coord=True),
            crop=None,
            post_transform=[
                dict(type='CenterShift', apply_z=False),
                dict(type='Add', keys_dict=dict(condition='ScanNet')),
                dict(type='ToTensor'),
                dict(
                    type='Collect',
                    keys=('coord', 'grid_coord', 'index', 'condition'),
                    feat_keys=('color', 'normal'))
            ],
            aug_transform=[[{
                'type': 'RandomRotateTargetAngle',
                'angle': [0],
                'axis': 'z',
                'center': [0, 0, 0],
                'p': 1
            }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [0.5],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [1],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [1.5],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [0],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [0.95, 0.95]
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [0.5],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [0.95, 0.95]
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [1],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [0.95, 0.95]
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [1.5],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [0.95, 0.95]
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [0],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [1.05, 1.05]
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [0.5],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [1.05, 1.05]
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [1],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [1.05, 1.05]
                           }],
                           [{
                               'type': 'RandomRotateTargetAngle',
                               'angle': [1.5],
                               'axis': 'z',
                               'center': [0, 0, 0],
                               'p': 1
                           }, {
                               'type': 'RandomScale',
                               'scale': [1.05, 1.05]
                           }], [{
                               'type': 'RandomFlip',
                               'p': 1
                           }]])))
