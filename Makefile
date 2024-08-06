makeFileDir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

start: build 
	podman run -d \
		-p 8000:8000 \
		-v $(makeFileDir)/jhub_config:/etc/jupyterhub:z \
		--name jhub \
		jhub:latest
		#-v $(makeFileDir)/auth.py:/usr/local/lib/python3.10/dist-packages/jupyterhub/auth.py:z \

build:
	podman build -f Containerfile -t jhub


restart: destroy start

stop:
	podman stop jhub

destroy: stop
	podman rm jhub
