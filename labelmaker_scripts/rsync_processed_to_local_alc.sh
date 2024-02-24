source_dir=/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/alc
target_dir=/home/guangda/repos/LabelMaker-Pointcept/data/alc

rsync -r --checksum -v -e ssh \
    guanji@euler.ethz.ch:$source_dir/* \
    $target_dir
