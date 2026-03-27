podman run --name ${USER}_lxplus_local \
    --gpus all \
    -v /data/${USER}/:/root/data/ \
    -v /data/share/:/root/share/ \
    -v /cvmfs:/cvmfs:shared \
    -it atlas-fastframes:v6.4.0
