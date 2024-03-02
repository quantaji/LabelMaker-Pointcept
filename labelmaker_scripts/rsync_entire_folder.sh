#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-rsync"
#SBATCH --output=rsync.out
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH -A ls_polle
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=2G
#SBATCH --tmp=32G

module purge
module load eth_proxy

# rsync scennet necessary files to a temporary folder
source_dir=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept
target_dir=/workspace/LabelMaker-Pointcept

rsync -r -v -e "ssh -p 22184 -i ~/.ssh/id_rsa" \
    --exclude='exp' \
    $source_dir/ \
    admin@194.68.245.82:$target_dir

nohup rsync -r -v -e "ssh -p 13000 -i ~/.ssh/id_rsa" --exclude='exp' /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/ admin@94.101.98.117:/workspace/LabelMaker-Pointcept/ >rsync.log 2>&1 &

nohup rsync  --checksum -r -v -e "ssh -p 13000 -i ~/.ssh/id_rsa" --exclude='exp' /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/ admin@94.101.98.117:/workspace/LabelMaker-Pointcept/ >rsync_checksum.log 2>&1 &

nohup rsync -r -v -e "ssh -p 33798 -i ~/.ssh/id_rsa" /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp/ root@94.101.98.117:/workspace/LabelMaker-Pointcept/exp/ >rsyn_exp.log 2>&1 &
