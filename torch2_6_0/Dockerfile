# LICENSE: MIT (Gary Peng: Apr. 15, 2025)
# This dockerfile built on the Ubuntu 24.04.1 LTS with nv GPU driver Version 550.144.03 and highest CUDA version 12.4

FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel

LABEL maintainer="Gary Peng <yygarypeng@gapp.nthu.edu.tw>"

ENV SUDO_FORCE_REMOVE=yes
ENV DEBIAN_FRONTEND=noninteractive

RUN buildDeps="git vim wget openssl htop glances libgl1-mesa-glx" && \
    apt-get update && \
    apt-get install --assume-yes apt-utils && \
    apt-get install -y $buildDeps && \
    apt-get autoremove -y && \
    apt-get clean

ADD torch_2_6_0.yml /workspace/torch.yml 

RUN mkdir ~/work/ && \
    mkdir ~/data/

ADD bashrc.sh /root/bashrc.sh
RUN cat /root/bashrc.sh >> ~/.bashrc && \
    rm /root/bashrc.sh

# Add test code in home directory
ADD test.py /root/test.py
ADD gitconfig /root/.gitconfig

CMD ["/bin/bash"]
