from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout
import sys


class ToolsUi(QDialog):
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    # 一个控制接收窗口1，一个控制接收窗口2
    signal_write_msg1 = QtCore.pyqtSignal(str)
    signal_write_msg2 = QtCore.pyqtSignal(str)

    def __init__(self, num):
        """
        初始化窗口
        :param num: 计数窗口
        """
        super(ToolsUi, self).__init__()
        self.num = num
        self._translate = QtCore.QCoreApplication.translate

        self.setObjectName("TCP-UDP")
        self.resize(700, 480)
        self.setAcceptDrops(False)
        self.setSizeGripEnabled(False)
        self.setWindowIcon(QtGui.QIcon('controller.png'))

        # 定义控件
        self.label_None = QtWidgets.QLabel()
        self.label_warning = QtWidgets.QLabel()
        self.pushButton_link = QtWidgets.QPushButton()  # 连接按钮
        self.pushButton_unlink = QtWidgets.QPushButton()  # 断开连接按钮
        self.pushButton_clear = QtWidgets.QPushButton()  # 清除按钮
        self.pushButton_clear2 = QtWidgets.QPushButton()
        self.pushButton_clear_history = QtWidgets.QPushButton()
        self.pushButton_exit = QtWidgets.QPushButton()  # 退出按钮
        self.all_nodes_label = QtWidgets.QLabel()  # 发送按钮

        self.node1_label = QtWidgets.QLabel()
        self.pushButton_get_node1 = QtWidgets.QPushButton()
        self.pushButton_stop_node1 = QtWidgets.QPushButton()

        self.node2_label = QtWidgets.QLabel()
        self.pushButton_get_node2 = QtWidgets.QPushButton()
        self.pushButton_stop_node2 = QtWidgets.QPushButton()

        # 下面是自己加的按钮，试试功能
        self.pushButton_begin_data = QtWidgets.QPushButton()  # 开始按钮
        self.pushButton_stop_data = QtWidgets.QPushButton()  # 结束按钮

        self.label_port = QtWidgets.QLabel()
        self.label_ip = QtWidgets.QLabel()
        self.label_rev = QtWidgets.QLabel()
        self.label_rev2 = QtWidgets.QLabel()
        self.lineEdit_port = QtWidgets.QLineEdit()
        self.lineEdit_ip_local = QtWidgets.QLineEdit()  # 显示本地Ip的内容框
        # self.textEdit_send = QtWidgets.QTextEdit()   # 显示要发数据的内容框
        self.textBrowser_recv = QtWidgets.QTextBrowser()
        self.textBrowser_recv2 = QtWidgets.QTextBrowser()
        self.TCP_Server_Label = QtWidgets.QLabel()  # TCP Server文字

        # 定义布局
        self.h_header = QHBoxLayout()
        self.h_box_1 = QHBoxLayout()  # H是水平方向布局
        self.h_box_2 = QHBoxLayout()
        self.h_box_3 = QHBoxLayout()
        self.h_box_4 = QHBoxLayout()
        self.h_box_5 = QHBoxLayout()
        self.h_box_node1 = QHBoxLayout()
        self.h_box_node2 = QHBoxLayout()
        self.h_box_clear = QHBoxLayout()
        self.h_box_recv = QHBoxLayout()
        self.h_box_recv2 = QHBoxLayout()
        self.h_box_exit = QHBoxLayout()
        self.h_box_all = QHBoxLayout()
        self.v_box_set = QVBoxLayout()
        # self.v_box_send = QVBoxLayout()
        self.v_box_exit = QVBoxLayout()
        self.v_box_right = QVBoxLayout()
        self.v_box_left = QVBoxLayout()
        self.v_box_right_right = QVBoxLayout()

        # 设置字体
        font = QtGui.QFont()
        font.setFamily("Yuppy TC")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_rev.setFont(font)
        self.label_rev2.setFont(font)

        # 设置控件的初始属性
        self.pushButton_unlink.setEnabled(False)
        # self.textEdit_send.hide()
        # self.textBrowser_recv.insertPlainText("This is received window-NO.%s\n" % self.num)
        self.label_warning.setStyleSheet("color:red")

        # 调用布局方法和控件显示文字的方法
        self.layout_ui()
        self.ui_translate()
        self.connect()

    def layout_ui(self):
        """
        设置控件的布局
        :return:
        """
        # 左侧布局添加
        self.h_header.addWidget(self.label_warning)
        self.h_box_1.addWidget(self.label_ip)
        self.h_box_1.addWidget(self.lineEdit_ip_local)
        self.h_box_5.addWidget(self.label_port)
        self.h_box_5.addWidget(self.lineEdit_port)

        self.h_box_2.addWidget(self.TCP_Server_Label)
        self.h_box_2.addWidget(self.pushButton_link)
        self.h_box_2.addWidget(self.pushButton_unlink)

        self.h_box_3.addWidget(self.all_nodes_label)
        self.h_box_3.addWidget(self.pushButton_begin_data)
        self.h_box_3.addWidget(self.pushButton_stop_data)

        self.h_box_node1.addWidget(self.node1_label)
        self.h_box_node1.addWidget(self.pushButton_get_node1)
        self.h_box_node1.addWidget(self.pushButton_stop_node1)

        self.h_box_node2.addWidget(self.node2_label)
        self.h_box_node2.addWidget(self.pushButton_get_node2)
        self.h_box_node2.addWidget(self.pushButton_stop_node2)

        self.v_box_set.addLayout(self.h_header)
        self.v_box_set.addLayout(self.h_box_1)
        self.v_box_set.addLayout(self.h_box_5)
        self.v_box_set.addLayout(self.h_box_2)
        self.v_box_set.addWidget(self.label_None)
        self.v_box_set.addLayout(self.h_box_3)
        self.v_box_set.addLayout(self.h_box_node1)
        self.v_box_set.addLayout(self.h_box_node2)

        self.h_box_4.addWidget(self.pushButton_exit)
        self.h_box_4.addWidget(self.label_None)
        self.h_box_4.addWidget(self.label_None)
        self.h_box_clear.addWidget(self.pushButton_clear_history)
        self.h_box_clear.addWidget(self.label_None)
        self.h_box_clear.addWidget(self.label_None)
        self.v_box_exit.addLayout(self.h_box_clear)
        self.v_box_exit.addLayout(self.h_box_4)

        self.v_box_left.addLayout(self.v_box_set)
        self.v_box_left.addWidget(self.label_None)
        self.v_box_left.addWidget(self.label_None)
        self.v_box_left.addLayout(self.v_box_exit)


        # 右侧布局添加
        self.h_box_recv.addWidget(self.label_rev)
        self.h_box_recv.addWidget(self.pushButton_clear)
        self.v_box_right.addLayout(self.h_box_recv)
        self.v_box_right.addWidget(self.textBrowser_recv)

        # 右右侧布局
        self.h_box_recv2.addWidget(self.label_rev2)
        self.h_box_recv2.addWidget(self.pushButton_clear2)
        self.v_box_right_right.addLayout(self.h_box_recv2)
        self.v_box_right_right.addWidget(self.textBrowser_recv2)

        # 将左右布局添加到窗体布局
        self.h_box_all.addLayout(self.v_box_left)
        self.h_box_all.addLayout(self.v_box_right)
        self.h_box_all.addLayout(self.v_box_right_right)

        # 设置窗体布局到窗体
        self.setLayout(self.h_box_all)

    def ui_translate(self):
        """
        控件默认显示文字的设置
        :param : QDialog类创建的对象
        :return: None
        """
        # 设置各个控件显示的文字
        # 也可使用控件的setText()方法设置文字
        self.setWindowTitle("Controller")
        self.TCP_Server_Label.setText("")
        self.pushButton_link.setText('连接')  # self._translate("TCP-UDP", "连接"))
        self.pushButton_unlink.setText('断开')  # self._translate("TCP-UDP", "断开"))
        self.pushButton_clear.setText("清空窗口1")
        self.pushButton_clear2.setText("清空窗口2")
        self.all_nodes_label.setText("全部节点：")
        self.pushButton_exit.setText("退出")
        self.pushButton_begin_data.setText("全部接收")
        self.pushButton_stop_data.setText('全部停止')

        self.label_warning.setText('请先连接网关后再操作！')
        self.lineEdit_ip_local.setText('192.168.0.179')
        self.lineEdit_port.setText('6001')

        self.node1_label.setText("节点1：")
        self.pushButton_get_node1.setText("接收节点1")
        self.pushButton_stop_node1.setText("停止节点1")
        self.pushButton_clear_history.setText("清空接收历史")
        self.node2_label.setText("节点2：")
        self.pushButton_get_node2.setText("接收节点2")
        self.pushButton_stop_node2.setText("停止节点2")

        self.label_ip.setText("本机IP:")
        self.label_port.setText("端口号:")
        self.label_rev.setText("Node 1")
        self.label_rev2.setText("Node 2")

    def connect(self):
        """
        控件信号-槽的设置
        :param : QDialog类创建的对象
        :return: None
        """
        self.signal_write_msg1.connect(self.write_msg1)  # 通过connect函数连接信号(signal_write_msg)与槽(write_msg),槽相当于与信号绑定的函数
        self.signal_write_msg2.connect(self.write_msg2)

    def write_msg1(self, msg):
        # signal_write_msg1信号会触发这个函数(槽)
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：PyQt程序的子线程中，直接向主线程的界面传输字符是不符合安全原则的
        :return: None
        """
        self.textBrowser_recv.insertPlainText(msg)
        # 滚动条移动到结尾
        self.textBrowser_recv.moveCursor(QtGui.QTextCursor.End)

    def write_msg2(self, msg):
        # signal_write_msg1信号会触发这个函数(槽)
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：PyQt程序的子线程中，直接向主线程的界面传输字符是不符合安全原则的
        :return: None
        """
        self.textBrowser_recv2.insertPlainText(msg)
        # 滚动条移动到结尾
        self.textBrowser_recv2.moveCursor(QtGui.QTextCursor.End)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        self.close_all()

    def close_all(self):
        pass


if __name__ == '__main__':
    """
    显示界面
    """
    app = QApplication(sys.argv)
    ui = ToolsUi(1)
    ui.show()
    sys.exit(app.exec_())
