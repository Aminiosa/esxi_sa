import configparser
import json
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

    with open(path, "w") as config_file:
        config.write(config_file)

def createjson(path):
    section0 = {"Name": "Check the system data",
    "Command": "uname -a",
    "Action": """""",
    "Alert": "Alerted"
    }
    section1 = {"Name": "Named1",
    "Command": "commanded",
    "Action": ["Action1", "Action2"],
    "Alert": "Alerted"
    }
    jsontouple = []
    jsontouple.append(section0)
    jsontouple.append(section1)

    jsonfile = open(path, mode="w", encoding="utf-8")
    json.dump(jsontouple, jsonfile)
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
    path = "settings.json"
    #createConfig(path)
    #createjson(path)
    #parsJson(path)
    executor()