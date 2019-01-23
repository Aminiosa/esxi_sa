["$content = get-vm; $Report=@(); foreach($Computer in $content){",
      "$GeneralProp=\"ordered\"@{",
      "\"ComputerName\"=$computer.Name;};$nic = 1",
      "$Computer | Get-VirtualPortGroup | foreach {",
      "$GeneralProp.Add(\"NIC$($nic) vSwitch\",$_.VirtualSwitch)",
      "$GeneralProp.Add(\"NIC$($nic) PortGroup\",$_.Name)",
      "$GeneralProp.Add(\"NIC$($nic) VLAN ID\",$_.VlanID)",
      "$GeneralProp.Add(\"NIC$($nic) IP\", $Computer.Guest.IPAddress\"$nic-1\")",
      "$nic++};$Report += \"$computer\";$Report += New-Object -TypeName psobject -Property $GeneralProp};Echo $Report"
    ]