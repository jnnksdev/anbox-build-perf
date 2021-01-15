As a maintainer and developer I want Anbox build time to be quicker to improve the development workflow and to see results faster. This is  especially relevant for rebuilds with small changes.

This repository will be a report style based work log with a set of experiments and implementations for each topic.

Feedback and suggestions are always welcome.

&nbsp;
## Current Situation
The preffered build method is the docker container and the image build time as well as Anbox build times are captured to begin with. Even though most of the time the image needs to be built only once, it is still relevant for CI/CD.

|   job  |  time  | command line |
| ------ | ------ | ------------ |
| docker |  82s | `docker build --no-cache --tag=anbox/anbox-build .` |  
| anbox  |  64s | `docker run --rm --volume=${PWD}:/anbox --user=$(id -u):$(id -g) anbox/anbox-build bash -c "cmake -B/anbox/build && make --jobs=8 --directory=/anbox/build"` |

These times are rounded to single seconds and should give a rough impression on the distribution.
For each experiment a separate set of measurements will be conducted which will be used as base for comparsions.

### Procedure
Docker image build times were measured in disregard of Dockers caching functionality to simulate a clean work environment with no prior image builds. Similar to that the build directory was removed after each Anbox build to ensure a build from scratch.

Each command was executed ten times to ensure an average value and to avoid spontaneous outliers.\ 
The build machine is a high end workstation.


&nbsp;
## Plans and Ideas

Optimizing the build environment and cmake configurations will be the first step to implement improvements.
Some functionality included in the build process can be compiled during the container creation for example.
Docker optimization with multi-staged builds could introduce a great reduction in image build time as well.\ 
No changes to the code base are made and the optimized build should result in the same binaries.

C++20 introduced modules which act as packages and can be used to shorted build times by providing stricter inter package interfaces. By reducing the cross module references responsibilities will be more granular, but also more separatable which allows for greater distiction between components that need to be rebuilt and some that do not.  
These changes might introduce differences in the build artifacts and might split the final binary into multiple libraries.


# Static Compilation of Dependencies and External Libraries
By statically providing library functionatlity during the Docker image build process, the dependecy can be ignored during Anbox build, since it is already compiled and usable.This would require the compilation and deployment of the library for all build environments, which introduces complexity for non-docker users.

Furthermore the value of providing libraries statically is propertional on the level of dependency, or rather how deep the dependency is integrated into Anbox. Theoretical performance improvements may be overshadowed by multitasking build systems being able to compile multiple parts of the program simultaneously.
When compiling a lbrary by itself the build time may be ten seconds. Anbox build time may be reduced by ten seconds as well, as long as it is a necessary step before anything else can be compiled. This would for example be the case for the C++ standard library, as it is used across almost all source files and a universal dependecy.
In most cases though the dependecy is used in a small subsection of the project as for example GoogleTest and GoogleMock wich are only used during unit testing or process-cpp which is exclusively used in the command line interface.
With CMake and Make able to parallelize the workload the build time reduction may not be as linear as expected.

## Static Compilation of cpu_features
Providing the dependency *cpu_features* as precompiled library for each build reduced the full-build-time by only about 300ms, but increased the docker image build time by about 1.3 seconds.