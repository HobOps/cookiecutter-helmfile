SHELL:=bash

REQUIRED_BINS := python3 helm helmfile sops
$(foreach bin,$(REQUIRED_BINS),\
    $(if $(shell command -v $(bin) 2> /dev/null),$(info Found `$(bin)`),$(error Please install `$(bin)`)))

cluster_apply:
	@if [ -z $(cluster) ]; then\
		echo "cluster is not defined"; exit 1;\
	fi
	helmfile -i -e $(cluster) -f clusters.yaml apply

cluster_diff:
	@if [ -z $(cluster) ]; then\
		echo "cluster is not defined"; exit 1;\
	fi
	helmfile -i -e $(cluster) -f clusters.yaml diff

apply:
	@if [ -z $(env) ]; then\
		echo "env is not defined"; exit 1;\
	fi
	@if [ -z $(name) ]; then\
		helmfile -i -e $(env) apply --show-secrets --suppress-secrets;\
	else\
		helmfile -i -e $(env) -l name=$(name) apply --show-secrets --suppress-secrets;\
	fi

sync:
	@if [ -z $(env) ]; then\
		echo "env is not defined"; exit 1;\
	fi
	@if [ -z $(name) ]; then\
		helmfile -i -e $(env) sync;\
	else\
		helmfile -i -e $(env) -l name=$(name) sync;\

diff:
	@if [ -z $(env) ]; then\
		echo "env is not defined"; exit 1;\
	fi
	@if [ -z $(name) ]; then\
		helmfile -i -e $(env) diff;\
	else\
		helmfile -i -e $(env) -l name=$(name) diff;\
	fi

cluster_template:
	@if [ -z $(cluster) ]; then\
		echo "cluster is not defined"; exit 1;\
	fi
	helmfile -i -e $(cluster) -f clusters.yaml template

template:
	@if [ -z $(env) ]; then\
		echo "env is not defined"; exit 1;\
	fi
	@if [ -z $(name) ]; then\
		helmfile -i -e $(env) template;\
	else\
		helmfile -i -e $(env) -l name=$(name) template;\
	fi

config:
	python3 scripts/render_config.py

update: config
	time helmfile deps

clean:
	rm -rf rendered/*