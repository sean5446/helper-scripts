```
sudo apt-get install zerofree
```

```
sudo mount /dev/sdb -o remount,ro
zerofree -v /dev/sdb
```

```
DISKPART> select vdisk file="C:\Users\queso\AppData\Local\Packages\...\LocalState\ext4.vhdx"
```

or:
```
wsl --shutdown
Import-Module -Name Hyper-v
Optimize-VHD -Mode Full -Verbose $env:LOCALAPPDATA\Packages\$((Get-AppxPackage *Ubuntu*).PackageFamilyName)\LocalState\ext4.vhdx
```
