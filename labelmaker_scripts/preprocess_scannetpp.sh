conda activate labelmaker

python /mnt/LabelMaker/LabelMaker-Pointcept/pointcept/datasets/preprocessing/scannetpp/preprocess_scannetpp.py --dataset_root /mnt/ScanNet++ --output_root /mnt/LabelMaker/LabelMaker-Pointcept/data/scannetpp --num_cpu 8
