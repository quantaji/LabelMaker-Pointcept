#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-scannet-preprocess"
#SBATCH --output=labelmaker_pointcept_scannet_preprocess.out
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

echo $TMPDIR
cd $TMPDIR

wget https://cvg-data.inf.ethz.ch/s3dis/Stanford3dDataset_v1.2.zip
unzip -q Stanford3dDataset_v1.2.zip

mkdir Stanford2d3dDataset_noXYZ
cd Stanford2d3dDataset_noXYZ

wget https://cvg-data.inf.ethz.ch/2d3ds/no_xyz/area_1_no_xyz.tar
tar -xvf area_1_no_xyz.tar

wget https://cvg-data.inf.ethz.ch/2d3ds/no_xyz/area_2_no_xyz.tar
tar -xvf area_2_no_xyz.tar

wget https://cvg-data.inf.ethz.ch/2d3ds/no_xyz/area_3_no_xyz.tar
tar -xvf area_3_no_xyz.tar

wget https://cvg-data.inf.ethz.ch/2d3ds/no_xyz/area_4_no_xyz.tar
tar -xvf area_4_no_xyz.tar

wget https://cvg-data.inf.ethz.ch/2d3ds/no_xyz/area_5a_no_xyz.tar
tar -xvf area_5a_no_xyz.tar

wget https://cvg-data.inf.ethz.ch/2d3ds/no_xyz/area_5b_no_xyz.tar
tar -xvf area_5b_no_xyz.tar

wget https://cvg-data.inf.ethz.ch/2d3ds/no_xyz/area_6_no_xyz.tar
tar -xvf area_6_no_xyz.tar

S3DIS_DIR=$TMPDIR/Stanford3dDataset_v1.2
RAW_S3DIS_DIR=$TMPDIR/Stanford2d3dDataset_noXYZ
PROCESSED_S3DIS_DIR=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/s3dis

cd /cluster/project/cvg/labelmaker/LabelMaker-Pointcept
python pointcept/datasets/preprocessing/s3dis/preprocess_s3dis.py --dataset_root ${S3DIS_DIR} --output_root ${PROCESSED_S3DIS_DIR} --raw_root ${RAW_S3DIS_DIR} --align_angle --parse_normal
