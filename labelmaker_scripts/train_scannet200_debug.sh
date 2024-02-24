env_name=labelmaker-pointcept
eval "$(conda shell.bash hook)"
conda activate $env_name
conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export CUDA_HOME=$CUDA_PATH

which python

export CUDA_VISIBLE_DEVICES="0"

# INTERPRETER_PATH=/cluster/project/cvg/labelmaker/miniconda3/envs/labelmaker-pointcept/bin/python
INTERPRETER_PATH=/home/guangda/miniconda3/envs/labelmaker-pointcept/bin/python
NUM_GPU=1
DATASET_NAME=scannet200
CONFIG_NAME="semseg-pt-v3m1-0-base-debug"
EXP_NAME=scannet200_from_scratch

sh scripts/train.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -c ${CONFIG_NAME} \
    -n ${EXP_NAME}
