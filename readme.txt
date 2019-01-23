ESXi audit tool

Confguring hooks.
Hooks are set up in *.json files.
Structure of *.json file:
{
    {
        "Alert": "NULL",                #Alert that will be add if Condition is FALSE
        "Command": "uname -a",          #Command to get data from ESXi server via SSH
        "Condition": "NULL",            #Condition wrote in Python3. var - store results of Instruction section
        "Instruction": "\nglobal var, version, sName, jReport\nvar = var.split(\" \")\nsName = var[1]\njReport[sName] = {}\nversion = var[2]\nvar=var[1]",
                                        # Instruction - Set on Python 3 commands to execute to process the data that retrived with SSH
                                        # var - string that contains OUT of command "Command"
        "Msg": "Getting name of server", # Message that will be show during data collection
        "Name": "Name",                 # Name of parameter that will be written in Report
        "Parent": "Server,Group,VLAN",  # Structure of report
        "Ver": "0",                     # mimal version where that rule is acceptable
        "VerM": "99"                    # Maximal version where that rule is acceptable
    }
}
