#!/usr/bin/env python
# coding:utf-8
from PyQt5.QtWidgets import *
import sys
from turtle_again import MainWindow
from PyQt5.QtWidgets import *
import rospy


if __name__ == '__main__':
    # ROS
    nodeName = "turtle_ctr"
    rospy.init_node(nodeName)

    # Qt Gui部分
    app = QApplication(sys.argv)

    # 窗体显示
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())