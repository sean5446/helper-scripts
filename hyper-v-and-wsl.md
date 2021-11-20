### Hyper V:
Set-VM -VMName "Ubuntu 20.04" -EnhancedSessionTransportType HvSocket


### OpenSSH for WSL:
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

Start-Service sshd
Get-Service sshd

or automatic:
Set-Service -Name sshd -StartupType 'Automatic'

New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\WINDOWS\System32\bash.exe" -PropertyType String -Force

