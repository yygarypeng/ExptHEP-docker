# Here the data path is set to `/data/${USER}/`  
# Need to copy `installation` to `/data/${USER}/` first; then move (copy) it to the container when creating the venv.
cp -r ./installation /data/${USER}/
docker run --name test --cpuset-cpus="0-8" --gpus all -v /data/${USER}/:/root/data/ -it yygarypeng/nthu_exphep_torch:latest