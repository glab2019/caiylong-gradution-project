import threading
import socket

encoding = 'utf-8'
BUFSIZE = 1024

# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self.counter = [0,0,0]
        
    def run(self):
        while True:
            data = self.client.recv(BUFSIZE)
            if(data):
                string = bytes.decode(data, encoding)
                print(string, end='')  # 执行打印的是这里，对它进行操作
                # self.counter += 1
                LoRaID = string[3:4]
                stringtemp = string.split("\n")[0]
                if LoRaID == '1':
                    self.counter[0] += 1
                    with open('1.txt', 'w') as f:
                        f.write(str(self.counter[0]) + '  ')
                        f.write(stringtemp)
                elif LoRaID == '2':
                    self.counter[1] += 1
                    with open('2.txt', 'a+') as f:
                        f.write(str(self.counter[1]) + '  ')
                        f.write(stringtemp)
                elif LoRaID == '3':
                    self.counter[2] += 1
                    with open('3.txt', 'a+') as f:
                        f.write(str(self.counter[2]) + '  ')
                        f.write(stringtemp)
                # with open('data.txt', 'a+') as f:
                #     stringtemp = string.split("\n")[0]
                #     f.write(str(self.counter) + '  ')
                #     f.write(stringtemp)
                # print("counter: " + str(self.counter))
            else:
                
                break
        print("close:", self.client.getpeername())
        
    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = bytes.decode(rec, encoding)
            if len(string)>2:
                string = string[0:-2]
            else:
                string = ' '
        else:
            string = False
        return string
 
 
# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("192.168.0.179", port))
        self.sock.listen(0)
    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            Reader(client).start()
            cltadd = cltadd
            print("Connected!")
 
 
lst  = Listener(6001)   # create a listen thread
lst.start() # then start