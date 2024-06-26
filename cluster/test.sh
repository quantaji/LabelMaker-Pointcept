export PATH="/home/blum/miniconda3/condabin/conda:${PATH}"

env_name=labelmaker-pointcept
eval "$(conda shell.bash hook)"
conda activate $env_name
conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export CUDA_HOME=$CUDA_PATH

which python

cd /raid/LabelMaker-Pointcept

INTERPRETER_PATH=/home/blum/miniconda3/envs/labelmaker-pointcept/bin/python

# export CUDA_VISIBLE_DEVICES="0"
export CUDA_VISIBLE_DEVICES="0,1,2,3"

# NUM_GPU=1
NUM_GPU=4
DATASET_NAME=scannetpp
# EXP_NAME=alc_pretrain
EXP_NAME=joint_pretrain_alc_train_val
CHECKPOINT_NAME="model_last"

sh scripts/test.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -n ${EXP_NAME} \
    -w ${CHECKPOINT_NAME}
