#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-structure3d-download"
#SBATCH --output=labelmaker_pointcept_structure3d_download.out
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH -A ls_polle
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=2G
#SBATCH --tmp=1024G

cd $TMPDIR

wget https://connecthkuhk-my.sharepoint.com/:u:/g/personal/wuxy_connect_hku_hk/EaTAxo4SvEJFnDVuv9bOol4B0GCI806BeI4G-TF9Rp7lZw?download=1 -O structured3d.zip

unzip -qq structured3d.zip
rm -rf structured3d.zip

cp -r $TMPDIR/* /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data
