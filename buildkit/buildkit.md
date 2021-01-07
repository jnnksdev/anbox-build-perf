Pull Request:
Status: 

# Docker BuildKit
Docker v18.09+ includes a newer backend for Linux containers called *BuildKit*. It can be enabled via a simple environment variable.

The simple change comes in with an improvement of 2.6 seconds (3%) for the image build time:

|   job    |   time  | command line |
| -------- | ------- | ------------ |
| master   |  79.95s | `docker build --no-cache --tag=anbox/anbox-build .` | 
| buildkit |  77.35s | `DOCKER_BUILDKIT=1 docker build --no-cache --tag=anbox/anbox-build .` | 