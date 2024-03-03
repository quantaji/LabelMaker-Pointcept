
env_name=labelmaker-pointcept
eval "$(conda shell.bash hook)"
conda activate $env_name
conda_home="$(conda info | grep "active env location : " | cut -d ":" -f2-)"
conda_home="${conda_home#"${conda_home%%[![:space:]]*}"}"

export CUDA_HOST_COMPILER="$conda_home/bin/gcc"
export CUDA_PATH="$conda_home"
export CUDA_HOME=$CUDA_PATH

which python

# source_dir=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept
# target_dir=$TMPDIR/LabelMaker-Pointcept
# echo "Start coping files!"
# rsync -r \
#     --exclude="data/s3dis" \
#     --exclude="data/scannet" \
#     --exclude="data/structured3d" \
#     $source_dir/ \
#     $target_dir
# echo "Files copy finished!"

# cd $target_dir

# cd /cluster/project/cvg/labelmaker/LabelMaker-Pointcept
cd /home/guangda/repos/LabelMaker-Pointcept

# export CUDA_VISIBLE_DEVICES="0,1,2,3"
export CUDA_VISIBLE_DEVICES="0"

INTERPRETER_PATH=/home/guangda/miniconda3/envs/labelmaker-pointcept/bin/python
NUM_GPU=1
DATASET_NAME=scannet200
CONFIG_NAME="semseg-pt-v3m1-0-base-test"
EXP_NAME=alc_pretrain_scannet200_ft

sh scripts/test.sh \
    -p ${INTERPRETER_PATH} \
    -g ${NUM_GPU} \
    -d ${DATASET_NAME} \
    -c ${CONFIG_NAME} \
    -n ${EXP_NAME} \
    -w ${CKPT_PATH}
