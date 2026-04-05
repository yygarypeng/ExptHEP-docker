# Here the data path is set to `/data/${USER}/`  
# You need to pull the image first with `docker pull yygarypeng/nthu_exphep_torch:latest` 
# or build it with the provided Dockerfile, and then run the container with the following command:
docker run --name torch --gpus all -v /data/${USER}/:/root/data/ -it ehep-torch-2.5.1:latest
