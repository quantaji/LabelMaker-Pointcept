#!/usr/bin/bash
#SBATCH --job-name="ptv3_scannet_finetune"
#SBATCH --output=ptv3_scannet_finetune_%j.out
#SBATCH --time=4:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=8G
#SBATCH -A ls_polle
#SBATCH --gpus=rtx_3090:4

module purge
module load gcc/11.4.0 cuda/12.1.1 eth_proxy

export PATH="/cluster/project/cvg/labelmaker/miniconda3/bin:${PATH}"

env_name=labelmaker-pointcept
eval "$(conda shell.bash hook)"
conda activate $env_name
conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export CUDA_HOME=$CUDA_PATH

which python

cd /cluster/project/cvg/labelmaker/LabelMaker-Pointcept

export CUDA_VISIBLE_DEVICES="0,1,2,3"
# export CUDA_VISIBLE_DEVICES="0"

INTERPRETER_PATH=/cluster/project/cvg/labelmaker/miniconda3/envs/labelmaker-pointcept/bin/python
NUM_GPU=4
DATASET_NAME=scannet200
CONFIG_NAME="semseg-pt-v3m1-1-finetune"
# CONFIG_NAME="semseg-pt-v3m1-0-base-wn199"
EXP_NAME=ppt_pretrain_scannet200_finetune
# EXP_NAME=arkitscenes_labelmaker_wn199_pretrain

sh scripts/train.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -c ${CONFIG_NAME} \
    -n ${EXP_NAME} -r true
