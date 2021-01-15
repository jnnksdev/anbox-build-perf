# Static Compilation of cpu_features Library
By statically providing the library functionatlity during the Docker image build process, the dependecy can be removed from the build process.

Instead of building the library with Anbox, it is present in the build environment. This would require the compilation and deployment of the library for all build environments, which introduces complexity for non-docker users.

The change brings benefits for developers only after compiling Anbox for five times and is therefore rather insignificant.
|job         |master |external|
|--          |--     |--      |
|docker build|77.91s |79.20s  | 
|anbox build |64.37s |64.05s  |
|            |       |        |
| **total**  |142.28s|143.25s |


## Versions
modified: 
```sh
git clone -b external-cpu-features git@github.com:jnnksdev/anbox anbox-external-cpu-features
cd anbox-external-cpu-features
git reset --hard 1a936f1deae2e3472ae75b04f273c165fc58f833

git clone -b master git@github.com:jnnksdev/anbox anbox-master
cd anbox-master
git reset --hard 6c10125a7f13908d2cbe56d2d9ab09872755f265
```