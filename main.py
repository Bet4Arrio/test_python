import requests
import json
from dataclasses import dataclass, asdict
import sys


@dataclass
class Packge:
    name:str
    current_version:str
    latest_version: str
    out_of_date:bool


def get_latest(packge_name:str) -> str:
    uri = f'https://pypi.org/pypi/{packge_name}/json'
    r = requests.get(uri)
    if r.status_code != requests.codes.ok:
        return None

    json = r.json()
    version = list(json['releases'])[-1]
    return version

def compare_versions(packge:Packge)->bool:
    return packge.current_version != packge.latest_version


def create_packge(packge_data:str)->Packge:
    if packge_data == "" or not ( "=" in packge_data):
        return None

    name, v = [x for x in  packge_data.split("=") if x != ""]
    name = name.replace(">", "").replace("<", "")
    last_version = get_latest(name)
    pkg = Packge(name, v, last_version, True)
    pkg.out_of_date = compare_versions(pkg)
    return pkg



def get_packges(target)->list:
    packges = []
    with open(target) as reqs:
        for line in reqs:
            name = line.rstrip()
            pkg =  create_packge(name)
            if pkg != None:
                packges.append(pkg)
    return packges

def main():
    if len(sys.argv) >= 2:
        target = sys.argv[1]
    else:
        target = input("caminho para o arquivo requirements.txt ou enter se estiver na raiz: ")
        target = target if target != '' else 'requirements.txt'

    packges = json.dumps([asdict(x) for x in get_packges(target)])
    if len(sys.argv) >= 3:
        file = sys.argv[2] if ".json" in sys.argv[2][-5:] else sys.argv[2]+".json"
        with open(file, 'w') as f:
            json.dump(packges, f)
    else:
        print(packges)
    
if __name__ == "__main__":
    main()


