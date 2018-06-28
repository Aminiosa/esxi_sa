import paramiko
import json
import time
import sys
import argparse
import os
import subprocess

from distutils.version import LooseVersion




def executor(execmd):
    stdin, stdout, stderr = client.exec_command(str(execmd))
    data = stdout.read() + stderr.read()
    return(data.decode('utf-8'))

def jParser(path):
    global var, version, sName, jReport
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
                exec(data[test]['Instruction'])
            except:
                print("Can't execute the instructions, check it")
                continue
            curPath = []
            curPath.append(sName)
            if data[test]['Parent'] != 'NULL':
                curPath.extend(data[test]['Parent'].split(','))

            if data[test]['Condition'] != "NULL":
                exec(data[test]['Condition'])

            jCreator(curPath, data[test]['Name'], var)
            print("...done.")

        if data[test]['type'] == "psh":
            pshsc = pshsc + "\necho \"<id:" + data[test]['id'] + ">\"\n" + '\n'.join(data[test]['Command']) + "\necho \"</id:" + data[test]['id'] + ">\""
            ids.append(data[test]['id'])


    pshsc = pshsc +"""\nDisconnect-VIServer $args[0] -confirm:$false
$WarningPreference = $oldWarningPreference"""
    #print(pshsc)
    with open(argas['ptps'], 'w', encoding='utf-8') as g:
        g.write(pshsc)
    g.close()
    alpha="powershell.exe -File powershell.ps1 " + argas['server'] + " " + argas['user'] + " " + argas['password'] \
          + " \"" + os.getcwd() + "\" > tempdat.txt"
    print("Gathering security configuration")
    os.system(alpha)
    tmpfile = open(rPath, 'r', encoding='utf-8')
    #for item in ids:
     #   temp = cutId(tmpfile, item)

    #print(ids)
    file.close()

def cutId(file, id):

        while file.readline() != ("<id: " + id + ">"):
            continue
      #  while


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


    Then the PowerCLI module should be installed into PowerShell:\n
       PS> Install-Module -Name VMware.PowerCLI\n
       PS> set-executionpolicy remotesigned
    """)
    parent_parser.add_argument('--user', action="store", default='root', help='ESXi user login. Default "root"')
    parent_parser.add_argument('--password', action="store", help='ESXi user\'s password')
    parent_parser.add_argument('--server', action="store", help="Server address or host")
    parent_parser.add_argument('--pcliport', action="store", default="443", help="PowerCLI port, 443 by default")
    parent_parser.add_argument('--sshport', action="store", default='22', help="SSH port, 22 by default")
    parent_parser.add_argument('--ptph', action="store", default='pwsh-preview', help="Path to power shell core, 'pwsh-preview' by default ")
    parent_parser.add_argument('--ptinv', action="store", default='inventory.json', help="Path to inventory rules fille, 'inventory.json' by default ")
    parent_parser.add_argument('--ptps', action="store", default='powershell.ps1', help="Path to pwershell script, 'powershell.ps1' by default")
    parent_parser.add_argument('--ptrep', action="store", default='report.json', help="Path to report, 'report.json' by default")
    argas = vars(parent_parser.parse_args())

    host = argas['server']
    user = argas['user']
    secret = argas['password']
    print("Connecting to :", host)
    port = argas['sshport']

    global sName, version, rPath, flagFirstIteration, jReport, ids
    ids=[]
    flagFirstIteration = 0
    version = " "
    jReport = {"ReportDate": time.ctime(time.time())}
    rPath = argas['ptrep'] #path to report
    invCfgFile = argas['ptinv'] #inventory file

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=secret, port=port)
    except:
        print("Error during connection to server")
        client.close()
        exit(1)


    jParser(invCfgFile)
    pathToTemp = os.getcwd()+'\\'+"temp.dat"
    with open(rPath, 'w', encoding='utf-8') as g:
        json.dump(jReport, g, sort_keys=True, indent=4)
    g.close()
    print("Script executed fully. Perhaps no errors.")
    client.close()
    exit(0)