# Need to have CVMFS mounted to /cvmfs, and data mounted to /root/data/ and /data/shared/
docker run --name ${USER}_lxplus_local \
    --gpus all \
    -v /data/${USER}/:/root/data/ \
    -v /data/share/:/root/share/ \
    -v /cvmfs:/cvmfs/ \
    -it atlas-fastframes:v6.4.0
