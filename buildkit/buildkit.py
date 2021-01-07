# Integrating Docker BuildKit BackEnd for Anbox Docker Image Build

import subprocess
import time 

def remove_anbox_image():
    """"remove anbox docker image"""
    cmd = f"docker images anbox/anbox-build --format={{{{.ID}}}}"
    #print(cmd)

    stdout_content = subprocess.check_output(cmd, shell=True)
    anbox_image_id = stdout_content.decode('ascii').strip()

    if len(anbox_image_id) > 0:
        cmd = f"docker rmi {anbox_image_id}"
        #print(cmd)
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

def run(cmd: str, dir = "/home/jannik/Workspace/anbox-work/anbox"):
    """run a command in shell after cd to dir"""
    cmd = f"cd {dir} && {cmd}"
    #print(cmd)
    subprocess.run(cmd,
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)


master = []
buildkit = []

MAX = 1
for i in range(MAX):
    print(f"---- RUN {i + 1} / {MAX}")

    remove_anbox_image()
    time.sleep(5)
    

    # master measurement
    start = time.time()
    run(f"docker build --no-cache --tag=anbox/anbox-build .")
    master_duration = time.time() - start
    
    master.append(master_duration)


    remove_anbox_image()
    time.sleep(5)


    # buildkit measurement
    start = time.time()
    run(f"DOCKER_BUILDKIT=1 docker build --no-cache --tag=anbox/anbox-build .")
    buildkit_duration = time.time() - start
                
    buildkit.append(buildkit_duration)
    

    print(f"buildkit - master: {buildkit_duration - master_duration}")

print(f"master: {master}")
print(f"master: {buildkit}")

# write to file
import os
pwd = os.path.dirname(os.path.abspath(__file__))
with open(f"{pwd}/result.json", "w+") as f:
    import json
    json.dump({
        "master": master,
        "buildkit": buildkit
    }, f)