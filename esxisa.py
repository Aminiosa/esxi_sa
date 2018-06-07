import sys
import paramiko
import json
import time

from distutils.version import LooseVersion

def executor(execmd):
    stdin, stdout, stderr = client.exec_command(str(execmd))
    data = stdout.read() + stderr.read()
    return(data.decode('utf-8'))

def jParser(path):
    global var, version, sName, jReport
    try:
        file = open(path, mode="r", encoding='utf-8')
    except:
        print("Can't open file")
        return
    data = json.load(file)
    for test in data:

        if (version != " "):
            if (LooseVersion(version) > LooseVersion(test['VerM'])) and (LooseVersion(version) < LooseVersion(test['Ver'])):
                print("That scrip is't capable with this version. Server version:", version,
                      ", script for:", test['Ver'], "to", test['VerM'])
                continue

        try:
            print("#Operation: ", test['Msg'])
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
        if test['Condition'] != "NULL":
            exec(test['Condition'])
        jCreator(curPath, test['Name'], var)
        print("...done.")

def jCreator(oParent, oName, oData):
    global jReport
    temp = jReport
    for item in oParent:
            if item not in temp:
                temp[item] = {}
            temp = temp[item]
            if item == oParent[-1]:
                temp[oName] = oData

if __name__ == "__main__":
    print("enter the password:")

    host = '188.130.155.61'
    user = 'root'
    secret = 'DataStore1234'#input()
    print("Your password:", secret)
    port = 22

    global sName, version, rPath, flagFirstIteration, jReport
    flagFirstIteration = 0
    version = " "
    jReport = {"ReportDate": time.ctime(time.time())}
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

    with open(rPath, 'w', encoding='utf-8') as g:
        json.dump(jReport, g, sort_keys=True, indent=4)

    print("Script executed fully. Perhaps no errors.")
    client.close()
    exit(0)