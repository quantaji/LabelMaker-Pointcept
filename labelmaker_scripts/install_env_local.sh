set -e

export CRYPTOGRAPHY_OPENSSL_NO_LEGACY=true
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
REPO_DIR=$SCRIPT_DIR/..

env_name=labelmaker-pointcept
conda create --name $env_name --yes python=3.9
eval "$(conda shell.bash hook)"
conda activate $env_name

INSTALLED_GCC_VERSION="9.5.0"
INSTALLED_CUDA_VERSION="11.8.0"
INSTALLED_CUDA_ABBREV="cu118"
INSTALLED_PYTORCH_VERSION="2.1.0"
INSTALLED_TORCHVISION_VERSION="0.16.0"
INSTALLED_TORCHAUDIO_VERSION="2.1.0"

conda install -y -c conda-forge gxx=${INSTALLED_GCC_VERSION} sysroot_linux-64=2.17 libcxx
conda install -y -c "nvidia/label/cuda-${INSTALLED_CUDA_VERSION}" cuda

pip install torch==${INSTALLED_PYTORCH_VERSION} torchvision==${INSTALLED_TORCHVISION_VERSION} torchaudio==${INSTALLED_TORCHAUDIO_VERSION} --index-url https://download.pytorch.org/whl/${INSTALLED_CUDA_ABBREV}

pip install sharedarray tensorboard tensorboardx yapf addict einops scipy plyfile termcolor timm torch-geometric spconv-cu113 h5py pyyaml numpy trimesh pandas scikit-learn

pip install torch-scatter==2.1.2 torch-sparse==0.6.18 torch-cluster==1.6.2 --index-url "" -f "https://data.pyg.org/whl/torch-${INSTALLED_PYTORCH_VERSION}%2B${INSTALLED_CUDA_ABBREV}.html"

cd ${REPO_DIR}/libs/pointops

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
export MAX_JOBS=8
export TORCH_CUDA_ARCH_LIST="6.0 6.1 6.2 7.0 7.2 7.5 8.0 8.6"

python setup.py install

pip install spconv-cu118

pip install flash-attn --no-build-isolation

pip install https://github.com/cvg/open3d-manylinux2014/releases/download/0.17.0/open3d_cpu-0.17.0-cp39-cp39-manylinux_2_17_x86_64.whl

# install labelmaker
pip install -U "git+https://github.com/cvg/LabelMaker.git"

pip install yapf==0.40.1

pip install git+https://github.com/openai/CLIP.git

# install point group for instance segmentation
conda install -y -c bioconda google-sparsehash
cd ${REPO_DIR}/libs/pointgroup_ops
python setup.py install --include_dirs=${CONDA_PREFIX}/include
