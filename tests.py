import configparser, time
import json
from distutils.version import LooseVersion

import sys


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "font", "Courier")
    config.set("Settings", "font_size", "10")
    config.set("Settings", "font_style", "Normal")
    config.set("Settings", "font_info",
               "You are using %(font)s at %(font_size)s pt")

    with open(path, "a") as config_file:
        config.write(config_file)

def createjson(path):

    section0 = {"Name": "Check the system data",
    "Ver": "6.7",
    "Command": "uname -a",
    "Instruction": """
global var
global res
var = var.split(" ")
print(var)
    """,
    "Alert": "Alerted",
    "Parent": "var1"
    }
    section1 = {"Name": "Named1",
    "Command": "commanded",
    "Action": ["Action1", "Action2"],
    "Alert": "Alerted"
    }
    section1["another"] = section0
    section1["another"]['Command']={"name":"gure"}
    jsontouple = section1


    print(jsontouple['another']['Command'])
    #jsontouple["another"] = {"sig":1}

    jsonfile = open(path, mode="w", encoding="utf-8")
    json.dump(jsontouple, jsonfile, sort_keys=True, indent=4)
    jsonfile.close()


def parsJson(path):
    file = open(path, mode="r", encoding='utf-8')
    data = json.load(file)
    #print(data["Alert"])
    for sections in data:
        print("----------------AA--------------------")
        print(str(sections))
        #print(str(sections.values()))

        print("length of section", str(sections), "is: ", len(sections))
        for parameter in sections:
            print("------------BB----------------")
            print(str(sections[parameter]))
            print("length os", str(parameter),  "is: ", len(sections[parameter]))
    file.close()

def executor():
    global var
    var = "VMkernel esxi 6.7.0 #1 SMP Release build-8169922 Apr  3 2018 14:48:22 x86_64 x86_64 x86_64 ESXi"
    command = """
    var1 = "ziga zaga"
    var1 = var1.split(" ")
    print(var1)
    """
    command = """
global var
var=var.split(" ")
print(var)
"""
    exec(command)
    #print(var)
    #command = """
    #var.spliit
    #"""


if __name__ == "__main__":
    path = "settings1.json"
    #createConfig(path)
    createjson(path)
    #parsJson(path)
    print(time.ctime(time.time()))
    #executor()
    #jcob={'Nma':'zuba'}
    #jcob.setdefault('addres', {})
    #jcob['addres'].setdefault('Nma',{})
    #jcob['addres']['Nma'].setdefault('zzma',{})
    #jcob['addres']['shmaddress']={'buuble':'mubble'}
    #print(jcob)
    #jReport={}
    #jReport.setdefault('esxi', {})
    #com = "jReport['esxi'].setdefault('big', {})"
    #exec(com)
    #print(jReport
    # )
    """
    oParent = ['good', 'bad', 'normal']
    jReport = {"Name":'goot'}
    for item in oParent:
        jReport[item]={}
        temp = temp
    """
    items = ['good', 'bad', 'normal']

    struct = {}
    temp = struct
    for item in items:
        if item not in temp:
            temp[item] = {}
        temp = temp[item]
    print(temp)
    print(struct)