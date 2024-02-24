source_dir=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/scannet
target_dir=/home/guangda/repos/LabelMaker-Pointcept/data/scannet

rsync -r --checksum -v -e ssh \
    guanji@euler.ethz.ch:$source_dir/* \
    $target_dir
