#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-alc-preprocess"
#SBATCH --output=labelmaker_pointcept_alc_preprocess.out
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH -A ls_polle
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=2G
#SBATCH --tmp=32G

set -e

module purge
module load eth_proxy

env_name=labelmaker-pointcept
eval "$(conda shell.bash hook)"
conda activate $env_name

which python
which pip

conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export PATH="$conda_home/bin:$PATH"
export CUDA_HOME=$CUDA_PATH

# RAW_SCANNET_DIR=/media/hermann/data/labelmaker/ARKitScene_LabelMaker
# PROCESSED_SCANNET_DIR=/home/guangda/repos/LabelMaker-Pointcept/data/alc

RAW_SCANNET_DIR=/cluster/project/cvg/labelmaker/ARKitScene_LabelMaker
PROCESSED_SCANNET_DIR=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/alc

# RAW_SCANNET_DIR: the directory of downloaded ScanNet v2 raw dataset.
# PROCESSED_SCANNET_DIR: the directory of the processed ScanNet dataset (output dir).
python pointcept/datasets/preprocessing/alc/preprocess_arkitscenes_labelmaker_consensus.py --dataset_root ${RAW_SCANNET_DIR} --output_root ${PROCESSED_SCANNET_DIR}
