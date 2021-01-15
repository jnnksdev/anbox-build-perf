# Integrating Docker external BackEnd for Anbox Docker Image Build

import subprocess
import time 

def run(cmd: str, dir = None):
    """run a command in shell after cd to dir"""
    if dir is not None:
        cmd = f"cd {dir} && {cmd}"
    
    
    #print(cmd + "\n")
    comp_proc = subprocess.run(cmd,
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)

    return comp_proc.returncode


def remove_anbox_image():
    """"remove anbox docker image"""
    cmd = f"docker images anbox/anbox-build --format={{{{.ID}}}}"
    #print(cmd)

    stdout_content = subprocess.check_output(cmd, shell=True)
    anbox_image_id = stdout_content.decode('ascii').strip()

    if len(anbox_image_id) > 0:
        run(f"docker rmi {anbox_image_id}")

master = []
external = []

import os
pwd = os.path.dirname(os.path.abspath(__file__))

MAX = 10
for i in range(MAX):
    print(f"---- RUN {i + 1} / {MAX}")


    run(f"rm -fr build", dir=f"{pwd}/anbox-master")
    remove_anbox_image()
    
    # master measurement
    start = time.time()
    docker_code = run(f"DOCKER_BUILDKIT=1 docker build --no-cache --tag=anbox/anbox-build .", dir=f"{pwd}/anbox-master")
    master_docker = time.time() - start
    start = time.time()
    anbox_code = run(f"docker run --rm --volume=$PWD:/anbox --user=$(id -u):$(id -g) anbox/anbox-build bash -c \"cmake -B/anbox/build && make --jobs=8 --directory=/anbox/build\"", 
        dir=f"{pwd}/anbox-master")
    master_anbox = time.time() - start
    
    master.append((master_docker, master_anbox, docker_code, anbox_code))

    if (docker_code + anbox_code) > 0:
        print(f"external failed: {docker_code} {anbox_code}")


    run(f"rm -fr build", dir=f"{pwd}/anbox-external-cpu-features")
    remove_anbox_image()

    # external measurement
    start = time.time()
    docker_code = run(f"DOCKER_BUILDKIT=1 docker build --no-cache --tag=anbox/anbox-build .", dir=f"{pwd}/anbox-external-cpu-features")
    external_docker = time.time() - start
    start = time.time()
    anbox_code = run(f"docker run --rm --volume=$PWD:/anbox --user=$(id -u):$(id -g) anbox/anbox-build bash -c \"cmake -B/anbox/build && make --jobs=8 --directory=/anbox/build\"", 
        dir=f"{pwd}/anbox-external-cpu-features")
    external_anbox = time.time() - start
                
    external.append((external_docker, external_anbox, docker_code, anbox_code))

    if (docker_code + anbox_code) > 0:
        print(f"external failed: {docker_code} {anbox_code}")


        
    print(f"external - master: {(int(round(1000*(external_docker - master_docker))), int(round(1000*(external_anbox - master_anbox))))}")

print(f"master: {master}")
print(f"external: {external}")

# write to file
with open(f"{pwd}/result.json", "w+") as f:
    import json
    json.dump({
        "master": master,
        "external": external
    }, f)
