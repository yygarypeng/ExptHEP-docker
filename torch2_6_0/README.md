# ExptHEP Docker: PyTorch 2.6.0 Environment

This directory contains a CUDA-enabled Docker setup for high-energy physics and machine learning workflows based on:

- PyTorch 2.6.0
- CUDA 12.4(container build) / 12.6(venv build)
- cuDNN 9
- Python 3.11 (Conda env: `torch`)
- ROOT 6.38.02

The image is built from `pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel` and installs HEP/ML tooling such as `uproot`, `mplhep`, `xgboost`, `lightning`, and `FrEIA` (for normalizing flows).

## Directory Overview

- `Dockerfile`: Container definition and package installation.
- `build.sh`: Build command for local image.
- `run.sh`: Example command to start an interactive GPU container.
- `test.py`: Environment verification script (imports, CUDA, ROOT JIT, I/O, mini training).
- `installation/torch_2_6_0.yml`: Conda environment spec used in image build.

## Prerequisites

- Linux host with NVIDIA GPU
- NVIDIA driver (pass: 570.211.01) compatible with CUDA 12.4
- Docker/Podman installed and runnable by your user
- NVIDIA Container Toolkit configured for Docker GPU access

Quick check:

```bash
docker --version
nvidia-smi
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

## Build Image

From this directory:

```bash
source build.sh
```

This builds:

```text
ehep-torch-2.6.0:latest
```

Equivalent manual command:

```bash
docker build -t ehep-torch-2.6.0:latest . --no-cache
```

Or you can simply pull from my Docker Hub:

```bash
docker pull yygarypeng/nthu_exphep_torch:latest
```

## Run Container

### Option A: Use the included script

```bash
source run.sh
```

Notes:

- `run.sh` copies `installation/` to `/data/${USER}/` on the host before launching the container.
- The script currently runs image `yygarypeng/nthu_exphep_torch:latest`.
- If you built locally with `build.sh`, update `run.sh` image name to `ehep-torch-2.6.0:latest` or run manually (Option B).

### Option B: Run manually with local image

```bash
docker run --name test \
	--cpuset-cpus="0-8" \
	--gpus all \
	-v /data/${USER}/:/root/data/ \
	-it ehep-torch-2.6.0:latest
```

## Inside the Container

Container startup behavior from `bashrc.sh`:

- Activates conda env `torch`
- Changes directory to `~/work`

Useful aliases are preconfigured:

- `data` -> `cd ~/data/`
- `work` -> `cd ~/work/`
- `home` -> `cd ~`
- `cc` -> `clear`

You also need to copy `/data/${USER}/installation/` to the container (e.g. `cp -r /data/${USER}/installation ~/`) to create a virtual environment from the provided `torch_2_6_0.yml`.
Then, go to `~/installation/` and run:

```bash
source install.sh
```

to install miniconda; then run

```bash
source venv_create.sh
```

to create the `torch` conda environment (follow the instructions when installing the environment). After that, you can activate it with:

```bash
conda activate torch
```

Everytime when you start the container, it will automatically activate the `torch` environment and change to the `~/work` directory.

## Verify Environment

Run:

```bash
python /root/test.py
```

The script checks:

- Core package imports and versions
- CUDA availability and Torch compute
- ROOT C++ JIT functionality
- ROOT to NumPy conversion
- Uproot ROOT file writing
- Lightning mini training loop

## Conda Environment Contents

Defined in `installation/torch_2_6_0.yml`:

- Python 3.11
- Jupyter
- pandas, pytables, numba, scipy
- matplotlib, seaborn
- scikit-learn
- xgboost, shap
- uproot, mplhep, h5py
- wandb
- pytorch=2.6
- lightning=2.4
- root=6.38.02
- pip package: FrEIA