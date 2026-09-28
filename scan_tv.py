import socket
import threading
import subprocess

def check_port(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, 8000))
        if result == 0:
            print(f"FOUND TV BOX AT: {ip}")
        sock.close()
    except:
        pass

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

local_ip = get_local_ip()
print(f"PC Local IP: {local_ip}")
prefix = '.'.join(local_ip.split('.')[:-1]) + '.'

threads = []
for i in range(1, 255):
    ip = prefix + str(i)
    if ip == local_ip: continue
    t = threading.Thread(target=check_port, args=(ip,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Scan complete.")
