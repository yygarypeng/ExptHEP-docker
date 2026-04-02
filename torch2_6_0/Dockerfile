# LICENSE: MIT (Gary Peng: Apr. 01, 2026)
# This dockerfile built on the Ubuntu 24.04.4 LTS with nv GPU driver Version 570.211.01 and `highest` CUDA version 12.8

FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel

LABEL maintainer="Gary Peng <yygarypeng@gapp.nthu.edu.tw>"

ENV SUDO_FORCE_REMOVE=yes
ENV DEBIAN_FRONTEND=noninteractive

COPY torch_2_6_0.yml /root/torch_2_6_0.yml
COPY bashrc.sh /root/bashrc.sh

RUN buildDeps="git vim wget openssh-client htop" && \
    apt-get update && \
    apt-get install --assume-yes --no-install-recommends apt-utils $buildDeps && \
    rm -rf /var/lib/apt/lists/* && \
    mamba env create --name torch -f /root/torch_2_6_0.yml && \
    mamba clean -afy && \
    mkdir -p /root/work /root/data && \
    cat /root/bashrc.sh >> /root/.bashrc && \
    rm -f /root/bashrc.sh /root/torch_2_6_0.yml

# Add test code in home directory
COPY test.py /root/test.py
COPY gitconfig /root/.gitconfig

CMD ["/bin/bash"]
