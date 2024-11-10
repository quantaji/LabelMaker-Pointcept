env_name=labelmaker-pointcept

export PATH="${HOME}/miniconda3/bin:${PATH}"

eval "$(conda shell.bash hook)"
conda activate $env_name
conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export CUDA_HOME=$CUDA_PATH

which python

cd /home/guangda/repos/LabelMaker-Pointcept

export CUDA_VISIBLE_DEVICES="0"

INTERPRETER_PATH=/home/guangda/miniconda3/envs/labelmaker-pointcept/bin/python
# NUM_GPU=8
NUM_GPU=4

# DATASET_NAME=scannet200
# DATASET_NAME=scannet
DATASET_NAME=scannetpp

# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-debug"
# CONFIG_NAME=insseg-pointgroup-v1m1-ppt-v1m2-pt-v3m1-finetune-debug
# CONFIG_NAME=insseg-pointgroup-v1m1-pt-v3m1-base
# CONFIG_NAME="semseg-pt-v3m1-0-base-wn199"
CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-trial-4"
# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-trial-5"

# EXP_NAME=scannet200_s3dis_structure3d_alc_joint_training_debug
# EXP_NAME=arkitscenes_labelmaker_wn199_pretrain
# EXP_NAME=insseg_ppt_pretrain_scannet200_ft_debug
# EXP_NAME=insseg_ppt_pretrain_scannet_ft_debug
# EXP_NAME=insseg_ptv3_base_debug
EXP_NAME=ppt_no_val_no_scannet_bs_24

CHECKPOINT_NAME="model_last"

export OPENBLAS_NUM_THREADS=1

sh scripts/test.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -n ${EXP_NAME} \
    -w ${CHECKPOINT_NAME}