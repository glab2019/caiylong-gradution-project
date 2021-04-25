from PyQt5 import QtWidgets
import ui
import socket
import threading
import sys
import stopThreading
import time


class TcpLogic(ui.ToolsUi):
    def __init__(self, num):
        super(TcpLogic, self).__init__(num)
        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()

        self.link = False  # 用于标记是否开启了连接

    def tcp_server_start(self):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            port = int(self.lineEdit_port.text())  # 开启TCP server模式后侦听端口
            self.tcp_socket.bind(('', port))
        except Exception as ret:
            msg = '请检查端口号\n'
            self.signal_write_msg1.emit(msg)
            self.signal_write_msg2.emit(msg)
        else:
            self.tcp_socket.listen()  # 侦听
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            msg = 'TCPServer is listening port: %s\n' % str(port)
            self.signal_write_msg1.emit(msg)
            self.signal_write_msg2.emit(msg)

    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                time.sleep(0.001)
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                msg = 'TCPServer has connected to IP: %s and port: %s\n' % client_address
                self.signal_write_msg1.emit(msg)
                self.signal_write_msg2.emit(msg)
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')   # 在这里处理数据 接收数据
                        lora_id = msg[3:4]
                        if lora_id == '1':
                            self.signal_write_msg1.emit( msg)
                            with open('1.txt', 'a+') as f:
                                f.write(msg.split("\n")[0])

                        if lora_id == '2':
                            self.signal_write_msg2.emit(msg)
                            with open('2.txt', 'a+') as f:
                                f.write(msg.split("\n")[0])
                        # msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0], address[1], msg)
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def tcp_send(self, command):
        """
        功能函数，用于TCP服务端和TCP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '请先连接网关再操作\n'
            self.signal_write_msg1.emit(msg)  # 发送信号量 会调用 write_msg函数
            self.signal_write_msg2.emit(msg)
        else:
            # (str(self.textEdit_send.toPlainText())).encode('utf-8')
            send_msg = command.encode('utf-8')    # 这里是发送框的内容
            try:
                # 向所有连接的客户端发送消息
                if command == 'get':
                    msg = '正在准备接收\n'
                    self.signal_write_msg1.emit(msg)  # 同样需要告诉接收框， 用来显示内容（实际上是让发送框与接收框通信）
                    self.signal_write_msg2.emit(msg)
                if command == 'sp':
                    msg = '已经停止接收\n'
                    self.signal_write_msg1.emit(msg)  # 同样需要告诉接收框， 用来显示内容（实际上是让发送框与接收框通信）
                    self.signal_write_msg2.emit(msg)
                if command == 'go':
                    msg = '正在准备接收1\n'
                    self.signal_write_msg1.emit(msg)  # 同样需要告诉接收框， 用来显示内容（实际上是让发送框与接收框通信）
                    # self.signal_write_msg2.emit(msg)
                if command == 'so':
                    msg = '已经停止接收1\n'
                    self.signal_write_msg1.emit(msg)  # 同样需要告诉接收框， 用来显示内容（实际上是让发送框与接收框通信）
                    # self.signal_write_msg2.emit(msg)
                if command == 'gt':
                    msg = '正在准备接收2\n'
                    # self.signal_write_msg1.emit(msg)  # 同样需要告诉接收框， 用来显示内容（实际上是让发送框与接收框通信）
                    self.signal_write_msg2.emit(msg)
                if command == 'st':
                    msg = '已经停止接收2\n'
                    # self.signal_write_msg1.emit(msg)  # 同样需要告诉接收框， 用来显示内容（实际上是让发送框与接收框通信）
                    self.signal_write_msg2.emit(msg)
                for client, address in self.client_socket_list:
                    client.send(send_msg)
            except Exception as ret:
                msg = '发送失败，请检查连接\n'
                self.signal_write_msg1.emit(msg)
                self.signal_write_msg2.emit(msg)

    def tcp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        # if self.TCP_Server_Label.currentIndex() == 0:
        try:
            for client, address in self.client_socket_list:
                client.close()
            self.tcp_socket.close()
            if self.link is True:
                msg = 'Disconnected!\n'
                self.signal_write_msg1.emit(msg)
                self.signal_write_msg2.emit(msg)
        except Exception as ret:
            pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = TcpLogic(1)
    ui.show()
    sys.exit(app.exec_())
