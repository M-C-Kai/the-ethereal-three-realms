param(
    [string]$SourceApk = (Join-Path $PSScriptRoot 'build_artifacts\apk\piaomiao_local_team.apk'),
    [string]$OutputApk = (Join-Path $PSScriptRoot 'build_artifacts\apk\piaomiao_local_60011.apk')
)

$ErrorActionPreference = 'Stop'
$BuildTools = Join-Path $env:LOCALAPPDATA 'Android\Sdk\build-tools\35.0.0'
$ZipAlign = Join-Path $BuildTools 'zipalign.exe'
$ApkSigner = Join-Path $BuildTools 'apksigner.bat'
$Keystore = Join-Path $PSScriptRoot 'build_artifacts\signing\local-test-keystore.p12'
$Python = 'D:\python\python.exe'
$Unsigned = Join-Path $PSScriptRoot 'build_artifacts\build\piaomiao_60011_unsigned.apk'
$Aligned = Join-Path $PSScriptRoot 'build_artifacts\build\piaomiao_60011_aligned.apk'

foreach ($required in @($SourceApk, $ZipAlign, $ApkSigner, $Keystore, $Python,
                       (Join-Path $PSScriptRoot 'maps\60011\source_scene.png'))) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Missing build input: $required" }
}
New-Item -ItemType Directory -Force -Path (Split-Path $Unsigned), (Split-Path $OutputApk) | Out-Null
& $Python (Join-Path $PSScriptRoot 'tools\build_map_60011_apk.py') `
    --source-apk $SourceApk --unsigned-apk $Unsigned
if ($LASTEXITCODE -ne 0) { throw 'Map resource generation failed' }
& $ZipAlign -p -f 4 $Unsigned $Aligned
if ($LASTEXITCODE -ne 0) { throw 'zipalign failed' }
& $ApkSigner sign --ks $Keystore --ks-key-alias localtest `
    --ks-pass pass:localtest123 --key-pass pass:localtest123 `
    --out $OutputApk $Aligned
if ($LASTEXITCODE -ne 0) { throw 'APK signing failed' }
& $ApkSigner verify --verbose --print-certs $OutputApk
if ($LASTEXITCODE -ne 0) { throw 'APK verification failed' }
Write-Host "Created: $OutputApk"
