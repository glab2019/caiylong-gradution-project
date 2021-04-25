from PyQt5 import QtWidgets
import tcp_logic
import sys
import matplotlib.pyplot as plt
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
is_close = False  # global的用法是在局部中使用，然后就可以操作这个全局变量了，而不是在开头声明为global
is_node1_plt = False
is_node2_plt = False
is_showing_tow = False

class MainWindow(tcp_logic.TcpLogic):
    def __init__(self, num):
        super(MainWindow, self).__init__(num)
        self.client_socket_list = list()
        self.another = None
        self.link = False  # 是否已连接


    def connect(self, ):
        """
        控件信号-槽的设置
        :param : QDialog类创建的对象
        :return: None
        """
        # 如需传递参数可以修改为connect(lambda: self.click(参数))
        # 绑定按钮的功能
        super(MainWindow, self).connect()
        self.pushButton_link.clicked.connect(self.click_link)
        self.pushButton_unlink.clicked.connect(self.click_unlink)
        self.pushButton_clear.clicked.connect(self.click_clear)
        self.pushButton_clear2.clicked.connect(self.click_clear2)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_begin_data.clicked.connect(self.begin_data)
        self.pushButton_stop_data.clicked.connect(self.stop_data)

        self.pushButton_get_node1.clicked.connect(self.begin_node1_data)
        self.pushButton_stop_node1.clicked.connect(self.stop_node1_data)
        self.pushButton_get_node2.clicked.connect(self.begin_node2_data)
        self.pushButton_stop_node2.clicked.connect(self.stop_node2_data)

        self.pushButton_clear_history.clicked.connect(self.clear_history)

    def click_link(self):
        """
        pushbutton_link控件点击触发的槽
        :return: None
        """
        self.tcp_server_start()  # 直接TCP Server模式
        self.link = True
        self.pushButton_unlink.setEnabled(True)
        self.pushButton_link.setEnabled(False)

    def click_unlink(self):
        """
        pushbutton_unlink控件点击触发的槽
        :return: None
        """
        # 关闭连接
        self.close_all()
        self.link = False
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def click_clear(self):
        self.textBrowser_recv.clear()

    def clear_history(self):
        self.click_clear()
        self.click_clear2()
        clear_all_history()

    def click_clear2(self):
        """
        pushbutton_clear控件点击触发的槽
        :return: None
        """
        # 清空接收区屏幕
        self.textBrowser_recv2.clear()

    def close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        # 连接时根据用户选择的功能调用函数
        self.tcp_close()  # 直接使用TCP
        self.reset()

    def reset(self):
        """
        功能函数，将按钮重置为初始状态
        :return:None
        """
        self.link = False
        self.client_socket_list = list()
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def begin_data(self):
        global is_close
        is_close = False
        self.tcp_send('get')  # 将tcp_send设置成发送'get'
        if self.link:
            draw_my_figure()
        # draw_my_figure()

    def stop_data(self):
        self.tcp_send('sp')
        global is_close
        global is_node1_plt
        global is_node2_plt
        global is_showing_tow
        is_showing_tow = False
        is_close = True
        is_node1_plt = False
        is_node2_plt = False
        # close_fig()
    def begin_node1_data(self):
        global is_close
        is_close = False
        self.tcp_send('go')
        global is_node1_plt
        global is_node2_plt
        global is_showing_tow
        is_node1_plt = True
        if self.link:
            if is_showing_tow:
                pass
            else:
                if is_node2_plt:
                    close_fig()
                    draw_my_figure()
                else:
                    close_fig()
                    only_get_node1_data()
    def begin_node2_data(self):
        global is_close
        is_close = False
        self.tcp_send('gt')
        global is_node1_plt
        global is_node2_plt
        global is_showing_tow
        is_node2_plt = True
        if self.link:
            if is_showing_tow:
                pass
            else:
                if is_node1_plt:
                    close_fig()
                    draw_my_figure()
                else:
                    close_fig()
                    only_get_node2_data()
    def stop_node1_data(self):
        self.tcp_send('so')
        global is_close
        global is_node1_plt
        global is_node2_plt
        global is_showing_tow
        if is_showing_tow:
            close_fig()
            only_get_node2_data()
        else:
            is_close = True
            close_fig()
        is_showing_tow = False
        is_node1_plt = False
        is_node2_plt = False
    def stop_node2_data(self):
        self.tcp_send('st')
        global is_close
        global is_node1_plt
        global is_node2_plt
        global is_showing_tow
        if is_showing_tow:
            close_fig()
            only_get_node1_data()
        else:
            is_close = True
            close_fig()
        is_showing_tow = False
        is_node2_plt = False
        is_node1_plt = False
def only_get_node1_data():
    humidity1 = []
    temperature1 = []
    # length = 0
    plt.figure(figsize=(5.5, 5))
    plt.ion()
    while True:
        plt.clf()
        with open('1.txt', 'r') as f:
            file_content1 = f.readlines()
        for each_line in file_content1:
            humidity1.append(int(each_line.split('H:')[1].split('%')[0]))
            temperature1.append(float(each_line.split('T:')[1].split('C')[0]))
        # length += 1
        x = range(len(humidity1))
        ag = plt.subplot(1, 1, 1)
        ag.set_title('节点1温湿度')
        ag.set_xlabel('次数')
        ag.set_ylabel('温湿度')
        ag.set_xlim(0, len(x))
        ag.set_ylim(-5, 100)
        plt.plot(x, humidity1, color='r', label='湿度')
        plt.plot(x, temperature1, color='g', label='温度')
        humidity1 = []
        temperature1 = []
        plt.legend()  # 显示label
        plt.grid()
        if not is_close:
            plt.show()
        if is_close:
            plt.close()
            break
        plt.pause(2)
    plt.ioff()
    plt.show()
def only_get_node2_data():
    humidity2 = []
    temperature2 = []
    # length = 0
    plt.figure(figsize=(5.5, 5))
    plt.ion()
    while True:
        plt.clf()
        # length += 1
        with open('2.txt', 'r') as f:
            file_content2 = f.readlines()
        for each_line in file_content2:
            humidity2.append(int(each_line.split('H:')[1].split('%')[0]))
            temperature2.append(float(each_line.split('T:')[1].split('C')[0]))
        x = range(len(humidity2))
        bg = plt.subplot(1, 1, 1)
        bg.set_title('节点2温湿度')
        bg.set_xlabel('次数')
        bg.set_ylabel('温湿度')
        bg.set_xlim(0, len(x))
        bg.set_ylim(-5, 100)
        plt.plot(x, humidity2, color='r', label='湿度')
        plt.plot(x, temperature2, color='g', label='温度')
        humidity2 = []
        temperature2 = []
        plt.legend()  # 显示label
        plt.grid()
        if not is_close:
            plt.show()
        if is_close:
            plt.close()
            break
        plt.pause(2)
    plt.ioff()
    plt.show()
def draw_my_figure():
    global is_showing_tow
    is_showing_tow = True
    humidity1 = []
    temperature1 = []
    humidity2 = []
    temperature2 = []
    # length = 0
    plt.figure(figsize=(11, 5))
    plt.ion()
    while True:
        plt.clf()
        plt.suptitle("温湿度")
        with open('1.txt', 'r') as f:
            file_content1 = f.readlines()
        for each_line in file_content1:
            humidity1.append(int(each_line.split('H:')[1].split('%')[0]))
            temperature1.append(float(each_line.split('T:')[1].split('C')[0]))
        # length += 1
        x = range(len(humidity1))
        ag = plt.subplot(1, 2, 1)
        ag.set_title('节点1温湿度')
        ag.set_xlabel('次数')
        ag.set_ylabel('温湿度')
        ag.set_xlim(0, len(x))
        ag.set_ylim(-5, 100)
        plt.plot(x, humidity1, color='r', label='湿度')
        plt.plot(x, temperature1, color='g', label='温度')
        plt.grid()
        humidity1 = []
        temperature1 = []
        # plt.title("节点1温湿度曲线")
        # plt.xlabel('次数')
        # plt.ylabel('湿度或温度')
        # plt.xlim(0, length)
        # plt.ylim(-5, 100)
        with open('2.txt', 'r') as f:
            file_content2 = f.readlines()
        for each_line in file_content2:
            humidity2.append(int(each_line.split('H:')[1].split('%')[0]))
            temperature2.append(float(each_line.split('T:')[1].split('C')[0]))
        x = range(len(humidity2))
        bg = plt.subplot(1, 2, 2)
        bg.set_title('节点2温湿度')
        bg.set_xlabel('次数')
        bg.set_ylabel('温湿度')
        bg.set_xlim(0, len(x))
        bg.set_ylim(-5, 100)
        plt.plot(x, humidity2, color='r', label='湿度')
        plt.plot(x, temperature2, color='g', label='温度')
        humidity2 = []
        temperature2 = []
        plt.legend()  # 显示label
        plt.grid()
        if not is_close:
            plt.show()
        if is_close:
            plt.close()
            break
        plt.pause(2)
    plt.ioff()
    plt.show()

def clear_all_history():
    for i in range(2):
        with open('{}.txt'.format(i+1), 'a+') as f:
            f.seek(0)
            f.truncate()

def close_fig():
    plt.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow(1)
    ui.show()
    sys.exit(app.exec_())
