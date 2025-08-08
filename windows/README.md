# Windows Stuff

## Zsh in MinGW for Git Bash
Download zsh https://packages.msys2.org/packages/zsh?repo=msys&variant=x86_64

Extract files and copy `usr` and `etc` to `C:\Program Files\Git`

Edit `~/.bash_profile` and add `exec zsh` to end of file


## Edit Remote Desktop Connections
```
HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default
```

## OpenSSH:
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

can change here to start WSL instead
```
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\WINDOWS\System32\bash.exe" -PropertyType String -Force
```

## Bypass windows 11 microsoft account
Press `Shift + F10` to launch the Command Prompt.

This command will bypass: `OOBE\BYPASSNRO` + Enter

taskmgr can end processes like "Network Connection Flow"

ipconfig /release can disconnect network


## Remote Desktop Entries

GetKey delete entries from `Computer\HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default`

## Quick hard drive perf test

`winsat disk -drive g`

