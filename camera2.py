# 导入需要的各个模块
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph as pg  # pyqtgraph是一个很好用的绘图模块

class Signal(QWidget):
    def __init__(self):
        super(Signal, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1200, 800)  # 设置GUI界面的大小
        self.setWindowTitle('signal_analysis')  # 界面窗口名称
        layout_chart = QtWidgets.QGridLayout()  # 表格布局
        self.setLayout(layout_chart)
        pg.setConfigOption('background', 'w')  # 把绘图控件的背景设置为白色，默认是黑色的
        self.pw = pg.PlotWidget()
        self.pw.showGrid(x=True, y=True)  # 绘图控件显示网格
        self.curve = self.pw.plot(pen='k')  # 画笔颜色设置
        layout_chart.addWidget(self.pw, 0, 0, 9, 10)  # 绘图控件在整个GUI界面上所占的区域设置，这里表示绘图控件在表格布局的第一行第一列，并且占据9行10列的区域

        bt1 = QPushButton('Button', self)  # 按钮控件
        layout_chart.addWidget(bt1, 10, 0, 1, 1)  # 按钮控件在表格布局中的第11行第1列，因为前面设置了绘图控件占9行，所以前面9行都是绘图控件，第10行空出来，不然图像和别的控件挨太近不好看
        text1_edit = QLineEdit("", self)  #  # 文本编辑框
        layout_chart.addWidget(text1_edit, 10, 1, 1, 2)  # 文本编辑框放在按钮旁边，占2列宽

if __name__ == "__main__":
    app=QApplication(sys.argv)
    pyShow = Signal()
    pyShow.show()
    sys.exit(app.exec_())