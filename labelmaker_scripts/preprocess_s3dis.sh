#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-s3dis-preprocess"
#SBATCH --output=labelmaker_pointcept_s3dis_preprocess.out
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH -A ls_polle
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=2G
#SBATCH --tmp=192G

set -e

module purge
module load eth_proxy

export PATH="/cluster/project/cvg/labelmaker/miniconda3/bin:${PATH}"

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

S3DIS_DIR=/cluster/project/cvg/labelmaker/S3DIS/Stanford3dDataset_v1.2
RAW_S3DIS_DIR=/cluster/project/cvg/labelmaker/S3DIS/Stanford2d3dDataset_noXYZ
PROCESSED_S3DIS_DIR=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/s3dis

cd /cluster/project/cvg/labelmaker/LabelMaker-Pointcept
# python pointcept/datasets/preprocessing/s3dis/preprocess_s3dis.py --dataset_root ${S3DIS_DIR} --output_root ${PROCESSED_S3DIS_DIR} --raw_root ${RAW_S3DIS_DIR} --align_angle --parse_normal
python pointcept/datasets/preprocessing/s3dis/preprocess_s3dis.py --dataset_root ${S3DIS_DIR} --output_root ${PROCESSED_S3DIS_DIR}