# LICENSE: MIT (Gary Peng: Jan. 19, 2025)
# This dockerfile built on the Ubuntu 24.04.1 LTS with nv GPU driver Version 550.127.08 andCUDA version 12.4; the base server env is from TensorFlow official image (tensorflow/tensorlfow:2.16.1-gpu)

FROM tensorflow/tensorflow:2.16.1-gpu

LABEL maintainer="Gary Peng <yygarypeng@gapp.nthu.edu.tw>"

ENV SUDO_FORCE_REMOVE=yes
ENV DEBIAN_FRONTEND=noninteractive

RUN buildDeps="git vim wget openssl htop glances libgl1-mesa-glx" && \
    apt-get update && \
    apt-get install --assume-yes apt-utils && \
    apt-get install -y $buildDeps && \
    apt-get clean
RUN mkdir -p ~/miniconda3 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh && \
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && \
    rm -rf ~/miniconda3/miniconda.sh
ENV PATH=/root/miniconda3/bin:$PATH
RUN conda init

ADD tf_2_16.yml /root/miniconda3/tf.yml 
RUN conda env create --name tf -f /root/miniconda3/tf.yml

RUN mkdir ~/work/ && \
    mkdir ~/data/

ADD bashrc.sh /root/bashrc.sh
RUN cat /root/bashrc.sh >> ~/.bashrc && \
    rm /root/bashrc.sh

# Add test code in home directory
ADD test.py /root/test.py
ADD gitconfig /root/.gitconfig

CMD ["/bin/bash"]
