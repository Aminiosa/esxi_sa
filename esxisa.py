import paramiko
import json
import time
import sys
import argparse
import os
import subprocess

from distutils.version import LooseVersion

def pshResParser(text, mainpar = None):
    text = list(filter(None, text.split('\n\n')))
    devisions = {}
    tempStore = None
    sklad = {}
    for i in range(0, len(text)):
        text[i]=list(filter(None, text[i].split('\n')))
        if len(text[i])>1:
            for j in range(0, len(text[i])):
                text[i][j]=list(filter(None, text[i][j].split(':')))
                if len(text[i][j])>1:
                    for k in range(0, len(text[i][j])):
                        text[i][j][k] = text[i][j][k].lstrip()
                        text[i][j][k] = text[i][j][k].rstrip()
            for j in range(0, len(text[i])):
                if mainpar != None:
                    if text[i][j][0] == mainpar and text[i][j][1] not in sklad.keys():
                        sklad[text[i][j][1]] = []
                        sklad[text[i][j][1]].append(text[i][j+1][1])
                    else:
                        if text[i][j][0] == mainpar and text[i][j][1] in sklad.keys():
                            sklad[text[i][j][1]].append(text[i][j + 1][1])
                else:
                    sklad[text[i][j][0]] = text[i][j][1]

        else:
            if tempStore == None:
                tempStore = (text[i][0])
            else:
                devisions[tempStore] = sklad
                tempStore = (text[i][0])
                sklad = {}
                devisions[tempStore] = sklad

    slist = []
    sdict = {}

    return devisions


def executor(execmd):
    stdin, stdout, stderr = client.exec_command(str(execmd))
    data = stdout.read() + stderr.read()
    return(data.decode('utf-8'))

def jParser(path, compPath):
    global var, version, sName, jReport, TOF
    flagIsAlerts = 0
    pshsc = """$oldWarningPreference = $WarningPreference
$WarningPreference = 'SilentlyContinue'
cd $args[3]
Connect-VIServer $args[0] -user $args[1] -password $args[2]"""
    try:
        file = open(path, mode="r", encoding='utf-8')
    except:
        print("Can't open file")
        return
    data = json.load(file)
    file.close()
    try:
        file = open(compPath, mode="r", encoding='utf-8')
    except:
        print("Can't open file")
        return
    data1=json.load(file)
    data = {**data, **data1}
    #print(data)
    file.close()
    sid=0
    for test in data:

        if (version != " "):
            if (LooseVersion(version) > LooseVersion(data[test]['VerM'])) and (LooseVersion(version) < LooseVersion(data[test]['Ver'])):
                print("That scrip is't capable with this version. Server version:", version,
                      ", script for:", data[test]['Ver'], "to", data[test]['VerM'])
                continue

        if data[test]['type'] == "ssh":
            try:
                print("#Operation: ", data[test]['Msg'])
                var = executor(data[test]['Command'])
            except:
                print("Error while send query to ESXi server")
                continue

            try:
                exec("\nglobal var\n"+data[test]['Instruction'])
            except:
                print("Can't execute the instructions, check it")
                continue
            curPath = []
            curPath.append(sName)
            if data[test]['Parent'] != 'NULL' and data[test]['Parent'] != '':
                curPath.extend(data[test]['Parent'].split(','))

            if data[test]['Condition'] != "NULL" and data[test]['Condition'] != "":
                TOF = True
                try:
                    exec("global TOF\n" + data[test]['Condition'])
                except:
                    print("Cannot execute Condition")
                if TOF is False:
                    flagIsAlerts = flagIsAlerts + 1
                    alerts.append(data[test]["Alert"])
            jCreator(curPath, data[test]['Name'], var)
            print("...done.")

        if data[test]['type'] == "psh":
            if type(data[test]['Command']) is list:
                pshsc = pshsc + "\necho \"<id:" + test + ">\"\n" + '\n'.join(
                    data[test]['Command']) + "\necho \"</id:" + test + ">\""
                ids.append(test)
                continue
            if type(data[test]['Command']) is str:
                pshsc = pshsc + "\necho \"<id:" + test + ">\"\n" + data[test]['Command'] + "\necho \"</id:" + test + ">\""
                ids.append(test)
                continue
            print("cannot recognize the command")

    pshsc = pshsc +"""\nDisconnect-VIServer $args[0] -confirm:$false
$WarningPreference = $oldWarningPreference"""
    with open(argas['ptps'], 'w', encoding='utf-8') as g:
        g.write(pshsc)
    g.close()
    alpha = argas['ptph'] + " -File powershell.ps1 " + argas['server'] + " " + argas['user'] + " " + argas['password'] \
          + " \"" + os.getcwd() + "\" > tempdat.txt"
    print("Gathering security configuration")
    try:
        os.system(alpha)
    except:
        print("Powershell interpreter not found. Interrupt")
        client.close()
        exit()
    try:
       tmpfile = open("tempdat.txt", 'r', encoding='utf-8')
    except:
        print("Some troubles with Powershell. Interrupt")
        client.close()
        exit()
    global pshData

    print("ids:", ids)

    for item in ids:
        print("Now exec operation is:", item)
        pshData = cutId(tmpfile, item)
        if data[item]['Instruction'] != "NULL":
            try:
                exec("global pshData\n" + data[item]['Instruction'])
            except:
                print("Can not execute instruction. Operation ID:", item)
                continue
        curPath = []
        curPath.append(sName)
        if data[item]['Parent'] != 'NULL':
            curPath.extend(data[item]['Parent'].split(','))
        jCreator(curPath, data[item]['Name'], pshData)
        if ((data[item]['Condition'] != "NULL") and (data[item]['Condition'] != "")):
                TOF = True
                try:
                    exec("global TOF\n"+data[item]['Condition'])
                except:
                    print("Can not execute Condition. Operation ID:", item)
                    continue
                if TOF is False:
                    flagIsAlerts = flagIsAlerts + 1
                    alerts.append(data[item]["Alert"])
    tmpfile.close()
    if flagIsAlerts > 0:
        print("There are", flagIsAlerts, "alerts! Please check the !!ALERTS.txt file!")
    #print(ids)

def cutId(files, id):
        res = ""
        files.seek(0)
        tmpitm = files.readline()
        while tmpitm != ("<id:" + id + ">\n") and tmpitm:
            tmpitm = files.readline()
        tmpitm = files.readline()
        if not tmpitm:
            print("Cannot find appropriate data")
            return None
        while tmpitm != ("</id:" + id + ">\n") and tmpitm:
            res = res + tmpitm
            tmpitm = files.readline()
        return res


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
    parent_parser = argparse.ArgumentParser(description="""ESXi security audit and inventory
    For fully functional PowerShell is required. For install:\n
       curl  https://packages.microsoft.com/keys/microsoft.asc > MS.key &&
       apt-key add MS.key &&
       curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | sudo tee /etc/apt/sources.list.d/microsoft.list &&
       sudo apt-get update &&
       sudo apt-get install  -y powershell \n\n\t
       
       Also you can install Powershell core with snap: snap install powershell --classic


    Then the PowerCLI module should be installed into PowerShell:\n
       PS> Install-Module -Name VMware.PowerCLI\n
       PS> set-executionpolicy remotesigned #For Windows
       PS> Set-PowerCLIConfiguration -Scope User -InvalidCertificateAction Ignore
    """)
    parent_parser.add_argument('--user', action="store", default='root', help='ESXi user login. Default "root"')
    parent_parser.add_argument('--password', action="store", help='ESXi user\'s password')
    parent_parser.add_argument('--server', action="store", help="Server address or host")
    parent_parser.add_argument('--pcliport', action="store", default="443", help="PowerCLI port, 443 by default")
    parent_parser.add_argument('--sshport', action="store", default='22', help="SSH port, 22 by default")
    parent_parser.add_argument('--ptph', action="store", default='pwsh', help="Path to power shell core, 'pwsh-preview' by default ")
    parent_parser.add_argument('--ptinv', action="store", default='inventory.json', help="Path to inventory rules fille, 'inventory.json' by default ")
    parent_parser.add_argument('--ptps', action="store", default='powershell.ps1', help="Path to pwershell script, 'powershell.ps1' by default")
    parent_parser.add_argument('--ptrep', action="store", default='report.json', help="Path to report, 'report.json' by default")
    parent_parser.add_argument('--compp', action="store", default='compliance.json',
                               help="Path to compliance config file, 'compliance.json' by default")
    argas = vars(parent_parser.parse_args())

    host = argas['server']
    user = argas['user']
    secret = argas['password']
    print("Connecting to :", host)
    port = argas['sshport']

    global sName, version, rPath, flagFirstIteration, jReport, ids, alerts
    alerts = []
    ids=[]
    flagFirstIteration = 0
    version = " "
    jReport = {"ReportDate": time.ctime(time.time())}
    rPath = argas['ptrep'] #path to report
    invCfgFile = argas['ptinv'] #inventory file
    compPath = argas['compp']
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=secret, port=port)
    except:
        print("Error during connection to server")
        client.close()
        exit(1)


    jParser(invCfgFile, compPath)
    pathToTemp = os.getcwd()+'\\'+"temp.dat"
    with open(rPath, 'w', encoding='utf-8') as g:
        json.dump(jReport, g, sort_keys=True, indent=4)
    g.close()
    with open("!!ALERTS.txt", 'w', encoding='utf-8') as g:
        g.write('\n'.join(alerts))
    g.close()
    print("Script executed fully. Perhaps no errors.")
    client.close()

    exit(0)