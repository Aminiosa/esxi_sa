var = ["root:Administrator","daemon:System daemons",
            "nfsnobody5534:Anonymous NFS User",
            "dcui00:DCUI User",
            "vpxuser00:VMware VirtualCenter administration account",
            "nmokh000:Administrator", ""]
var.remove("")
temp = {}
for item in var:
    item = item.split(':')
    temp[item[0]]=item[1]
print(temp)
var = temp
print(var)