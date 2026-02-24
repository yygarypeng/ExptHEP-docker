name=$(whoami)
container_name="${name}_env"
workdir="/data/${name}"
# image="ubuntu:22.04"
image="docker.io/yygarypeng/nthu_exphep_torch"

podman pull ${image}

podman run -it \
    	--name ${container_name} \
    	--hostname ${name}-env \
    	-v ${workdir}:/data:rw \
    	--memory=32768m \
    	--cpus=16 \
		--device nvidia.com/gpu=all \
    	--cap-drop=ALL \
    	--cap-add=CHOWN \
    	--cap-add=SETUID \
    	--cap-add=SETGID \
    	--cap-add=FOWNER \
    	--cap-add=DAC_OVERRIDE \
    	--cap-add=NET_BIND_SERVICE \
    	--security-opt=no-new-privileges \
    	${image} /bin/bash
