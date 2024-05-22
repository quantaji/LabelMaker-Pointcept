```sh
srun \
    --mem=64GB \
    --export ALL \
    -c 36 \
    --gres=gpu:nvidia_a100-sxm4-40gb:8 \
    --container-name=labelmaker \
    --job-name="labelmaker" \
    -p GPU8 \
    --container-image=nvcr.io/ml2r/interactive_cuda:12.2.0 \
    --mail-user=guanji@student.ethz.ch \
    --mail-type=ALL \
    --pty /bin/bash
```

```sh
srun \
    --mem=64GB \
    --export ALL \
    -c 36 \
    --gres=gpu:nvidia_a100-sxm4-80gb:4 \
    --container-name=labelmaker \
    --job-name="labelmaker" \
    -p GPU4 \
    --container-image=nvcr.io/ml2r/interactive_cuda:12.2.0 \
    --mail-user=guanji@student.ethz.ch \
    --mail-type=ALL \
    --pty /bin/bash
```

```sh
srun \
    --mem=64GB \
    --export ALL \
    -c 8 \
    --gres=gpu:1 \
    --container-name=labelmaker \
    --job-name="labelmaker" \
    -p GPU1 \
    --container-image=nvcr.io/ml2r/interactive_cuda:12.2.0 \
    --mail-user=guanji@student.ethz.ch \
    --mail-type=ALL \
    --pty /bin/bash
```
