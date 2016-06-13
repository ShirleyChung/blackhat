import socket

t_host = "172.16.43.54"
t_port = 22

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((t_host, t_port))

client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

print client.recv(4096)