#!/usr/bin/bash
#SBATCH --job-name="pointcept-train"
#SBATCH --output=ptv3_train_%j.out
#SBATCH --time=120:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=20G
#SBATCH -A ls_polle
#SBATCH --gpus=a100_80gb:4

module purge
# module load gcc/11.4.0 cuda/12.1.1 eth_proxy
module load stack/2024-06 gcc/12.2.0 cuda/12.1.1 eth_proxy

#SBATCH --gpus=rtx_3090:8 for other configuration

export PATH="/cluster/project/cvg/labelmaker/miniconda3/bin:${PATH}"

env_name=labelmaker-pointcept
eval "$(conda shell.bash hook)"
conda activate $env_name
conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export CUDA_HOME=$CUDA_PATH

export PYTHONWARNINGS="ignore"

which python

cd /cluster/project/cvg/labelmaker/LabelMaker-Pointcept

# export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"
# export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5"
export CUDA_VISIBLE_DEVICES="0,1,2,3"
# export CUDA_VISIBLE_DEVICES="0,1,2"
# export CUDA_VISIBLE_DEVICES="0,1"
# export CUDA_VISIBLE_DEVICES="0"

export OMP_NUM_THREADS=1
export USE_SIMPLE_THREADED_LEVEL3=1

INTERPRETER_PATH=/cluster/project/cvg/labelmaker/miniconda3/envs/labelmaker-pointcept/bin/python

# NUM_GPU=8
# NUM_GPU=6
NUM_GPU=4
# NUM_GPU=3
# NUM_GPU=2

# DATASET_NAME=scannet200
DATASET_NAME=scannetpp
# DATASET_NAME=scannet
# DATASET_NAME=alc
# DATASET_NAME=structured3d

# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20241108-submit"
# EXP_NAME=20241108_ppt_submit

CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20241108-euler"
EXP_NAME=20241108_ppt_no_val

RESUME=false
# RESUME=true

sh scripts/train.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -c ${CONFIG_NAME} \
    -n ${EXP_NAME} \
    -r ${RESUME}
