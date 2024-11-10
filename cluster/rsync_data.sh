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

## rsync scannet mix3d data for evaluation
rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/mnt/LabelMaker/labelmaker-mix3d/data/processed/scannet/* /home/guangda/repos/LabelMaker-Pointcept/data/mix3d_preprocessed/scannet/

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/mnt/LabelMaker/labelmaker-mix3d/data/processed/scannet200/* /home/guangda/repos/LabelMaker-Pointcept/data/mix3d_preprocessed/scannet200/

## rsync original ptv3 checkpoints to this repo
rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Models/PointTransformerV3/scannet-semseg-pt-v3m1-0-base/* /home/guangda/repos/LabelMaker-Pointcept/exp/scannet/original-semseg-pt-v3m1-0-base/

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Models/PointTransformerV3/scannet-semseg-pt-v3m1-1-ppt-extreme/* /home/guangda/repos/LabelMaker-Pointcept/exp/scannet/original-semseg-pt-v3m1-1-ppt-extreme/

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/scratch/quanta/Models/PointTransformerV3/scannet200-semseg-pt-v3m1-0-base/* /home/guangda/repos/LabelMaker-Pointcept/exp/scannet200/original-semseg-pt-v3m1-0-base/

# rsync mix3d exp
rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/mnt/LabelMaker/labelmaker-mix3d/saved/evaluation_scannet200/* /home/guangda/repos/labelmaker-mix3d-exps/evaluation_scannet200/

rsync -r --ignore-existing -v -e ssh /home/guangda/repos/LabelMaker-Pointcept/exp/* quanta@rowletew.hopto.org:/mnt/LabelMaker/LabelMaker-Pointcept/exp

rsync -r --ignore-existing -v -e ssh quanta@rowletew.hopto.org:/mnt/LabelMaker/LabelMaker-Pointcept/exp/* /home/guangda/repos/LabelMaker-Pointcept/exp/

rsync -r --ignore-existing -v -e ssh /raid/LabelMaker-Pointcept/exp/* guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/exp/

rsync -r --ignore-existing -v -e "ssh -p 22000" ml2ran11s1:/raid/LabelMaker-Pointcept/* /raid/LabelMaker-Pointcept/

rsync -r --ignore-existing -v -e ssh /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp/scannetpp/baseline_from_scratch/* guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/exp/scannetpp/baseline_from_scratch/

rsync -r --ignore-existing -v -e ssh /cluster/project/cvg/labelmaker/LabelMaker-Pointcept/exp/scannet200/ppt_pretrain_scannet200_finetune_retry/* guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/exp/scannet200/ppt_pretrain_scannet200_finetune_retry/

# rsync -r --ignore-existing -v -e ssh guangda@129.132.245.59:/home/guangda/repos/LabelMaker-Pointcept/exp/scannet200/ppt_pretrain_scannet200_finetune_retry/* /mnt/LabelMaker/LabelMaker-Pointcept/exp/scannet200/ppt_pretrain_scannet200_finetune_retry/


rsync -r --ignore-existing -v -e ssh /home/guangda/repos/LabelMaker-Pointcept/exp/scannet200/ppt_pretrain_scannet200_finetune_retry/* quanta@rowletew.hopto.org:/mnt/LabelMaker/LabelMaker-Pointcept/exp/scannet200/ppt_pretrain_scannet200_finetune_retry/
