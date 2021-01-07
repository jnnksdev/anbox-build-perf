As a maintainer and developer I want Anbox build time to be quicker to improve the development workflow and to see results faster. This is  especially relevant for rebuilds with small changes.

This issue will be a report style based work log with a set of experiments and implementations for each topic.

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

----------




-----






### Notes
* process-cpp can be built standalone, but needs `set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++14")` in CMakeLists.txt
    * otherwise `namespace linux` will be marked with an error `expected identifier before numeric constant` or `expected unqualified-id before numeric constant`
    * more info: [Build error when set (CMAKE_CXX_STANDARD 11)](https://github.com/cinder/Cinder/issues/2108)



* none of the following packages are required to build anbox: `ca-certificates` `cmake-data` `cmake-extras` `debhelper` `dbus` `git` 