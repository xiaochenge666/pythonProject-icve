# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zhijiaoui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from com.version_hand.gui import index_rc

class Ui_zhijiaoUi(object):
    def setupUi(self, zhijiaoUi):
        zhijiaoUi.setObjectName("zhijiaoUi")
        zhijiaoUi.resize(614, 405)
        zhijiaoUi.setMaximumSize(QtCore.QSize(614, 405))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        zhijiaoUi.setWindowIcon(icon)
        zhijiaoUi.setWindowOpacity(0.7)
        zhijiaoUi.setStyleSheet("background:")
        self.centralwidget = QtWidgets.QWidget(zhijiaoUi)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 110, 581, 201))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("")
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(True)
        self.groupBox.setObjectName("groupBox")
        self.checkBox_shuake = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_shuake.setGeometry(QtCore.QRect(20, 29, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_shuake.setFont(font)
        self.checkBox_shuake.setStyleSheet("")
        self.checkBox_shuake.setChecked(True)
        self.checkBox_shuake.setObjectName("checkBox_shuake")
        self.checkBox_shuapinglun = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_shuapinglun.setGeometry(QtCore.QRect(100, 29, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_shuapinglun.setFont(font)
        self.checkBox_shuapinglun.setStyleSheet("")
        self.checkBox_shuapinglun.setObjectName("checkBox_shuapinglun")
        self.checkBox_diypinglun = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_diypinglun.setGeometry(QtCore.QRect(20, 64, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_diypinglun.setFont(font)
        self.checkBox_diypinglun.setStyleSheet("")
        self.checkBox_diypinglun.setObjectName("checkBox_diypinglun")
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(20, 45, 541, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.line.setFont(font)
        self.line.setStyleSheet("")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.textEdit_pinlun = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_pinlun.setEnabled(True)
        self.textEdit_pinlun.setGeometry(QtCore.QRect(20, 90, 541, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.textEdit_pinlun.setFont(font)
        self.textEdit_pinlun.setStyleSheet("background:rgba(100,100,100,0.2);border:none;color:green")
        self.textEdit_pinlun.setObjectName("textEdit_pinlun")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox)
        self.horizontalSlider.setGeometry(QtCore.QRect(123, 167, 431, 22))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.horizontalSlider.setFont(font)
        self.horizontalSlider.setStyleSheet("")
        self.horizontalSlider.setMaximum(11)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setSliderPosition(11)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(True)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.line_2 = QtWidgets.QFrame(self.groupBox)
        self.line_2.setGeometry(QtCore.QRect(20, 150, 541, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(20, 170, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setStyleSheet("")
        self.checkBox.setObjectName("checkBox")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(108, 50, 361, 35))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox.setStyleSheet("")
        self.comboBox.setEditable(False)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(491, 50, 75, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setStyleSheet("background:rgba(100,100,100,0.2);border:none;color:green")
        self.pushButton_start.setObjectName("pushButton_start")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 50, 61, 35))
        font = QtGui.QFont()
        font.setFamily("MingLiU-ExtB")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 360, 571, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.progressBar_total_2 = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar_total_2.setStyleSheet("QProgressBar { \n"
"    border: 2px solid grey;   \n"
"    border-radius: 5px;   \n"
"    background-color: #FFFFFF;\n"
"}\n"
"QProgressBar::chunk {   \n"
"background-color:#48D1CC;  \n"
"width: 20px;\n"
"}\n"
"QProgressBar {  \n"
"border: 2px solid grey;   \n"
"border-radius: 5px;   \n"
"text-align: center;\n"
"}")
        self.progressBar_total_2.setProperty("value", 24)
        self.progressBar_total_2.setObjectName("progressBar_total_2")
        self.horizontalLayout_2.addWidget(self.progressBar_total_2)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 330, 571, 26))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.progressBar_total = QtWidgets.QProgressBar(self.layoutWidget1)
        self.progressBar_total.setStyleSheet("QProgressBar { \n"
"    border: 2px solid grey;   \n"
"    border-radius: 5px;   \n"
"    background-color: #FFFFFF;\n"
"}\n"
"QProgressBar::chunk {   \n"
"background-color: #05B8CC;   \n"
"width: 20px;\n"
"}\n"
"QProgressBar {  \n"
"border: 2px solid grey;   \n"
"border-radius: 5px;   \n"
"text-align: center;\n"
"}")
        self.progressBar_total.setProperty("value", 24)
        self.progressBar_total.setObjectName("progressBar_total")
        self.horizontalLayout.addWidget(self.progressBar_total)
        zhijiaoUi.setCentralWidget(self.centralwidget)

        self.retranslateUi(zhijiaoUi)
        self.comboBox.setCurrentIndex(-1)
        self.pushButton_start.clicked.connect(zhijiaoUi.startFlush)
        QtCore.QMetaObject.connectSlotsByName(zhijiaoUi)

    def retranslateUi(self, zhijiaoUi):
        _translate = QtCore.QCoreApplication.translate
        zhijiaoUi.setWindowTitle(_translate("zhijiaoUi", "小陈鸽网课小助手QQ1430986978"))
        self.groupBox.setTitle(_translate("zhijiaoUi", "高级设置"))
        self.checkBox_shuake.setText(_translate("zhijiaoUi", "刷课"))
        self.checkBox_shuapinglun.setText(_translate("zhijiaoUi", "刷评论"))
        self.checkBox_diypinglun.setText(_translate("zhijiaoUi", "自定义评论内容"))
        self.checkBox.setStatusTip(_translate("zhijiaoUi", "最大11，默认1"))
        self.checkBox.setWhatsThis(_translate("zhijiaoUi", "最大11，默认1"))
        self.checkBox.setAccessibleName(_translate("zhijiaoUi", "最大11，默认1"))
        self.checkBox.setText(_translate("zhijiaoUi", "刷课速度"))
        self.pushButton_start.setText(_translate("zhijiaoUi", "开始"))
        self.label.setText(_translate("zhijiaoUi", "课程名："))
        self.label_3.setText(_translate("zhijiaoUi", "当前课件："))
        self.label_2.setText(_translate("zhijiaoUi", "当前课程总进度："))
