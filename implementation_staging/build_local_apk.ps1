param(
    [Parameter(Mandatory = $true)]
    [string]$ServerIp,
    [Parameter(Mandatory = $true)]
    [string]$SourceApk,
    [int]$Port = 6805
)

$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BuildDir = Join-Path $ProjectDir 'build'
$UnsignedApk = Join-Path $BuildDir 'piaomiao_local_unsigned.apk'
$AlignedApk = Join-Path $BuildDir 'piaomiao_local_aligned.apk'
$FinalApk = Join-Path $ProjectDir 'piaomiao_local_login.apk'
$KeyStorePath = Join-Path $ProjectDir 'local-test-keystore.p12'
$PythonExe = 'python'
$AndroidBuildTools = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\35.0.0'
$ZipAlignExe = Join-Path $AndroidBuildTools 'zipalign.exe'
$ApkSignerBat = Join-Path $AndroidBuildTools 'apksigner.bat'
$KeyToolExe = 'C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot\bin\keytool.exe'

New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null

& $PythonExe (Join-Path $ProjectDir 'tools\patch_apk.py') $SourceApk $UnsignedApk --host $ServerIp --port $Port --channel 15
& $ZipAlignExe -p -f 4 $UnsignedApk $AlignedApk

if (-not (Test-Path -LiteralPath $KeyStorePath)) {
    & $KeyToolExe -genkeypair -keystore $KeyStorePath -storetype PKCS12 -storepass localtest123 -keypass localtest123 -alias localtest -keyalg RSA -keysize 2048 -validity 3650 -dname 'CN=Piaomiao Local Login,OU=Local Test,O=Codex,L=Local,ST=Local,C=CN'
}

& $ApkSignerBat sign --ks $KeyStorePath --ks-key-alias localtest --ks-pass pass:localtest123 --key-pass pass:localtest123 --out $FinalApk $AlignedApk
& $ApkSignerBat verify --verbose --print-certs $FinalApk
Write-Host "Created: $FinalApk"
