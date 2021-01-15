
import os
pwd = os.path.dirname(os.path.abspath(__file__))

test = [[1, 2], [3, 4], [5, 6]]

test2 = list(map(list, zip(*test)))    
print(test2)


result = None
path = f"{pwd}/result.json"
print(path)
with open(path, "r") as f:
    import json
    result = json.load(f)

aggregate = {}
for key in result:
    aggregate[key] = {}


for key in result:
    times = list(map(list, zip(*(result[key]))))
    
    docker_times = times[0]
    print(key)
    avg_docker = int(round(1000 * sum(docker_times) / len(docker_times)))
    aggregate[key]["docker"] = avg_docker
    

    anbox_times = times[1]
    avg_anbox = int(round(1000 * sum(anbox_times) / len(anbox_times)))
    aggregate[key]["anbox"] = avg_anbox

    print(f"avg docker: {avg_docker}")
    print(f"avg anbox: {avg_anbox}")
    

print(f"docker: external - master = {aggregate['external']['docker'] - aggregate['master']['docker']}")
print(f"anbox: external - master = {aggregate['external']['anbox'] - aggregate['master']['anbox']}")