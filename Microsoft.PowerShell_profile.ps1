
echo $PSVersionTable | findstr "PSVersion"

echo "Profile: $PROFILE" 

# stylize powershell console with oh-my-posh
if (Test-Path -Path "$env:POSH_THEMES_PATH" -PathType Container) {
    oh-my-posh init pwsh | Invoke-Expression
}

# if vcpkg loaded source vcpkg
if (Test-Path -Path "~/.vcpkg/vcpkg-init.ps1" -PathType Leaf) {
    . ~/.vcpkg/vcpkg-init.ps1
}

# if visual studio installed, load cmake, etc
if (Test-Path -Path (Join-Path ${env:ProgramFiles(x86)} '\\Microsoft Visual Studio\\Installer\\vswhere.exe') -PathType Leaf) {
    &{$vsPath = &(Join-Path ${env:ProgramFiles(x86)} '\\Microsoft Visual Studio\\Installer\\vswhere.exe') -property installationpath; Import-Module (Join-Path $vsPath 'Common7\\Tools\\Microsoft.VisualStudio.DevShell.dll'); Enter-VsDevShell -VsInstallPath $vsPath -SkipAutomaticLocation}
}

# aliases
function which($name)
{
    Get-Command $name | Select-Object -ExpandProperty Definition
}

function ifconfig()
{
    ipconfig
}

function grep($pat, $path)
{
    Select-String -Path $path -Pattern $pat
}

function rm($path) {
    Remove-Item -Force -Recurse -LiteralPath $path 
}

# function find($pat)
# {
#     Get-ChildItem -Recurse -Filter $pat
# }
