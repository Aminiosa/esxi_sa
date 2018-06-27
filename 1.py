# -*- coding: iso-8859-1 -*-
import subprocess
import shlex
import sys
import argparse, os, subprocess

parent_parser = argparse.ArgumentParser(description="""ESXi security audit and inventory
For fully functional PowerShell is required. For install:\n
   curl  https://packages.microsoft.com/keys/microsoft.asc > MS.key &&
   apt-key add MS.key &&
   curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | sudo tee /etc/apt/sources.list.d/microsoft.list &&
   sudo apt-get update &&
   sudo apt-get install  -y powershell\n\n\t
   
   
Then the PowerCLI module should be installed into PowerShell:\n
   PS> Install-Module -Name VMware.PowerCLI\n
""")
parent_parser.add_argument('--user', action="store", default='root', help='ESXi user login. Default "root"')
parent_parser.add_argument('--password', action="store", help='ESXi user\'s password', default="DataStore1234")
parent_parser.add_argument('--server', action="store", help="Server address or host", default="188.130.155.61")
parent_parser.add_argument('--pcliport', action="store", default="443", help="PowerCLI port, 443 by default")
parent_parser.add_argument('--sshport', action="store", default='22', help="SSH port, 22 by default")
argas = vars(parent_parser.parse_args())
user = argas['user']
print(os.getcwd())
alpha = "powershell.exe -File powershell.ps1 " + argas['server'] + " " + argas['user'] + " " + argas['password'] + " \"" + os.getcwd()+"\" > tempdat.txt"
print(alpha)
#os.system(alpha)
#cmd = alpha
#args = shlex.split(alpha)

proc = subprocess.Popen(alpha , shell=True, stdout=subprocess.PIPE)
out = proc.stdout.readlines()
alpha = "powershell.exe -File powershell.ps1 " + argas['server'] + " " + argas['user'] + " " + argas['password'] + " \"" + os.getcwd()+"\" > tempdat.txt"
#os.system(alpha)
