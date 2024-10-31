#!/usr/bin/bash
#SBATCH --job-name="pointcept-train"
#SBATCH --output=ptv3_train_%j.out
#SBATCH --time=120:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=5G
#SBATCH -A ls_polle
#SBATCH --gpus=rtx_3090:8

module purge
# module load gcc/11.4.0 cuda/12.1.1 eth_proxy
module load stack/2024-06 gcc/12.2.0 cuda/12.1.1 eth_proxy

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

export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"
# export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5"
# export CUDA_VISIBLE_DEVICES="0,1,2,3"
# export CUDA_VISIBLE_DEVICES="0,1,2"
# export CUDA_VISIBLE_DEVICES="0,1"
# export CUDA_VISIBLE_DEVICES="0"

export OMP_NUM_THREADS=1
export USE_SIMPLE_THREADED_LEVEL3=1

INTERPRETER_PATH=/cluster/project/cvg/labelmaker/miniconda3/envs/labelmaker-pointcept/bin/python

NUM_GPU=8
# NUM_GPU=6
# NUM_GPU=4
# NUM_GPU=3
# NUM_GPU=2

# DATASET_NAME=scannet200
DATASET_NAME=scannetpp
# DATASET_NAME=scannet
# DATASET_NAME=alc
# DATASET_NAME=structured3d

# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20240805"
# CONFIG_NAME="semseg-pt-v3m1-0-base-wn199-rebuttal-100p"
# CONFIG_NAME="semseg-pt-v3m1-0-base-wn199-rebuttal-retrain"
# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-train-val"
# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-trial-1"
CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-trial-2"
# CONFIG_NAME="semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-trial-3"
# CONFIG_NAME="semseg-pt-v3m1-0-base-structured3d-rebuttal"
# CONFIG_NAME=semseg-pt-v3m1-0-base-ft
# CONFIG_NAME=insseg-pointgroup-v1m1-pt-v3m1-base
# CONFIG_NAME=insseg-pointgroup-v1m1-ppt-v1m2-pt-v3m1-finetune-linear
# CONFIG_NAME=insseg-pointgroup-v1m1-ppt-v1m2-pt-v3m1-finetune-full


# EXP_NAME=instance_segmentation_base
# EXP_NAME=instance_segmentation_base_test
# EXP_NAME=instance_segmentation_ppt_pretrain_ft_linear
# EXP_NAME=instance_segmentation_ppt_pretrain_ft_full
# EXP_NAME=ppt_alc_structured3d_scannet200_a100_40
# EXP_NAME=alc_100p_pretrain
# EXP_NAME=semseg-pt-v3m1-0-base-wn199-rebuttal-retrain
# EXP_NAME=semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive
# EXP_NAME=semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-no-val
# EXP_NAME=semseg-pt-v3m1-1-ppt-extreme-alc-20240823-massive-train-val
# EXP_NAME=structured3d_100p_pretrain
# EXP_NAME=rebuttal_50p_ft_linear
# EXP_NAME=rebuttal_100p_ft_linear
# EXP_NAME=rebuttal_100p_ft
# EXP_NAME=rebuttal_20p_ft
# EXP_NAME=rebuttal_0p_ft
# EXP_NAME=rebuttal_structured3d_ft_linear
# EXP_NAME=rebuttal_structured3d_ft
EXP_NAME=ppt_no_val_no_scannet_bs_16
# EXP_NAME=ppt_no_val_no_scannet_no_scannet200_bs_16

RESUME=false
# RESUME=true

sh scripts/train.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -c ${CONFIG_NAME} \
    -n ${EXP_NAME} \
    -r ${RESUME}
