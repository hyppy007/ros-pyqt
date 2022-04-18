#!/usr/bin/env python3
# coding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import rospy
from geometry_msgs.msg import Twist
from math import radians, degrees
# turtlesim/Pose
from turtlesim.msg import Pose
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 创建自己的渲染定时器
        updatetimer = QTimer(self)
        # 设置定时器的频率
        updatetimer.setInterval(20)
        updatetimer.start()
        # 监听timer事件
        updatetimer.timeout.connect(self.on_update)

        # 设置title
        self.setWindowTitle("小乌龟控制")
        self.resize(400, 0)

        # 设置布局
        layout = QFormLayout()
        self.setLayout(layout)

        # 添加控件
        self.editLinear = QLineEdit("0")
        layout.addRow("线速度", self.editLinear)

        self.editAngular = QLineEdit("0")
        layout.addRow("角速度", self.editAngular)

        self.btnSend = QPushButton("发送")
        layout.addRow(self.btnSend)

        self.labelX = QLabel()
        layout.addRow("当前X坐标", self.labelX)

        self.labelY = QLabel()
        layout.addRow("当前Y坐标", self.labelY)

        self.labelLinear = QLabel()
        layout.addRow("当前线速度", self.labelLinear)

        self.labelAngular = QLabel()
        layout.addRow("当前角速度", self.labelAngular)

        self.labelDegrees = QLabel()
        layout.addRow("当前角度", self.labelDegrees)

        # 添加事件
        self.btnSend.clicked.connect(self.clickSend)

        # 创建publisher
        topicName = "/turtle1/cmd_vel"
        self.publisher = rospy.Publisher(topicName, Twist, queue_size=1000)

        # 接受小乌龟信息
        pose_name = '/turtle1/pose'
        rospy.Subscriber(pose_name,Pose,self.pose_call)

    def pose_call(self,msg):
        if not isinstance(msg,Pose): return
        print (msg)
        self.labelX.setText(str(msg.x))
        self.labelY.setText(str(msg.y))
        self.labelLinear.setText(str(msg.linear_velocity))
        self.labelAngular.setText(str(msg.angular_velocity))
        # 弧度转角度
        self.labelDegrees.setText(str(degrees(msg.theta)))
        # self.labelDegrees.setText(str(msg.theta))



    def clickSend(self):
        linearX = float(self.editLinear.text())
        # 角度转弧度
        angularZ = radians(float(self.editAngular.text()))

        # 构建消息
        twist = Twist()
        twist.linear.x = linearX
        twist.angular.z = angularZ
        # 发布
        self.publisher.publish(twist)

    def on_update(self):
        self.update()
        if rospy.is_shutdown():
            self.close()
