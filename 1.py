from distutils.version import LooseVersion
version = "6.7.0"

if (LooseVersion(version) <= LooseVersion('0')) and (LooseVersion(version) > LooseVersion('99')):
    print("That scrip is't capable with this version. Server version:", version)
else:
    print("ok")