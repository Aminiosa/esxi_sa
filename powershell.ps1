$oldWarningPreference = $WarningPreference
$WarningPreference = 'SilentlyContinue'
cd $args[3]
Connect-VIServer $args[0] -user $args[1] -password $args[2]
echo "<id:17>"
Foreach ($VMHost in Get-VMHost ) {
$ESXCli = Get-EsxCli -VMHost $VMHost
$VMHost | Select Name, @{N="AcceptanceLevel";E={$ESXCli.software.acceptance.get()}}
}
echo "</id:17>"
echo "<id:18>"
Foreach ($VMHost in Get-VMHost ) {
$ESXCli = Get-EsxCli -VMHost $VMHost
$ESXCli.system.module.list() | Foreach {
$ESXCli.system.module.get($_.Name) | Select @{N="VMHost";E={$VMHost}}, Module,
License, Modulefile, Version, SignedStatus, SignatureDigest, SignatureFingerPrint
}
}
echo "</id:18>"
Disconnect-VIServer $args[0] -confirm:$false
$WarningPreference = $oldWarningPreference