source_dir=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp
target_dir=/home/guangda/repos/LabelMaker-Pointcept/exp

rsync -r --ignore-existing -v -e ssh \
    guanji@euler.ethz.ch:$source_dir/* \
    $target_dir
