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

# export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"
export CUDA_VISIBLE_DEVICES="0"

INTERPRETER_PATH=/home/guangda/miniconda3/envs/labelmaker-pointcept/bin/python
NUM_GPU=1
DATASET_NAME=scannet200
# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc"
# CONFIG_NAME="semseg-pt-v3m1-0-base-wn199"
# EXP_NAME=scannet200_s3dis_structure3d_alc_joint_training
# EXP_NAME=arkitscenes_labelmaker_wn199_pretrain
# CONFIG_NAME="semseg-pt-v3m1-0-base-ft"
# EXP_NAME=alc_pretrain_scannet200_ft_train_val
EXP_NAME="alc_pretrain_scannet200_ft_train_newtest_lower_lr_epoch1600_train_val"
CHECKPOINT_NAME="model_last"

export OPENBLAS_NUM_THREADS=1

sh scripts/test.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -w ${CHECKPOINT_NAME} \
    -n ${EXP_NAME} 
