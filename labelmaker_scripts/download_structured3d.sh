#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-structured3d-download"
#SBATCH --output=labelmaker_pointcept_structured3d_download.out
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH -A ls_polle
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=2G
#SBATCH --tmp=32G

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

mkdir -p /cluster/project/cvg/labelmaker/Structured3D
cd /cluster/project/cvg/labelmaker/Structured3D

wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_00.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_01.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_02.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_03.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_04.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_05.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_06.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_07.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_08.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_09.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_10.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_11.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_12.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_13.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_14.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_15.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_16.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_panorama_17.zip

wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_00.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_01.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_02.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_03.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_04.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_05.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_06.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_07.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_08.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_09.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_10.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_11.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_12.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_13.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_14.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_15.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_16.zip
wget --no-verbose https://zju-kjl-jointlab-azure.kujiale.com/zju-kjl-jointlab/Structured3D/Structured3D_perspective_full_17.zip
