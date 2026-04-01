# LICENSE: MIT (Gary Peng: Apr. 01, 2026)
# This dockerfile built on the Ubuntu 24.04.4 LTS with nv GPU driver Version 570.211.01 and `highest` CUDA version 12.8

FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel

LABEL maintainer="Gary Peng <yygarypeng@gapp.nthu.edu.tw>"

ENV SUDO_FORCE_REMOVE=yes
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/conda/bin:$PATH

RUN buildDeps="git vim wget openssl htop glances" && \
    apt-get update && \
    apt-get install --assume-yes apt-utils && \
    apt-get install -y $buildDeps && \
    apt-get autoremove -y && \
    apt-get clean

ADD installation/torch_2_6_0.yml /workspace/torch_2_6_0.yml
RUN conda env create --name torch -f /workspace/torch_2_6_0.yml
RUN conda init bash

RUN mkdir ~/work/ && \
    mkdir ~/data/

ADD bashrc.sh /root/bashrc.sh
RUN cat /root/bashrc.sh >> ~/.bashrc && \
    rm /root/bashrc.sh

# Add test code in home directory
ADD test.py /root/test.py
ADD gitconfig /root/.gitconfig

CMD ["/bin/bash"]
