import sys
import paramiko
import configparser

def executor(execmd):
    stdin, stdout, stderr = client.exec_command(str(execmd))
    data = stdout.read() + stderr.read()
    return(data.decode('utf-8'))


print("enter the password:")

host = '188.130.155.61'
user = 'root'
secret = 'DataStore1234'#input()
print("Your password:", secret)
port = 22
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
except:
    print("Error during connection to server")
    client.close()
    exit(1)
mean = executor("uname -a")
mean = mean.split("/t")
print(executor("chkconfig -l"))

print("Script executed fully. Perhaps no errors.")
client.close()
exit(0)