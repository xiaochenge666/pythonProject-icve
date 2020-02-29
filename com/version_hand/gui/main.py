import sys

from PyQt5.QtCore import QThread, pyqtSignal
from com.version_hand.gui.zhijiaoui import *
from com.version_hand.gui.loginui import *
from com.version_hand.gui.tpis import *
from com.version_hand.tools.zhijiaoyun import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import *

z = zhihui()  # 职教云对象


class FlashCourseThread(QThread):

    def __init__(self):
        super(FlashCourseThread, self).__init__()
        self.cname = ''

    def setCname(self, cname):
        self.cname = cname

    def run(self):
        z.doFlashCourse(self.cname)


t = FlashCourseThread()


class Tips(QDialog, Ui_Dialog):
    def __init__(self):
        super(Tips, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

    def setText(self, msg):
        self.label.setText(msg)

    def closeWin(self):
        exec


class MyMain(QMainWindow, Ui_zhijiaoUi):
    # openTipsSg = pyqtSignal(str)
    # openTipsWinSg = pyqtSignal()

    def __init__(self, parent=None):
        super(MyMain, self).__init__(parent)
        self.setupUi(self)
        self.groupBox.clicked.connect(self.fun1)
        self.checkBox_shuapinglun.clicked.connect(self.fun2)
        self.checkBox.clicked.connect(self.fun3)
        self.checkBox_diypinglun.clicked.connect(self.fun4)
        z.sendPer.connect(self.slotProcessBar)
        z.sendTotalCell.connect(self.slotSendTotalCell)
        z.sendCurrPage.connect(self.slotSendCurrPage)
        # z.excepttionSg.connect(self.slotExceptTips)


    def init(self):
        c, o = z.getLearnningCourseList()
        self.comboBox.addItems(c)

    def startFlush(self):
        # 按照默认方式刷 和 按照用户自定义
        cname = self.comboBox.currentText()
        if not self.groupBox.isChecked():
            t.setCname(cname)
            t.start()
        else:

            isFLC, isCm, isDiyCm, isSpd = self.getStatus()
            msg = ''
            if self.textEdit_pinlun.isEnabled():
                msg = self.textEdit_pinlun.toPlainText()
                speed = self.horizontalSlider.value()

                print(msg, speed)

            # z.doDiyFlashCourse(cname, isFLC, isSpd, isCm, msg)

            pass

    def getStatus(self):
        isFlC = self.checkBox_shuake.isChecked()
        isCm = self.checkBox_shuapinglun.isChecked()
        isDiyCm = self.checkBox_diypinglun.isChecked()
        isSpeed = self.checkBox.isChecked()
        return isFlC, isCm, isDiyCm, isSpeed

    def slotProcessBar(self, per):
        self.progressBar_total_2.setValue(per)

    def slotSendTotalCell(self, total):
        self.progressBar_total.setRange(0, total)

    def slotSendCurrPage(self, value):
        print(value)
        self.progressBar_total.setValue(value)

    def slotExceptTips(self, msg):
        print(msg)



    def fun1(self):
        if self.groupBox.isChecked():
            self.checkBox_shuake.setEnabled(True)
            self.checkBox_shuake.setChecked(True)
            self.checkBox_shuapinglun.setEnabled(True)
            self.checkBox_diypinglun.setEnabled(False)
            self.checkBox_shuapinglun.setChecked(False)
            self.checkBox.setEnabled(True)
            self.checkBox.setChecked(False)
            self.horizontalSlider.setEnabled(False)
        else:
            self.checkBox_shuake.setEnabled(False)
            self.checkBox_shuapinglun.setEnabled(False)
            self.checkBox_diypinglun.setEnabled(False)
            self.checkBox_diypinglun.setChecked(False)
            self.checkBox.setEnabled(False)
            self.textEdit_pinlun.setEnabled(False)
            self.horizontalSlider.setEnabled(False)

    def fun2(self):
        # 处理复选框和刷课
        if self.checkBox_shuapinglun.isChecked():
            self.checkBox_diypinglun.setEnabled(True)
        else:
            self.checkBox_diypinglun.setEnabled(False)
            self.textEdit_pinlun.setEnabled(False)

    def fun3(self):
        # 处理复选框与刷课速度进度条
        if self.checkBox.isChecked():
            self.horizontalSlider.setEnabled(True)
        else:
            self.horizontalSlider.setEnabled(False)

    def fun4(self):
        # 处理自定义评论和文本编辑框
        if self.checkBox_diypinglun.isChecked():
            self.textEdit_pinlun.setEnabled(True)
        else:
            self.textEdit_pinlun.setEnabled(False)


class Mylogin(QMainWindow, Ui_Form):
    loginSuc = pyqtSignal()
    tipsSg = pyqtSignal(str)
    showTipsSg = pyqtSignal()

    def __init__(self, parent=None):
        super(Mylogin, self).__init__(parent)
        self.setupUi(self)
        self.updateCode()
        print(z)

    def updateCode(self):
        z.getVerificationCode()
        self.label_6.setPixmap(QPixmap('img/local.png'))

    def login(self):
        # 获取用户输入的对象
        # user = self.lineEdit.text()
        # pwd = self.lineEdit_2.text()
        user = '1227947691'
        pwd = 'zfz999107.'
        vcode = self.lineEdit_3.text()
        if user and pwd and vcode:
            code = z.login(user, pwd, vcode)
            if code == 1:
                self.loginSuc.emit()
            else:
                if code == -16:
                    self.tipsSg.emit("oh 天！验证码错误都能输错！")
                elif code == -2:
                    self.tipsSg.emit("恭喜泥~ 密码不对，请重试~")
                else:
                    self.tipsSg.emit("哇塞！好厉害连小陈鸽都有找到的bug，你居然找到了，快去Ta面前炫耀一番吧~")
                self.showTipsSg.emit()
                self.updateCode()

    def showTips(self, msg):

        tips.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Mylogin()
    main = MyMain()
    tips = Tips()
    # main.openTipsSg.connect(tips.setText)
    # main.openTipsWinSg.connect(tips.show)
    myWin.tipsSg.connect(tips.setText)
    myWin.showTipsSg.connect(tips.show)
    myWin.show()
    myWin.loginSuc.connect(main.show)
    myWin.loginSuc.connect(main.init)
    myWin.loginSuc.connect(myWin.hide)  # 隐藏登陆界面
    sys.exit(app.exec_())
