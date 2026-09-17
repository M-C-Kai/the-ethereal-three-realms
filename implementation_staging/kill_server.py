import subprocess, os, sys, time

r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'], capture_output=True, text=True)
for line in r.stdout.strip().split('\n'):
    parts = line.strip().strip('"').split('","')
    if len(parts) >= 2:
        pid = parts[1]
        # Check command line for server.py
        r2 = subprocess.run(['wmic', 'process', 'where', f'processid={pid}', 'get', 'commandline'], capture_output=True, text=True)
        if 'server.py' in r2.stdout:
            print(f"Killing server PID {pid}")
            subprocess.run(['taskkill', '/F', '/PID', pid])
            time.sleep(1)
print("Done")
