docker run --name torch --cpuset-cpus="0-8" --gpus all -v /data/${USER}/:/root/data/ -it yygarypeng/nthu_exphep_torch:latest
