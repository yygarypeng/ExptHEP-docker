#!/bin/bash

# Meed to install cvmfs outside the containers (need to be as an admin)
# This can work for Ubuntu 24.04.4 LTS
# https://cvmfs.readthedocs.io/en/2.3/cpt-quickstart.html#installation

sudo apt update
sudo apt install -y curl gnupg

curl -fsSL https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest_all.deb -o cvmfs-release.deb
sudo dpkg -i cvmfs-release.deb

sudo apt update
sudo apt install -y cvmfs cvmfs-config-default

echo "CVMFS_REPOSITORIES=atlas.cern.ch,atlas-condb.cern.ch,sft.cern.ch,atlas-nightlies.cern.ch,unpacked.cern.ch

CVMFS_HTTP_PROXY=DIRECT
CVMFS_DNS_ROAMING=yes

CVMFS_QUOTA_LIMIT=100000
CVMFS_CACHE_BASE=/var/lib/cvmfs

CVMFS_TIMEOUT=5
CVMFS_TIMEOUT_DIRECT=10
CVMFS_MAX_RETRIES=2

CVMFS_NFILES=65536
CVMFS_IPFAMILY_PREFER=4" | sudo tee /etc/cvmfs/default.local

sudo cvmfs_config setup
sudo cvmfs_config probe

ls /cvmfs/atlas.cern.ch
cat /etc/cvmfs/default.local
