param(
    [Parameter(Mandatory = $true)]
    [string]$ServerIp,
    [Parameter(Mandatory = $true)]
    [string]$SourceApk,
    [int]$Port = 6805
)

$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceDir = Resolve-Path (Join-Path $ProjectDir '..\..')
$ApkToolJar = Join-Path $WorkspaceDir 'work\tools\apktool.jar'
$DecodeDir = Join-Path $WorkspaceDir 'work\apk-person-panel'
$FrameworkDir = Join-Path $WorkspaceDir 'work\apktool-framework'
$BuildDir = Join-Path $ProjectDir 'build'
$RebuiltApk = Join-Path $BuildDir 'person_panel_rebuilt.apk'
$PatchedApk = Join-Path $BuildDir 'person_panel_endpoint.apk'
$AlignedApk = Join-Path $BuildDir 'person_panel_aligned.apk'
$FinalApk = Join-Path $ProjectDir 'piaomiao_local_person_panel.apk'
$KeyStorePath = Join-Path $ProjectDir 'local-test-keystore.p12'
$AndroidBuildTools = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\35.0.0'
$ZipAlignExe = Join-Path $AndroidBuildTools 'zipalign.exe'
$ApkSignerBat = Join-Path $AndroidBuildTools 'apksigner.bat'
$JavaExe = 'C:\Program Files\Microsoft\jdk-21.0.11.10-hotspot\bin\java.exe'

New-Item -ItemType Directory -Force -Path $BuildDir, $FrameworkDir | Out-Null

& $JavaExe -jar $ApkToolJar d -f -r -p $FrameworkDir -o $DecodeDir $SourceApk
& python (Join-Path $ProjectDir 'tools\patch_person_shortcut.py') $DecodeDir
& $JavaExe -jar $ApkToolJar b -p $FrameworkDir -o $RebuiltApk $DecodeDir
& python (Join-Path $ProjectDir 'tools\patch_apk.py') $RebuiltApk $PatchedApk --host $ServerIp --port $Port --channel 15
& $ZipAlignExe -p -f 4 $PatchedApk $AlignedApk
& $ApkSignerBat sign --ks $KeyStorePath --ks-key-alias localtest --ks-pass pass:localtest123 --key-pass pass:localtest123 --out $FinalApk $AlignedApk
& $ApkSignerBat verify --verbose --print-certs $FinalApk
Write-Host "Created: $FinalApk"
