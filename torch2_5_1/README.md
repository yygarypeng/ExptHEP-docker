# ExptHEP Docker: PyTorch 2.5.1 Environment

This directory contains a CUDA-enabled Docker setup for high-energy physics and machine learning workflows.

## Key Specifications

- **Base Image**: `pytorch/pytorch:2.5.1-cuda11.8-cudnn9-devel`
- **Host Requirements**: Linux host with NVIDIA GPU, Docker/Podman, and NVIDIA Container Toolkit
- **PyTorch**: 2.5.1 with torchvision 0.20.1 and torchaudio 2.5.1
- **CUDA/cuDNN**: 11.8 and 9 (in container)
- **Python**: 3.10 (in conda env `torch`)
- **ROOT**: 6.38.02
- **Environment Manager**: Mamba (conda-compatible, faster)

The `torch` conda environment is created during Docker build using mamba. All dependencies are pre-installed, so no setup is required after container starts.

## Directory Overview

- `Dockerfile`: Container definition, system packages (git, vim, wget, openssh-client, htop), and conda environment setup.
- `torch_2_5_1.yml`: Conda environment specification (packages, dependencies, and pip wheels).
- `bashrc.sh`: Bash configuration with git branch display, aliases, and tab completion.
- `gitconfig`: Git configuration file for the root user.
- `build.sh`: Build command for local image.
- `run.sh`: Command to run container with recommended GPU and CPU settings.
- `test.py`: Comprehensive environment verification script (package imports, CUDA availability, version checks).

## Prerequisites

- Linux host with NVIDIA GPU
- NVIDIA driver new enough for CUDA 11.8 container runtime
- Docker/Podman installed and runnable by your user
- NVIDIA Container Toolkit configured for Docker GPU access

Quick check:

```bash
docker --version
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

## Build Image

From this directory:

```bash
bash build.sh
```

This builds the image `ehep-torch-2.5.1:latest` locally.

**Option 1: Build locally**
```bash
docker build -t ehep-torch-2.5.1:latest . --no-cache
```

**Option 2: Pull from Docker Hub**
```bash
docker pull yygarypeng/nthu_exphep_torch:latest
```

## Run Container

### Quick Start (with run.sh)
If you have pulled the image from Option 2, simply run:

```bash
bash run.sh
```

This runs the container with preset GPU and CPU configurations. Adjust `--cpuset-cpus` based on your system's CPU topology.

### Manual Run (local image)

```bash
docker run --name torch \
  --cpuset-cpus="0-8" \
  --gpus all \
  -v /data/${USER}/:/root/data/ \
  -it ehep-torch-2.5.1:latest
```

### Notes on Configuration

- **`--cpuset-cpus`**: Restrict CPU usage to avoid contention with other containers. Customize based on your system (e.g., `0-8` for 9 cores, `0-15` for 16 cores).
- **`--gpus all`**: Passes all GPUs to the container. Requires NVIDIA Container Toolkit.
- **`-v /data/${USER}/:/root/data/`**: Mounts host directory `/data/${USER}/` to container `/root/data/`. Create the directory first if needed.
- **`--name torch`**: Container name for easy `docker exec` and management.

## Inside the Container

### Automatic Startup

When the container starts (`bashrc.sh` customizations):

1. Conda environment `torch` is activated
2. Working directory changes to `~/work/`
3. Shell prompt displays git branch if in a git repository

### Preset Aliases

- `cc` → `clear`
- `data` → `cd ~/data/`
- `work` → `cd ~/work/`
- `home` → `cd ~`

### Tab Completion

- Case-insensitive tab completion
- Shows all completions on ambiguous matches
- Menu-based completion with arrow keys

### Pre-installed Tools (System)

- Git, Vim, Wget, OpenSSH client, htop

### Environment Testing

Run `python test.py` to verify the environment:

- Core stack (torch, torchvision, torchaudio, lightning, xgboost)
- All Python packages and versions
- CUDA availability and GPU detection
- ROOT integration

### Conda Environment (`torch`)

The `torch` environment includes:

**Core ML/Data Science:**
- PyTorch 2.5.1, torchvision 0.20.1, torchaudio 2.5.1
- Lightning 2.4.x
- scikit-learn, xgboost, shap
- pandas, numpy, scipy, numba
- matplotlib, seaborn, pydot

**HEP-specific:**
- ROOT 6.38.02
- uproot, mplhep

**Other Tools:**
- Jupyter, h5py, wandb, FrEIA (normalizing flows)

Modify the environment by editing `torch_2_5_1.yml` and rebuilding the image.

## Verify Environment

Run:

```bash
python /root/test.py
```

The script performs a comprehensive check of:

- Core ML stack (PyTorch, torchvision, torchaudio, lightning, xgboost)
- All required Python packages (pandas, scikit-learn, uproot, mplhep, etc.)
- CUDA availability and GPU detection
- ROOT integration

## Testing Env Setup Commands

```bash
# Check environment is working
python test.py

# Verify GPU access
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

## Build Metadata

- **License**: MIT
- **Maintainer**: Gary Peng <yygarypeng@gapp.nthu.edu.tw>
- **Build Date**: April 1, 2026
- **Host System Used for Build**: Ubuntu 22.04.3 LTS
- **NVIDIA Driver (Build Host)**: 535.129.03
- **CUDA (Build Host)**: 12.2