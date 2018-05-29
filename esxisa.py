import sys
import paramiko

print("enter the password:")

host = '188.130.155.61'
user = 'root'
secret = input()
print("Your password:", secret)
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=port)
stdin, stdout, stderr = client.exec_command('uname -a')
data = stdout.read() + stderr.read()
print(data.decode('utf-8'))
client.close()