from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTableWidget, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QImage, QPixmap, QIcon
import sys
import socket
import threading
import scan_device_ui


class signal(QObject):
    # 自定义一个信号
    signal = pyqtSignal(str)

    # 定义一个发送信号的函数
    def emit(self, text):
        self.signal.emit(text)

class QDeviceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = ui = scan_device_ui.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("海帆-设备配置助手 V1.0")
        self.ui.scan_device.clicked.connect(self.scan_device)
        self.ui.reset_ip.clicked.connect(self.reset_ip_info)
        self.ui.reboot_device.clicked.connect(self.reboot_device)
        self.ui.exec_remote_cmd.clicked.connect(self.exec_remote_cmd)

        self.MULTICAST_ANY = "0.0.0.0"
        self.MULTICAST_IP = "239.255.255.250"
        self.MULTICAST_PORT = 35880

        self.update_ui = signal()
        self.update_ui.signal.connect(self.update_list_ui)

        self.start_listening()
        self.init_tables()
        self.count_index = 0
        self.list_content = []

    def init_tables(self):
        self.ui.device_list.setColumnCount(5)
        self.ui.device_list.setHorizontalHeaderLabels(['ID', 'MAC地址', 'IP地址', '子网掩码', '网关'])
        self.ui.device_list.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.ui.device_list.itemClicked.connect(self.table_item_click)
        pass

    def table_item_click(self, item):
        print("item click = ", item.row())
        content = self.list_content[item.row()]

        self.ui.et_mac.setText(content[1])
        self.ui.et_ip.setText(content[2])
        self.ui.et_mask.setText(content[3])
        self.ui.et_gateway.setText(content[4])

        pass

    def start_listening(self):
        # 创建UDP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # 允许端口复用
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定监听多播数据包的端口
        self.socket.bind((self.MULTICAST_ANY, self.MULTICAST_PORT))
        # 声明该socket为多播类型
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        # 加入多播组，组地址由第三个参数制定
        self.socket.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.MULTICAST_IP) + socket.inet_aton(self.MULTICAST_ANY)
        )
        self.socket.setblocking(False)

        self.receive_thread = threading.Thread(target=self.receive_message_worker, args=())
        self.receive_thread.start()
        pass

    def receive_message_worker(self):
        print("start recive message thread ...")
        while True:
            try:
                data, address = self.socket.recvfrom(2048)
            except Exception as e:
                # print(e)
                pass
            else:
                data = data.decode()
                print(data)
                self.update_ui.emit(data)
        pass

    def scan_device(self):
        print("scan device start ...")
        self.list_content = []
        self.count_index = 0
        self.ui.device_list.clearContents()

        self.socket.sendto("list".encode(), (self.MULTICAST_IP, self.MULTICAST_PORT))
        pass

    def update_list_ui(self, content):
        if content.startswith("client"):
            print("client = ", content)
            self.ui.device_list.setRowCount(self.count_index + 1)
            contents = content.split("-")
            item1 = QTableWidgetItem(str(self.count_index + 1))
            self.ui.device_list.setItem(self.count_index, 0, item1)
            item2 = QTableWidgetItem(contents[1])
            self.ui.device_list.setItem(self.count_index, 1, item2)
            item3 = QTableWidgetItem(contents[2])
            self.ui.device_list.setItem(self.count_index, 2, item3)
            if len(contents) > 3:
                item4 = QTableWidgetItem(contents[3])
                self.ui.device_list.setItem(self.count_index, 3, item4)
                item5 = QTableWidgetItem(contents[4])
                self.ui.device_list.setItem(self.count_index, 4, item5)
            self.count_index += 1

            self.list_content.append([str(self.count_index + 1), contents[1], contents[2], contents[3], contents[4]])
        if content.startswith("cmdstr"):
            content = content.split("#")[1]
            self.ui.et_cmd_result.setText(content)
        pass

    def reset_ip_info(self):
        mac = self.ui.et_mac.text()
        ip = self.ui.et_ip.text()
        mask = self.ui.et_mask.text()
        gateway = self.ui.et_gateway.text()
        cmd = "modifyip-{}-{}-{}-{}".format(mac, ip, mask, gateway)
        print("reset ip param = " + cmd)
        self.socket.sendto(cmd.encode(), (self.MULTICAST_IP, self.MULTICAST_PORT))
        pass

    def reboot_device(self):
        mac = self.ui.et_mac.text()
        cmd = "reboot-{}".format(mac)
        print("reset ip param = " + cmd)
        self.socket.sendto(cmd.encode(), (self.MULTICAST_IP, self.MULTICAST_PORT))

    def exec_remote_cmd(self):
        mac = self.ui.et_mac.text()
        cmdstr = self.ui.et_remote_cmd.text()
        cmd = "exec#{}#{}#".format(mac, cmdstr)
        print("reset ip param = " + cmd)
        self.socket.sendto(cmd.encode(), (self.MULTICAST_IP, self.MULTICAST_PORT))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QDeviceWidget()
    # w.setWindowState(Qt.WindowMaximized)
    w.show()
    sys.exit(app.exec_())