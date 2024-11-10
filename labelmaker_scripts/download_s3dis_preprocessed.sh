#!/usr/bin/bash
#SBATCH --job-name="labelmaker-pointcept-s3dis-download"
#SBATCH --output=labelmaker_pointcept_s3dis_download.out
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH -A ls_polle
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=2G
#SBATCH --tmp=12G

cd $TMPDIR

wget https://connecthkuhk-my.sharepoint.com/:u:/g/personal/wuxy_connect_hku_hk/ERtd0QAyLGNMs6vsM4XnebcBseQ8YTL0UTrMmp11PmQF3g?download=1 -O s3dis.zip

unzip -qq s3dis.zip
rm -rf s3dis.zip

cp -r $TMPDIR/* /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data
