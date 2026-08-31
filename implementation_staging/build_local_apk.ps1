param(
    [Parameter(Mandatory = $true)]
    [string]$ServerIp,
    [Parameter(Mandatory = $true)]
    [string]$SourceApk,
    [int]$Port = 6805,
    [string]$ApkTool = 'apktool',
    [string]$ApkToolJar = ''
)

$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BuildDir = Join-Path $ProjectDir 'build'
$ApkToolWorkDir = Join-Path ([System.IO.Path]::GetTempPath()) 'piaomiao-local-apk-build'
$FrameworkDir = Join-Path $ApkToolWorkDir 'framework'
$SmaliDir = Join-Path $ApkToolWorkDir 'decoded'
$RebuiltApk = Join-Path $ApkToolWorkDir 'piaomiao_decoded_rebuilt.apk'
$UnsignedApk = Join-Path $BuildDir 'piaomiao_local_unsigned.apk'
$AlignedApk = Join-Path $BuildDir 'piaomiao_local_aligned.apk'
$FinalApk = Join-Path $ProjectDir 'piaomiao_local_login.apk'
$KeyStorePath = Join-Path $ProjectDir 'local-test-keystore.p12'
$PythonExe = 'python'
$AndroidBuildTools = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\35.0.0'
$ZipAlignExe = Join-Path $AndroidBuildTools 'zipalign.exe'
$ApkSignerBat = Join-Path $AndroidBuildTools 'apksigner.bat'
$KeyToolExe = 'C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot\bin\keytool.exe'
$JavaExe = 'C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot\bin\java.exe'
$UseApkToolJar = $ApkToolJar -and (Test-Path -LiteralPath $ApkToolJar)

function Assert-NativeSuccess {
    param([Parameter(Mandatory = $true)][string]$Step)
    if ($LASTEXITCODE -ne 0) {
        throw "$Step failed (exit $LASTEXITCODE)"
    }
}

if (-not $UseApkToolJar -and -not (Get-Command $ApkTool -ErrorAction SilentlyContinue)) {
    throw "apktool not found on PATH ('$ApkTool'). Install apktool so the local NPC and battle smali patches can be applied."
}

New-Item -ItemType Directory -Force -Path $BuildDir, $ApkToolWorkDir, $FrameworkDir | Out-Null

# Decode the source APK, apply the local smali patches, then reassemble. This is
# required because the NPC handlers and native battle-escape transition live in
# the dex and cannot be injected through the channel.o overlay alone.
if ($UseApkToolJar) {
    & $JavaExe -jar $ApkToolJar d $SourceApk -o $SmaliDir -f -p $FrameworkDir
} else {
    & $ApkTool d $SourceApk -o $SmaliDir -f -p $FrameworkDir
}
if ($LASTEXITCODE -ne 0) { throw "apktool decode failed (exit $LASTEXITCODE)" }

& $PythonExe (Join-Path $ProjectDir 'tools\patch_npc_direction.py') $SmaliDir
Assert-NativeSuccess 'NPC direction/selection smali patch'
& $PythonExe (Join-Path $ProjectDir 'tools\patch_battle_escape.py') $SmaliDir
Assert-NativeSuccess 'battle escape timing/status smali patch'
& $PythonExe (Join-Path $ProjectDir 'tools\patch_battle_weapon.py') $SmaliDir
Assert-NativeSuccess 'battle idle weapon asset patch'

# The client only renders a distinct map id after loading both of its local
# map resources.  Kunlun reuses the proven map 58 composite-tile reference
# while keeping its own generated logical tile/collision map.
$DecodedMapDir = Join-Path $SmaliDir 'assets\res\map'
$ChanganMapRef = Join-Path $DecodedMapDir '58.map.ref'
$KunlunMapO = Join-Path $ProjectDir 'maps\60001.map.o'
if (-not (Test-Path -LiteralPath $ChanganMapRef)) {
    throw "source APK is missing required map reference: $ChanganMapRef"
}
if (-not (Test-Path -LiteralPath $KunlunMapO)) {
    throw "generated Kunlun map is missing: $KunlunMapO"
}
Copy-Item -LiteralPath $ChanganMapRef -Destination (Join-Path $DecodedMapDir '60001.map.ref') -Force
Copy-Item -LiteralPath $KunlunMapO -Destination (Join-Path $DecodedMapDir '60001.map.o') -Force

if ($UseApkToolJar) {
    & $JavaExe -jar $ApkToolJar b $SmaliDir -o $RebuiltApk -p $FrameworkDir
} else {
    & $ApkTool b $SmaliDir -o $RebuiltApk -p $FrameworkDir
}
if ($LASTEXITCODE -ne 0) { throw "apktool build failed (exit $LASTEXITCODE)" }

# Inject the local login endpoint into the reassembled APK (assets/res/channel.o).
& $PythonExe (Join-Path $ProjectDir 'tools\patch_apk.py') $RebuiltApk $UnsignedApk --host $ServerIp --port $Port --channel 15
Assert-NativeSuccess 'APK endpoint patch'
& $ZipAlignExe -p -f 4 $UnsignedApk $AlignedApk
Assert-NativeSuccess 'zipalign'

if (-not (Test-Path -LiteralPath $KeyStorePath)) {
    & $KeyToolExe -genkeypair -keystore $KeyStorePath -storetype PKCS12 -storepass localtest123 -keypass localtest123 -alias localtest -keyalg RSA -keysize 2048 -validity 3650 -dname 'CN=Piaomiao Local Login,OU=Local Test,O=Codex,L=Local,ST=Local,C=CN'
    Assert-NativeSuccess 'test keystore generation'
}

& $ApkSignerBat sign --ks $KeyStorePath --ks-key-alias localtest --ks-pass pass:localtest123 --key-pass pass:localtest123 --out $FinalApk $AlignedApk
Assert-NativeSuccess 'APK signing'
& $ApkSignerBat verify --verbose --print-certs $FinalApk
Assert-NativeSuccess 'APK signature verification'
Write-Host "Created: $FinalApk"
