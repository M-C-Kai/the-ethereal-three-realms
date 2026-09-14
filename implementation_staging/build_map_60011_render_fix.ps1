param(
    [string]$SourceApk = (Join-Path $PSScriptRoot 'build_artifacts\apk\piaomiao_local_60011.apk'),
    [string]$OutputApk = (Join-Path $PSScriptRoot 'build_artifacts\apk\piaomiao_local_60011_render_fix.apk'),
    [string]$ApkToolJar = 'C:\Users\Kail\AppData\Local\Temp\apktools\apktool.jar'
)

$ErrorActionPreference = 'Stop'
$RunDir = Join-Path $env:TEMP ('piaomiao-map-60011-render-fix-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$Decoded = Join-Path $RunDir 'decoded'
$Framework = Join-Path $RunDir 'framework'
$Unsigned = Join-Path $RunDir 'unsigned.apk'
$Aligned = Join-Path $RunDir 'aligned.apk'
$Java = 'C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot\bin\java.exe'
$BuildTools = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\35.0.0'
$Keystore = Join-Path $PSScriptRoot 'build_artifacts\signing\local-test-keystore.p12'

foreach ($required in @($SourceApk, $ApkToolJar, $Java, $Keystore,
                       (Join-Path $BuildTools 'zipalign.exe'),
                       (Join-Path $BuildTools 'apksigner.bat'))) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Missing build input: $required" }
}
New-Item -ItemType Directory -Force -Path $RunDir, $Framework | Out-Null
& $Java -jar $ApkToolJar d $SourceApk -o $Decoded -p $Framework
if ($LASTEXITCODE -ne 0) { throw 'APK decode failed' }
& 'D:\python\python.exe' (Join-Path $PSScriptRoot 'tools\patch_map_60011_render_range.py') `
    (Join-Path $Decoded 'smali\pmsj\work\b\m.smali')
if ($LASTEXITCODE -ne 0) { throw 'Map render patch failed' }
& $Java -jar $ApkToolJar b $Decoded -o $Unsigned -p $Framework
if ($LASTEXITCODE -ne 0) { throw 'APK build failed' }
& (Join-Path $BuildTools 'zipalign.exe') -p -f 4 $Unsigned $Aligned
if ($LASTEXITCODE -ne 0) { throw 'zipalign failed' }
& (Join-Path $BuildTools 'apksigner.bat') sign --ks $Keystore --ks-key-alias localtest `
    --ks-pass pass:localtest123 --key-pass pass:localtest123 --out $OutputApk $Aligned
if ($LASTEXITCODE -ne 0) { throw 'APK signing failed' }
& (Join-Path $BuildTools 'apksigner.bat') verify --verbose --print-certs $OutputApk
if ($LASTEXITCODE -ne 0) { throw 'APK verification failed' }
Write-Host "Created: $OutputApk"
