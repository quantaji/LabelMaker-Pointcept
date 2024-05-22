# first rsync all data from euler to herman's machine
rsync -r --ignore-existing -v -e ssh guanji@euler.ethz.ch:/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/* /home/guangda/repos/LabelMaker-Pointcept/data/

# then rsync all data from herman's zurich machine to cluster
rsync -r --ignore-existing -v -e ssh  guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/data/* /home/blum/LabelMaker-Pointcept/data/
