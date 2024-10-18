# source_dir=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp/alc/alc_100p_pretrain
# target_dir=/home/guangda/repos/LabelMaker-Pointcept/exp/alc/alc_100p_pretrain
# /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp/alc/

# rsync -r --ignore-existing -v -e ssh \
#     guanji@euler.ethz.ch:$source_dir/* \
#     $target_dir


# source_pth=/home/guangda/repos/LabelMaker-Pointcept/exp/alc/alc_100p_pretrain/model/model_mod_scannet200.pth
# target_pth=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp/alc/alc_100p_pretrain/model/model_mod_scannet200.pth

# rsync -r --ignore-existing -v -e ssh \
#     $source_pth \
#     guanji@euler.ethz.ch:$target_pth
