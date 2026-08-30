param(
    [Parameter(Mandatory = $true)]
    [string]$ServerIp,
    [Parameter(Mandatory = $true)]
    [string]$SourceApk,
    [int]$Port = 6805,
    [string]$ApkTool = 'apktool'
)

$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BuildDir = Join-Path $ProjectDir 'build'
$SmaliDir = Join-Path $BuildDir 'apk_decoded'
$RebuiltApk = Join-Path $BuildDir 'piaomiao_decoded_rebuilt.apk'
$UnsignedApk = Join-Path $BuildDir 'piaomiao_local_unsigned.apk'
$AlignedApk = Join-Path $BuildDir 'piaomiao_local_aligned.apk'
$FinalApk = Join-Path $ProjectDir 'piaomiao_local_login.apk'
$KeyStorePath = Join-Path $ProjectDir 'local-test-keystore.p12'
$PythonExe = 'python'
$AndroidBuildTools = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\35.0.0'
$ZipAlignExe = Join-Path $AndroidBuildTools 'zipalign.exe'
$ApkSignerBat = Join-Path $AndroidBuildTools 'apksigner.bat'
$KeyToolExe = 'C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot\bin\keytool.exe'

if (-not (Get-Command $ApkTool -ErrorAction SilentlyContinue)) {
    throw "apktool not found on PATH ('$ApkTool'). Install apktool so the 1126 subtype=1 NPC-direction smali patch can be applied."
}

New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null

# Decode the source APK, apply the local smali patches, then reassemble. This is
# required because the 1126 subtype=1 (NPC in-place rotation) handler lives in the
# dex and cannot be injected via the channel.o overlay alone.
& $ApkTool d $SourceApk -o $SmaliDir -f
if ($LASTEXITCODE -ne 0) { throw "apktool decode failed (exit $LASTEXITCODE)" }

& $PythonExe (Join-Path $ProjectDir 'tools\patch_npc_direction.py') $SmaliDir
if ($LASTEXITCODE -ne 0) { throw "npc direction smali patch failed (exit $LASTEXITCODE)" }

& $ApkTool b $SmaliDir -o $RebuiltApk
if ($LASTEXITCODE -ne 0) { throw "apktool build failed (exit $LASTEXITCODE)" }

# Inject the local login endpoint into the reassembled APK (assets/res/channel.o).
& $PythonExe (Join-Path $ProjectDir 'tools\patch_apk.py') $RebuiltApk $UnsignedApk --host $ServerIp --port $Port --channel 15
& $ZipAlignExe -p -f 4 $UnsignedApk $AlignedApk

if (-not (Test-Path -LiteralPath $KeyStorePath)) {
    & $KeyToolExe -genkeypair -keystore $KeyStorePath -storetype PKCS12 -storepass localtest123 -keypass localtest123 -alias localtest -keyalg RSA -keysize 2048 -validity 3650 -dname 'CN=Piaomiao Local Login,OU=Local Test,O=Codex,L=Local,ST=Local,C=CN'
}

& $ApkSignerBat sign --ks $KeyStorePath --ks-key-alias localtest --ks-pass pass:localtest123 --key-pass pass:localtest123 --out $FinalApk $AlignedApk
& $ApkSignerBat verify --verbose --print-certs $FinalApk
Write-Host "Created: $FinalApk"
