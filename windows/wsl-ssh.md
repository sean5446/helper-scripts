### OpenSSH for WSL:
```
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

```cmd
Get-Service sshd
Start-Service sshd
```

or automatic:
```
Set-Service -Name sshd -StartupType 'Automatic'
```

```
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\WINDOWS\System32\bash.exe" -PropertyType String -Force
```
