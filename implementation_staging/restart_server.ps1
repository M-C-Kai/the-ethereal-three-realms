# Kill every process bound to the game port, close leftover launcher windows,
# then start a fresh local server in this console.
param(
    [int]$Port = 6805,
    [string]$AdvertiseHost = '192.168.0.104',
    [string]$Python = 'D:\python\python.exe'
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Get-ListeningPids {
    param([int]$PortNumber)
    $found = @()
    foreach ($line in (& netstat -ano)) {
        if ($line -notmatch 'LISTENING') { continue }
        if ($line -notmatch ":$PortNumber\s") { continue }
        if ($line -match '\s(\d+)\s*$') {
            $found += [int]$Matches[1]
        }
    }
    $found | Where-Object { $_ -gt 0 } | Select-Object -Unique
}

function Get-ServerPyPids {
    $found = @()
    Get-CimInstance Win32_Process -Filter "Name = 'python.exe' OR Name = 'pythonw.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -and ($_.CommandLine -match 'server\.py') } |
        ForEach-Object { $found += [int]$_.ProcessId }
    $found | Where-Object { $_ -gt 0 } | Select-Object -Unique
}

function Get-LauncherCmdPids {
    $found = @()
    Get-CimInstance Win32_Process -Filter "Name = 'cmd.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -and ($_.CommandLine -match 'start_server\.bat') } |
        ForEach-Object { $found += [int]$_.ProcessId }
    Get-Process -Name cmd -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowTitle -eq 'PiaomiaoLocalServer' } |
        ForEach-Object { $found += [int]$_.Id }
    $found | Where-Object { $_ -gt 0 } | Select-Object -Unique
}

function Get-ParentPid {
    param([int]$ProcessId)
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction SilentlyContinue
    if ($null -eq $proc) { return 0 }
    return [int]$proc.ParentProcessId
}

function Stop-PidTree {
    param([int]$ProcessId)
    Write-Host "Stopping PID $ProcessId"
    & taskkill.exe /PID $ProcessId /T /F 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
    }
}

$launchExit = 0
$pythonProcess = $null
$mutex = $null
$hasMutex = $false
try {
    $mutex = New-Object System.Threading.Mutex($false, 'Global\PiaomiaoSanJieLocalServerLaunch')
    try {
        $hasMutex = $mutex.WaitOne(15000)
    } catch [System.Threading.AbandonedMutexException] {
        $hasMutex = $true
    }
    if (-not $hasMutex) {
        Write-Host "Another launcher is already restarting the server. This extra window will close."
        $launchExit = 2
    } else {
        $selfPid = $PID
        $parentPid = Get-ParentPid -ProcessId $selfPid
        $ids = @()
        $ids += @(Get-ListeningPids -PortNumber $Port)
        $ids += @(Get-ServerPyPids)
        $ids += @(Get-LauncherCmdPids)
        $ids = $ids | Where-Object { $_ -gt 0 -and $_ -ne $selfPid -and $_ -ne $parentPid } | Select-Object -Unique
        foreach ($procId in $ids) {
            Stop-PidTree -ProcessId $procId
        }

        $deadline = (Get-Date).AddSeconds(8)
        do {
            $still = @(Get-ListeningPids -PortNumber $Port)
            if ($still.Count -eq 0) { break }
            Start-Sleep -Milliseconds 200
        } while ((Get-Date) -lt $deadline)

        $still = @(Get-ListeningPids -PortNumber $Port)
        if ($still.Count -gt 0) {
            throw "Port $Port still LISTENING after kill: $($still -join ', ')"
        }

        Write-Host "Starting $Python server.py on 0.0.0.0:$Port advertising ${AdvertiseHost}:$Port"
        $pythonProcess = Start-Process -FilePath $Python -ArgumentList @(
            '.\server.py',
            '--host', '0.0.0.0',
            '--port', "$Port",
            '--advertise-host', $AdvertiseHost
        ) -WorkingDirectory $Root -NoNewWindow -PassThru

        $deadline = (Get-Date).AddSeconds(8)
        do {
            if ($pythonProcess.HasExited) { break }
            $bound = @(Get-ListeningPids -PortNumber $Port)
            if ($bound.Count -gt 0) { break }
            Start-Sleep -Milliseconds 100
        } while ((Get-Date) -lt $deadline)

        if ($pythonProcess.HasExited) {
            $launchExit = $pythonProcess.ExitCode
            if ($launchExit -eq 0) { $launchExit = 1 }
            Write-Host "server.py exited before binding port $Port (code $launchExit)"
        }
    }
} catch {
    Write-Host $_
    if ($launchExit -eq 0) { $launchExit = 1 }
} finally {
    if ($hasMutex -and $null -ne $mutex) {
        [void]$mutex.ReleaseMutex()
        $hasMutex = $false
    }
    if ($null -ne $mutex) {
        $mutex.Dispose()
    }
}

if ($launchExit -ne 0) {
    exit $launchExit
}
if ($null -eq $pythonProcess) {
    exit 1
}
$pythonProcess.WaitForExit()
exit $pythonProcess.ExitCode
