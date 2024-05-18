env_name=labelmaker-pointcept
eval "$(conda shell.bash hook)"
conda activate $env_name
conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export CUDA_HOME=$CUDA_PATH

which python

cd /home/guangda/repos/LabelMaker-Pointcept

# export CUDA_VISIBLE_DEVICES="0,1,2,3"
export CUDA_VISIBLE_DEVICES="0"

INTERPRETER_PATH=/home/guangda/miniconda3/envs/labelmaker-pointcept/bin/python
NUM_GPU=1
# DATASET_NAME=scannet
DATASET_NAME=scannetpp
CONFIG_NAME="semseg-pt-v3m1-1-finetune-debug"
# CONFIG_NAME="semseg-pt-v3m1-0-base-wn199"
# EXP_NAME=ppt_pretrain_scannet_finetune_train
# EXP_NAME=arkitscenes_labelmaker_wn199_pretrain
# EXP_NAME=ppt_pretrain_scannet_finetune_train_attn_alc_linear
# EXP_NAME=ppt_pretrain_scannet_finetune_train_attn_scannet_linear
# EXP_NAME=ppt_scannet200_pretrain_scannet_finetune_train_attn_alc_linear
EXP_NAME=debug_dataset

sh scripts/train.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -c ${CONFIG_NAME} \
    -n ${EXP_NAME}

