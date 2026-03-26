# LICENSE: MIT (Gary Peng: Mar. 26, 2026)
# This dockerfile built on AlmaLinux 9
# https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/#docker-image-and-continuous-integration-ci

# FastFrames image source:
FROM gitlab-registry.cern.ch/atlas-amglab/fastframes:v6.4.0

LABEL maintainer="Gary Peng <yygarypeng@gapp.nthu.edu.tw>"

ENV SUDO_FORCE_REMOVE=yes

RUN set -eux; \
    yum install -y epel-release; \
    buildDeps="git vim wget openssl htop glances"; \
    yum install -y --setopt=skip_if_unavailable=True --nobest $buildDeps; \
    yum clean all; \
    rm -rf /var/cache/yum

ADD bashrc.sh /root/bashrc.sh
RUN cat /root/bashrc.sh >> ~/.bashrc && \
    rm /root/bashrc.sh

CMD ["/bin/bash"]