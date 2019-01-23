import json
from pprint import pprint



def getcve(key):
   with open('CVE.json') as f:
     data = json.load(f)
   return(data[key])
print("Enter ESXi version (5.5/6.0/6.5)")
version=input()
pprint(getcve(version))

