name="test"
container_name="${name}_env"
workdir="/data/${name}"
image="$ubunut:22.04"

docker run -it \
    	--name ${container_name} \
    	--hostname ${name}-env \
    	-v ${workdir}:/data:rw \
    	--memory=4096m \
    	--cpus=8 \
    	--cap-drop=ALL \
    	--cap-add=CHOWN \
    	--cap-add=SETUID \
    	--cap-add=SETGID \
    	--cap-add=FOWNER \
    	--cap-add=DAC_OVERRIDE \
    	--cap-add=NET_BIND_SERVICE \
    	--security-opt=no-new-privileges \
    	${image} /bin/bash
