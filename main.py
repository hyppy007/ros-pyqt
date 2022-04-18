#!/usr/bin/env python
from scripts import camera4
from scripts.camera4 import *
import cv2
from PySide2.QtCore import QFile, QObject
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import *
import sys
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication, pyqtSignal, QPoint, QRect, QTimer

from camera_ros import *
from ui_help import ui_Help
from ui_camera import ui_Camera
from cProfile import label
from time import sleep
from PyQt5.QtWidgets import QStyleOption, QStyle, QFrame, QSpacerItem, QSizePolicy
from camera import ui_Camera_ros

class MainUi(QtWidgets.QMainWindow):
    windowMaximumed = pyqtSignal()
    windowNormaled = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.resize(1200, 700)
        self._padding = 5
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
         #初始化摄像头
        self.CAM_NUM = 0
        self.timer_camera = QTimer() #初始化定时器
        self.cap = cv2.VideoCapture()
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QHBoxLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格
        self.top_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QHBoxLayout()  # 创建上方部件的水平布局层
        self.top_widget.setLayout(self.top_layout)  # 设置上方部件布局为水平
        self.top_widget.setObjectName('top_widget')
        self.down_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.down_widget.setObjectName('down_widget')
        self.down_layout = QtWidgets.QGridLayout()
        self.down_widget.setLayout(self.down_layout)
        self.right_newsong_widget = QtWidgets.QWidget()
        self.right_newsong_widget.setObjectName('right_newsong_widget')
        self.right_newsong_layout = QtWidgets.QGridLayout()
        self.right_newsong_widget.setLayout(self.right_newsong_layout)
        self.right_recommend_widget = QtWidgets.QWidget()
        self.right_recommend_widget.setObjectName('right_recommend_widget')
        self.right_recommend_layout = QtWidgets.QGridLayout()
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.main_layout.addWidget(self.left_widget, 2, 0, 3, 12)

        self.main_layout.addWidget(self.right_widget, 15, 0, 6, 12)

        self.main_layout.addWidget(self.right_recommend_widget, 5, 0, 10, 12)

        self.main_layout.addWidget(self.top_widget, 0, 0, 2, 12)

        self.main_layout.addWidget(self.down_widget, 21, 0, 15, 6)

        self.main_layout.addWidget(self.right_newsong_widget, 21, 6, 15, 6)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.main_layout.setSpacing(20)
        # 左侧公司标志
        self.top_button = QtWidgets.QPushButton()
        self.top_button.setObjectName('top_button')
        self.top_button.setMaximumSize(100, 20)
        self.top_button.setMinimumSize(100, 20)
        self.top_button.setStyleSheet("QPushButton{border-image: url(images/zz.png)}")

        self.left_button_4 = QtWidgets.QPushButton()
        self.left_button_4.setObjectName('left_button_4')
        self.left_button_5 = QtWidgets.QPushButton()
        self.left_button_5.setObjectName('left_button_5')
        self.left_button_6 = QtWidgets.QPushButton()
        self.left_button_6.setObjectName('left_button_6')

        self.left_button_4.setMinimumSize(25, 25)
        self.left_button_4.setMaximumSize(25, 25)
        self.left_button_5.setMinimumSize(25, 25)
        self.left_button_5.setMaximumSize(25, 25)
        self.left_button_6.setMinimumSize(25, 25)
        self.left_button_6.setMaximumSize(25, 25)

        # 设置标题栏按钮样式
        self.left_button_4.setStyleSheet(
            '''QPushButton{border-image: url(images/mini.png)}
               QPushButton:hover{border-image: url(images/mini2.png)}
               QPushButton:pressed{border-image: url(images/mini.png)}
            ''')
        self.left_button_5.setStyleSheet(
            '''QPushButton{border-image: url(images/max.png)}
               QPushButton:hover{border-image: url(images/max2.png)}
               QPushButton:pressed{border-image:url(images/max.png)}
               ''')
        self.left_button_6.setStyleSheet(
            '''QPushButton{border-image: url(images/close.png)}
               QPushButton:hover{border-image: url(images/close2.png)}
               QPushButton:pressed{border-image: url(images/close.png)}''')
        self.top_layout.setSpacing(5)
        self.top_layout.addWidget(self.top_button, alignment=Qt.AlignLeft)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.left_button_4, alignment=Qt.AlignRight)
        self.top_layout.addWidget(self.left_button_5, alignment=Qt.AlignRight)
        self.top_layout.addWidget(self.left_button_6, alignment=Qt.AlignRight)

        self.left_label_1 = QtWidgets.QPushButton("About")
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.left_label_1.setFont(font)
        self.left_label_1.setObjectName('left_label')
        self.left_label_1.setStyleSheet(
            '''QPushButton{font-size:10pt; color: rgb(133,133,133); border: 0px; background-color: rgb(255,151,0)}
               QPushButton:hover{color: white; background-color: rgb(255,151,0)}
            ''')

        self.left_button_1 = QtWidgets.QPushButton("Process")
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.left_button_1.setFont(font)
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.setStyleSheet(
            '''QPushButton{font-size:10pt; color: rgb(133,133,133); border: 0px; background-color: rgb(255,151,0)}
               QPushButton:hover{color: white; background-color: rgb(255,151,0)}
            ''')

        self.left_button_2 = QtWidgets.QPushButton("Colourisation")
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.left_button_2.setFont(font)
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.setStyleSheet(
            '''QPushButton{font-size:10pt; color: rgb(133,133,133); border: 0px; background-color: rgb(255,151,0)}
               QPushButton:hover{color: white; background-color: rgb(255,151,0)}
            ''')

        self.left_button_3 = QtWidgets.QPushButton("3D view")
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.left_button_3.setFont(font)
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.setStyleSheet(
            '''QPushButton{font-size:10pt; color: rgb(133,133,133); border: 0px; background-color: rgb(255,151,0)}
               QPushButton:hover{color: white; background-color: rgb(255,151,0)}
            ''')
        self.left_layout.addWidget(self.left_button_1, alignment=Qt.AlignLeft)
        self.left_widget.setContentsMargins(30, 11, 15, 0)
        self.left_layout.addSpacing(15)
        self.left_layout.addWidget(self.left_button_2, alignment=Qt.AlignLeft)
        self.left_layout.addSpacing(15)
        self.left_layout.addWidget(self.left_button_3, alignment=Qt.AlignLeft)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.left_label_1, alignment=Qt.AlignRight)

        self.right_recommend_LineEdit = QtWidgets.QLineEdit()
        self.right_recommend_LineEdit.setStyleSheet("QLineEdit\n"
                                                    "{\n"
                                                    "    font-size:15pt;\n"
                                                    "    color: rgb(255,151,0);\n"
                                                    "    background-color: white;\n"
                                                    "    border-width: 2px;\n"
                                                    "    padding-top: 4px;\n"
                                                    "    padding-button: 4px;\n"
                                                    "    padding-left: 10px;\n"
                                                    "    padding-right: 10px;\n"

                                                    "    border-style: solid;\n"
                                                    "    border-color: rgb(255,151,0);\n"
                                                    "\n"
                                                    "\n"
                                                    "}")
        self.right_recommend_LineEdit.setAlignment(Qt.AlignCenter)
        self.right_recommend_LineEdit.setObjectName('right_LineEdit')
        self.main_layout.addWidget(self.right_recommend_LineEdit, 5, 0, 10, 12)
        self.right_recommend_LineEdit.setContentsMargins(15, 10, 15, 0)
        self.right_recommend_LineEdit.setMaximumSize(2200, 200)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_recommend_LineEdit.setFont(font)
        right_recommend_LineEdit2 = QtWidgets.QLineEdit(self.right_recommend_LineEdit)
        self.main_layout.addWidget(right_recommend_LineEdit2, 5, 0, 10, 12)
        right_recommend_LineEdit2.setContentsMargins(25, 20, 25, 10)
        right_recommend_LineEdit2.setMaximumSize(2200, 200)
        right_recommend_LineEdit2.setAlignment(Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(65)
        right_recommend_LineEdit2.setFont(font)
        right_recommend_LineEdit2.setText("Please Drag Images Here")
        right_recommend_LineEdit2.setStyleSheet("QLineEdit\n"
                                                "{\n"
                                                "    font-size:15pt;\n"
                                                "    color: rgb(255,151,0);\n"
                                                "    background-color: white;\n"
                                                "    border-width: 2px;\n"

                                                "    border-style: dashed;\n"
                                                "    border-color: rgb(255,151,0);\n"
                                                "\n"
                                                "\n"
                                                "}")

        self.recommend_button_1 = QtWidgets.QPushButton()
        self.recommend_button_1.setText("Run")  # 设按钮文本
        self.recommend_button_1.setObjectName('recommend_button_1')
        self.recommend_button_1.setMinimumSize(120, 120)
        self.recommend_button_1.setMaximumSize(120, 120)
        self.right_layout.addWidget(self.recommend_button_1, 0, 11, 5, 1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.recommend_button_1.setFont(font)
        self.recommend_button_1.setStyleSheet("QPushButton\n"
                                              "{\n"
                                              "    font-size:15pt;\n"
                                              "    color: white;\n"
                                              "    background-color: rgb(255,151,0)\n"
                                              "}")

        self.progressBar = QtWidgets.QProgressBar()
        self.right_layout.addWidget(self.progressBar, 0, 0, 5, 8)
        self.right_layout.setContentsMargins(15, 10, 15, 10)
        self.progressBar.setValue(0)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        label_progress = QtWidgets.QLabel(self.progressBar)
        label_progress.setText("0/4")
        self.right_layout.addWidget(label_progress, 2, 7, 1, 1)

        label_progress.setFont(font)
        label_progress.setStyleSheet("QLabel\n"
                                     "{\n"
                                     "    font-size:15pt;\n"
                                     "    color: white;\n"
                                     "    background-color: rgb(255,157,15)\n"

                                     "}")

        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar\n"
                                       "{\n"
                                       "    text-align: center;\n"
                                       "    font-size: 15pt;\n"
                                       "    color: white;\n"
                                       "    background-color: white;\n"
                                       "    border-image: url(images/progress.png)}"
                                       "    border-width: 5px;\n"
                                       "    border-style: solid;\n"
                                       "    border-color: white;\n"
                                       "\n"
                                       "\n"
                                       "}")
        self.progressBar.setMaximumSize(2000, 120)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_recommend_LineEdit.setFont(font)

        self.pushButton_5 = QtWidgets.QPushButton()
        self.pushButton_5.setObjectName("pushButton_5")
        self.main_layout.addWidget(self.pushButton_5, 24, 5, 3, 3, QtCore.Qt.AlignCenter)
        self.pushButton_5.setStyleSheet("QPushButton{border-image: url(images/logo.png)}")
        self.pushButton_5.setMaximumSize(200, 200)
        self.pushButton_5.setMinimumSize(200, 200)

        down_LineEdit = QtWidgets.QLineEdit(self.main_widget)
        self.main_layout.addWidget(down_LineEdit, 20, 0, 15, 12)
        down_LineEdit.setContentsMargins(20, 0, 20, 20)
        down_LineEdit.setMaximumSize(4000, 300)
        down_LineEdit.setStyleSheet('''
                background:rgb(255,0,0,0);
                border-width: 10px;
                border-style: solid;
                border-color: rgb(43, 43, 43)
                ''')
        down_LineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        down_LineEdit.setEnabled(False)

        # 左下的部件
        self.down_widget.setContentsMargins(40, 50, 20, 70)
        self.label_3 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QLabel\n"
                                   "{\n"
                                   "    background:rgb(255,0,0,0);\n"
                                   "    color: white;\n"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.main_layout.addWidget(self.label_3, 24, 1, 1, 1)
        self.label_3.setText("Dataset")
        self.label_3.setContentsMargins(40, 0, 20, 0)
        self.lineEdit = QtWidgets.QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.main_layout.addWidget(self.lineEdit, 24, 2, 1, 1)
        self.lineEdit.setContentsMargins(0, 0, 10, 0)
        self.lineEdit.setStyleSheet("QLineEdit\n"
                                    "{\n"
                                    "    color: black;\n"
                                    "    background-color: white;\n"
                                    "\n"
                                    "\n"
                                    "}")
        self.lineEdit.setText("D:\\document/ZZCOMM")
        self.label_2 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel\n"
                                   "{\n"
                                   "    color: white;\n"
                                   "    background:rgb(255,0,0,0);\n"
                                   "}")
        self.label_2.setObjectName("label_2")
        self.main_layout.addWidget(self.label_2, 25, 1, 1, 1)
        self.label_2.setText("Dataset")
        self.label_2.setContentsMargins(40, 0, 20, 0)
        self.pushButton_2 = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton\n"
                                        "{\n"
                                        "    color: white;\n"
                                        "    background-color: rgb(255,151,0)\n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.main_layout.addWidget(self.pushButton_2, 24, 4, 1, 1, QtCore.Qt.AlignLeft)
        self.pushButton_2.setText("Open")

        self.lineEdit_2 = QtWidgets.QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.main_layout.addWidget(self.lineEdit_2, 25, 2, 1, 1)
        self.lineEdit_2.setContentsMargins(0, 0, 10, 0)
        self.lineEdit_2.setStyleSheet("QLineEdit\n"
                                      "{\n"
                                      "    color: black;\n"
                                      "    background-color: white;\n"
                                      "\n"
                                      "\n"
                                      "}")
        self.lineEdit_2.setText("D:\\document/ZZCOMM")
        self.pushButton_3 = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton\n"
                                        "{\n"
                                        "    color: white;\n"
                                        "    background-color: rgb(255,151,0)\n"
                                        "}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.main_layout.addWidget(self.pushButton_3, 25, 4, 1, 1, QtCore.Qt.AlignLeft)
        self.pushButton_3.setText("Open")

        self.lineEdit_3 = QtWidgets.QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.main_layout.addWidget(self.lineEdit_3, 26, 2, 1, 1, )
        self.lineEdit_3.setContentsMargins(0, 0, 10, 0)
        self.lineEdit_3.setStyleSheet("QLineEdit\n"
                                      "{\n"
                                      "    color: black;\n"
                                      "    background-color: white;\n"
                                      "\n"
                                      "\n"
                                      "}")
        self.lineEdit_3.setText("D:\\document/ZZCOMM")
        self.pushButton = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton\n"
                                      "{\n"
                                      "    color: white;\n"
                                      "    background-color: rgb(255,151,0)\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.main_layout.addWidget(self.pushButton, 26, 4, 1, 1, QtCore.Qt.AlignLeft)
        self.pushButton.setText("Open")

        self.label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel\n"
                                 "{\n"
                                 "    color: white;\n"
                                 "    background:rgb(255,0,0,0);\n"
                                 "}")
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.main_layout.addWidget(self.label, 26, 1, 1, 1)
        self.label.setText("Dataset")
        self.label.setContentsMargins(40, 0, 20, 0)
        self.main_layout.setColumnStretch(2, 3)
        self.main_layout.setColumnStretch(5, 3)
        self.top_widget.setStyleSheet('''
        background: white;

        ''')

        self.down_widget.setStyleSheet('''
        background: rgba(64,64,64);

        ''')

        self.left_widget.setStyleSheet('''
        background: rgba(255,151,0);


        }

        ''')

        self.right_widget.setStyleSheet('''
        background: rgba(64,64,64);

        ''')

        self.right_recommend_widget.setStyleSheet('''
        font-size:15pt;                                                 
        color: rgb(255,151,0);
        background-color: rgb(64,64,64);


        ''')

        self.right_newsong_widget.setStyleSheet('''
        background: rgba(64,64,64);


        ''')
        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_layout.setSpacing(0)

        self.left_button_4.clicked.connect(self.showMinimized)
        self.left_button_5.clicked.connect(self.slot_max_or_recv)
        self.left_button_6.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.open)
        self.pushButton_2.clicked.connect(self.ui)
        self.recommend_button_1.clicked.connect(self.help)
        self.left_button_2.clicked.connect(self.camera2)
        self.left_button_3.clicked.connect(self.camera_ros)
        self.pushButton_3.clicked.connect(self.open_new_window)

        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.main_layout.setContentsMargins(0, 0, 0, 0)


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mflag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def slot_max_or_recv(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.down_widget.x() + 10, self.down_widget.y() + 10, 100, 100)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))
        painter.drawRect(rect)

    def open(self):
        import rqt
        self.one = rqt.MainWindow()
        self.one.show()

    def camera2(self):
        import camera2
        self.two = camera2.Signal()
        self.two.show()

    def ui(self):
        self.form2 = QtWidgets.QWidget()
        self.ui2 = Form()
        self.ui2.setupUi(self.form2)
        self.forme2.show()


    def camera_ros(self):
        stats = ui_Camera()
        stats.ui.show()
        #self.ui.close()


    def help(self):
        stats = ui_Help()
        stats.ui.show()
        #self.ui.close()
        app.exec_()

    def open_new_window(self):
        # 实例化另外一个窗口
        self.window2 = Window2()
        # 显示新窗口
        self.window2.show()
        # 关闭自己
        self.hide()

class Window2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('窗口2')
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        button = QtWidgets.QPushButton('按钮2')
        grid = QtWidgets.QGridLayout(centralWidget)
        grid.addWidget(button)

def main():
    app = QtWidgets.QApplication(sys.argv)

    gui = MainUi()
    print(gui.right_recommend_LineEdit.frameGeometry())
    print(gui.label.getContentsMargins())
    print(gui.down_widget.frameGeometry())

    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
