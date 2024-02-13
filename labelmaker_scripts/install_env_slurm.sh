#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-env-build"
#SBATCH --output=labelmaker_pointcept_env_build.out
#SBATCH --time=2:00:00
#SBATCH --ntasks=1
#SBATCH -A ls_polle
#SBATCH --cpus-per-task=6
#SBATCH --mem-per-cpu=4G
#SBATCH --tmp=32G
#SBATCH --gpus=rtx_3090:1

set -e

module purge
module load eth_proxy


env_name=labelmaker-pointcept
conda create --name $env_name --yes python=3.9
eval "$(conda shell.bash hook)"
conda activate $env_name

INSTALLED_GCC_VERSION="9.5.0"
INSTALLED_CUDA_VERSION="11.3.1"
INSTALLED_CUDA_ABBREV="cu113"
INSTALLED_PYTORCH_VERSION="1.12.1"
INSTALLED_TORCHVISION_VERSION="0.13.1"
INSTALLED_TORCHAUDIO_VERSION="0.12.1"

conda install -y -c conda-forge gxx=${INSTALLED_GCC_VERSION} sysroot_linux-64=2.17 libcxx
conda install -y -c "nvidia/label/cuda-${INSTALLED_CUDA_VERSION}" cuda

pip install torch==${INSTALLED_PYTORCH_VERSION} torchvision==${INSTALLED_TORCHVISION_VERSION} torchaudio==${INSTALLED_TORCHAUDIO_VERSION} --index-url https://download.pytorch.org/whl/${INSTALLED_CUDA_ABBREV}

pip install sharedarray tensorboard tensorboardx yapf addict einops scipy plyfile termcolor timm torch-geometric spconv-cu113 h5py pyyaml numpy

pip install torch-scatter==2.1.0 torch-sparse==0.6.16 torch-cluster==1.6.0 --index-url "" -f "https://data.pyg.org/whl/torch-${INSTALLED_PYTORCH_VERSION}%2B${INSTALLED_CUDA_ABBREV}.html"

cd libs/pointops

conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

conda deactivate
conda activate ${env_name}

which nvcc
nvcc --version

export BUILD_WITH_CUDA=1
export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export PATH="$conda_home/bin:$PATH"
export CUDA_HOME=$CUDA_PATH
export FORCE_CUDA=1
export MAX_JOBS=6
export TORCH_CUDA_ARCH_LIST="6.0 6.1 6.2 7.0 7.2 7.5 8.0 8.6"

python setup.py install
cd ../..
