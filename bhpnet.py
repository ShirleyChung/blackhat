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
    
    
    