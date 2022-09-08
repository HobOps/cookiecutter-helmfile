# cookiecutter-helmfile

Cookiecutter template for managing Kubernetes environments with Helmfile [HobOps](https://github.com/helmfile/helmfile)

## Getting Started

### Clone repository
```
cookiecutter https://github.com/HobOps/cookiecutter-helmfile.git
```

### Install dependencies
- [SOPS](https://github.com/mozilla/sops)
- Python3
  - pyyaml
- [helm](https://github.com/helm/helm/releases)
  - plugins
    - [diff](https://github.com/databus23/helm-diff)
      - ```helm plugin install https://github.com/databus23/helm-diff```
    - [secrets](https://github.com/jkroepke/helm-secrets)
      - ```helm plugin install https://github.com/jkroepke/helm-secrets```
- [helmfile](https://github.com/helmfile/helmfile#installation)
### Setup helmfile
- Configure [.sops.yaml](.sops.yaml) file following the [official documentation](https://github.com/mozilla/sops)
- Customize helmfile releases in [settings.yaml](include/settings.yaml)
- Add clusters to [clusters/index.yaml](clusters/index.yaml)
- Add environments to [environments/index.yaml](environments/index.yaml)

### Install dependencies
```
pip3 install -r scripts/requirements.txt
```

### Render and update helmfile release file
```
make update
```

### Install infrastructure charts to cluster
```
make cluster_apply cluster={{cookiecutter.initial_cluster_name}}
```

### Install environment
```
make apply env={{cookiecutter.initial_environment_name}}
```