### Hyper V:
## VM install
- generation 2 - don't enable secure boot
- don't auto-login
```sh
sudo apt-get install xrdp
sudo systemctl enable xrdp
```

Powershell (elevated)

`Set-VM -VMName "Ubuntu 22.04" -EnhancedSessionTransportType HvSocket`

