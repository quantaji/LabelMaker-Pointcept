source_dir=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp
target_dir=/home/guangda/repos/LabelMaker-Pointcept/exp

rsync -r --ignore-existing -v -e ssh \
    guanji@euler.ethz.ch:$source_dir/* \
    $target_dir


# rsync -r --ignore-existing -v -e ssh guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/exp/scannet/alc_pretrain_scannet20_ft_linear/* /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp/scannet/alc_pretrain_scannet20_ft_linear/
# rsync -r --ignore-existing -v -e ssh guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/exp/ /mnt/LabelMaker/LabelMaker-Pointcept/exp/
