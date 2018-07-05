pshData = """
Name            : 188.130.155.61
AcceptanceLevel : PartnerSupported

"""
#global pshData
var = ''
pshData = list(filter(None, pshData.split("\n")))
for iter in pshData[1:]:
    iter = iter.split(':')
    var = iter[1].lstrip()
pshData = var+'1'
print(pshData)
alerts = []

if pshData != "PartnerSupported":\n alerts.append("""----------->>>
Community Supported VIBs are not supported and do not have a digital signature. To
protect the security and integrity of your ESXi hosts do not allow unsigned
(CommunitySupported) VIBs to be installed on your hosts.
Recommendations:
Foreach ($VMHost in Get-VMHost ) {
$ESXCli = Get-EsxCli -VMHost $VMHost
$ESXCli.software.acceptance.Set("PartnerSupported")
}
    """)
print(alerts)