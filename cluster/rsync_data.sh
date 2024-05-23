# first rsync all data from euler to herman's machine
rsync -r --ignore-existing -v -e ssh guanji@euler.ethz.ch:/cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/* /home/guangda/repos/LabelMaker-Pointcept/data/

# then rsync all data from herman's zurich machine to cluster
rsync -r --ignore-existing -v -e ssh guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/data/* /raid/LabelMaker-Pointcept/data/

# rsync new data into the repo
rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/scannet-compressed/scannet/* /raid/LabelMaker-Pointcept/data/scannet

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/s3dis-compressed/* /raid/LabelMaker-Pointcept/data/s3dis

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/structured3d-compressed/structured3d/* /raid/LabelMaker-Pointcept/data/structured3d

# sync to herman's zurich machine
# rsync new data into the repo
rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/scannet-compressed/scannet/* /home/guangda/repos/LabelMaker-Pointcept/data/scannet

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/s3dis-compressed/* /home/guangda/repos/LabelMaker-Pointcept/data/s3dis

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/structured3d-compressed/structured3d/* /home/guangda/repos/LabelMaker-Pointcept/data/structured3d

# rsync to euler
rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/scannet-compressed/scannet/* /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/scannet

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/s3dis-compressed/* /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/s3dis

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Datasets/structured3d-compressed/structured3d/* /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/data/structured3d

## checksum
rsync -r --checksum -v -e ssh guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/data/* /raid/LabelMaker-Pointcept/data/
