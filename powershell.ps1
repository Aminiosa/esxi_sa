$oldWarningPreference = $WarningPreference
$WarningPreference = 'SilentlyContinue'
cd $args[3]
Connect-VIServer $args[0] -user $args[1] -password $args[2]
echo "<id:17>"
foreach ($vms in get-vm) {echo "$vms"; Get-VIPermission -Entity $vms | Select-Object -Property role,principal}
echo "</id:17>"
echo "<id:18>"
$content = get-vm; $Report=@(); foreach($Computer in $content){
$GeneralProp=[ordered]@{
"ComputerName"=$computer.Name;};$nic = 1
$Computer | Get-VirtualPortGroup | foreach { 
$GeneralProp.Add("NIC$($nic) vSwitch",$_.VirtualSwitch)
$GeneralProp.Add("NIC$($nic) PortGroup",$_.Name)
$GeneralProp.Add("NIC$($nic) VLAN ID",$_.VlanID)
$GeneralProp.Add("NIC$($nic) IP", $Computer.Guest.IPAddress[$nic-1])
$nic++};$Report += "$computer";$Report += New-Object -TypeName psobject -Property $GeneralProp};Echo $Report
echo "</id:18>"
echo "<id:100>"
Foreach ($VMHost in Get-VMHost ) {
$ESXCli = Get-EsxCli -VMHost $VMHost
$VMHost | Select Name, @{N="AcceptanceLevel";E={$ESXCli.software.acceptance.get()}}
}
echo "</id:100>"
echo "<id:101>"
Foreach ($VMHost in Get-VMHost ) {
$ESXCli = Get-EsxCli -VMHost $VMHost
$ESXCli.system.module.list() | Foreach { Echo $_.Name;
$ESXCli.system.module.get($_.Name) | Select @{N="VMHost";E={$VMHost}}, Module,
License,
Modulefile,
Version,
SignedStatus
#SignatureDigest,
#SignatureFingerPrint
} }
echo "</id:101>"
echo "<id:102>"
Get-VMHost | Select Name, @{N="NTPSetting";E={$_ | Get-VMHostNtpServer}}|fl
echo "</id:102>"
echo "<id:105>"
Get-VMHost | Select Name, @{N="Net.DVFilterBindIpAddress";E={$_ | GetVMHostAdvancedConfiguration Net.DVFilterBindIpAddress | Select -ExpandProperty Values}} | fl
echo "</id:105>"
echo "<id:107>"
Get-VMHost | Select Name, @{N="Syslog.global.logDir";E={$_ | GetVMHostAdvancedConfiguration Syslog.global.logDir | Select -ExpandProperty Values}} | fl
echo "</id:107>"
echo "<id:108>"
Get-VMHost | Select Name, @{N="Syslog.global.logHost";E={$_ | GetVMHostAdvancedConfiguration Syslog.global.logHost | Select -ExpandProperty Values}} | fl
echo "</id:108>"
echo "<id:109>"
Get-VMHost | Get-VMHostAuthentication | Select VmHost, Domain, DomainMembershipStatus | fl
echo "</id:109>"
echo "<id:110>"
Get-VMHost | Get-VMHostService | Where { $_.key -eq "DCUI" } | Select-Object Policy | fl
echo "</id:110>"
echo "<id:111>"
Get-VMHost | Get-VMHostService | Where { $_.key -eq "TSM" } | Select Policy | fl 
echo "</id:111>"
echo "<id:112>"
Get-VMHost | Get-VMHostService | Where { $_.key -eq "TSM" } | Select Policy | fl 
echo "</id:112>"
echo "<id:113>"
Get-VMHost | Select @{N="UserVars.ESXiShellInteractiveTimeOut";E={$_ | GetVMHostAdvancedConfiguration UserVars.ESXiShellInteractiveTimeOut | Select -ExpandProperty Values}} | fl
echo "</id:113>"
echo "<id:114>"
Get-VMHost | Select @{N="UserVars.ESXiShellInteractiveTimeOut";E={$_ | GetVMHostAdvancedConfiguration UserVars.ESXiShellInteractiveTimeOut | Select -ExpandProperty Values}} | fl
echo "</id:114>"
Disconnect-VIServer $args[0] -confirm:$false
$WarningPreference = $oldWarningPreference