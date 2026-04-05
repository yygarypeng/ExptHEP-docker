# LICENSE: MIT (Gary Peng: Apr. 05, 2026)
# This dockerfile built on the Ubuntu 22.04.3 LTS with nv GPU driver Version 535.129.03 and `highest` CUDA version 12.2

FROM pytorch/pytorch:2.5.1-cuda11.8-cudnn9-devel

LABEL maintainer="Gary Peng <yygarypeng@gapp.nthu.edu.tw>"

ENV SUDO_FORCE_REMOVE=yes
ENV DEBIAN_FRONTEND=noninteractive

COPY torch_2_5_1.yml /root/torch_2_5_1.yml
COPY bashrc.sh /root/bashrc.sh

RUN buildDeps="git vim wget openssh-client htop" && \
    apt-get update && \
    apt-get install --assume-yes --no-install-recommends apt-utils $buildDeps && \
    rm -rf /var/lib/apt/lists/* && \
    mamba env create --name torch --file /root/torch_2_5_1.yml && \
    mamba clean -afy && \
    mkdir -p /root/work /root/data && \
    cat /root/bashrc.sh >> /root/.bashrc && \
    rm -f /root/bashrc.sh /root/torch_2_5_1.yml

# Add test code in home directory
COPY test.py /root/test.py
COPY gitconfig /root/.gitconfig

CMD ["/bin/bash"]
