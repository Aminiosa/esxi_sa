var = """Switch Name:Num Ports:Used Ports:Configured Ports:MTU:Uplinks:
vSwitch0:2560:5:128:1500:vmnic0:
vSwitch1:6666:8:129:2500:vmnic1:
"""
var = var.split('\n')
del var[-1]
var = [i.split(':') for i in var]
temp = {}
for item in var[1:]:
 temp[item[0]]={}
 for i in range(6):
  temp[item[0]][var[0][i]] = item[i]
var = temp
print(var)
