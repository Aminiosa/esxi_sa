import sys
import paramiko
import configparser
import json
from distutils.version import LooseVersion

def executor(execmd):
    stdin, stdout, stderr = client.exec_command(str(execmd))
    data = stdout.read() + stderr.read()
    return(data.decode('utf-8'))

def jParser(path):
    global var, version, sName, rPath
    try:
        file = open(path, mode="r", encoding='utf-8')
    except:
        print("Can't open file")
        return
    data = json.load(file)
    for test in data:

        if (version != " "):
            if (LooseVersion(version) < LooseVersion(test['Ver'])):
                print("That scrip is't capable with this version. Server version:", version, ", script:", test['Ver'])
                continue

        try:
            print("#Operation: ", test['Name'])
            var = executor(test['Command'])
        except:
            print("Error while send query to ESXi server")
            continue

        try:
            exec(test['Instruction'])
        except:
            print("Can't execute the instructions")
            continue
        curPath = []
        curPath.append(sName)
        if test['Parent'] != 'NULL':
            curPath.extend(test['Parent'].split(','))
        print(curPath)
        jCreator(rPath, curPath, test['Name'], var)

def jCreator(rPath, oParent, oName, oData):
    print(rPath, oParent, oName, oData)

if __name__ == "__main__":
    print("enter the password:")

    host = '188.130.155.61'
    user = 'root'
    secret = 'DataStore1234'#input()
    print("Your password:", secret)
    port = 22

    global sName, version, rPath, flagFirstIteration
    flagFirstIteration = 0
    version = " "
    rPath='report.json' #path to report
    invCfgFile = 'inventory.json' #inventory file

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=secret, port=port)
    except:
        print("Error during connection to server")
        client.close()
        exit(1)


    jParser(invCfgFile)
    print("Script executed fully. Perhaps no errors.")
    client.close()
    exit(0)