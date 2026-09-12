# Close the previous game server, then start a fresh one in this console.
# Repeated clicks are serialized by a mutex: each click stops the old Python
# process and starts a new one. Launcher cmd windows are never killed, because
# taskkill /T on those trees also aborted the click that was still starting.
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
        Where-Object { $_.CommandLine -and ($_.CommandLine -match '(server|server_dynamic_maps|server_pets|server_pet_system)\.py') } |
        ForEach-Object { $found += [int]$_.ProcessId }
    $found | Where-Object { $_ -gt 0 } | Select-Object -Unique
}

function Get-ParentPid {
    param([int]$ProcessId)
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction SilentlyContinue
    if ($null -eq $proc) { return 0 }
    return [int]$proc.ParentProcessId
}

function Get-ProtectedPids {
    param([int]$ProcessId)
    $found = @()
    $current = [int]$ProcessId
    $seen = @{}
    while ($current -gt 0 -and -not $seen.ContainsKey($current)) {
        $seen[$current] = $true
        $found += $current
        $current = Get-ParentPid -ProcessId $current
    }
    $found
}

function Stop-Pid {
    param([int]$ProcessId)
    Write-Host "Stopping PID $ProcessId"
    & taskkill.exe /PID $ProcessId /F 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
    }
}

function Wait-PortFree {
    param(
        [int]$PortNumber,
        [int]$TimeoutSeconds = 8
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $still = @(Get-ListeningPids -PortNumber $PortNumber)
        if ($still.Count -eq 0) { return }
        Start-Sleep -Milliseconds 200
    } while ((Get-Date) -lt $deadline)
    $still = @(Get-ListeningPids -PortNumber $PortNumber)
    if ($still.Count -gt 0) {
        throw "Port $PortNumber still LISTENING after close: $($still -join ', ')"
    }
}

$launchExit = 0
$pythonProcess = $null
$mutex = $null
$hasMutex = $false
try {
    $mutex = New-Object System.Threading.Mutex($false, 'Global\PiaomiaoSanJieLocalServerLaunch')
    try {
        $hasMutex = $mutex.WaitOne(30000)
    } catch [System.Threading.AbandonedMutexException] {
        $hasMutex = $true
    }
    if (-not $hasMutex) {
        Write-Host "Another launcher is already restarting the server. This extra window will close."
        $launchExit = 2
    } else {
        $protected = @(Get-ProtectedPids -ProcessId $PID)
        $ids = @()
        $ids += @(Get-ListeningPids -PortNumber $Port)
        $ids += @(Get-ServerPyPids)
        $ids = @($ids | Where-Object { $_ -gt 0 -and $protected -notcontains $_ } | Select-Object -Unique)
        if ($ids.Count -gt 0) {
            Write-Host "Closing previous server on port $Port"
            foreach ($procId in $ids) {
                Stop-Pid -ProcessId $procId
            }
        }
        Wait-PortFree -PortNumber $Port

        Write-Host "Starting $Python server_pet_system.py on 0.0.0.0:$Port advertising ${AdvertiseHost}:$Port"
        $pythonProcess = Start-Process -FilePath $Python -ArgumentList @(
            '.\server_pet_system.py',
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
            Write-Host "server_pet_system.py exited before binding port $Port (code $launchExit)"
        } else {
            Write-Host "Server is listening on port $Port"
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
# The replacement click already started a new window. Close this one instead of
# pausing on the taskkill exit code from the previous Python process.
exit 0
