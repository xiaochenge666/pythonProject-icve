import pygame
from PyQt5.QtCore import QThread, pyqtSignal
from com.version_hand.gui.zhijiaoui import *
from com.version_hand.gui.loginui import *
from com.version_hand.gui.tpis import *
from com.version_hand.tools.zhijiaoyun import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import *
import sys
import os


# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


filename = resource_path(os.path.join("img", "music.mp3"))

z = zhihui()  # 职教云对象


class FlashCourseThread(QThread):
    throwExceptionSg = pyqtSignal(str)

    def __init__(self):
        super(FlashCourseThread, self).__init__()
        self.cname = ''

    def setCname(self, cname):
        self.cname = cname

    def run(self):
        try:
            z.doFlashCourse(self.cname)
        except:
            self.throwExceptionSg.emit('出错了！！！')
            # exit(0)


class FlashDiyCourseThread(QThread):
    throwExceptionSg = pyqtSignal(str)

    def __init__(self):
        super(FlashDiyCourseThread, self).__init__()
        self.Cobj = {}

    def setCobj(self, cobj):
        self.Cobj = cobj

    def run(self):
        try:
            print(self.Cobj)
            z.doDiyFlashCourse(cname=self.Cobj['cname'], isWantFlCourse=self.Cobj['isFlc'], speed=self.Cobj['speed'],
                               isWantComment=
                               self.Cobj['isCm'], msg=self.Cobj['msg'])
        except:
            self.throwExceptionSg.emit('出错了！！！, 请稍后再试....')


t = FlashCourseThread()
td = FlashDiyCourseThread()


class Tips(QDialog, Ui_Dialog):
    def __init__(self):
        super(Tips, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

    def setText(self, msg):
        self.label.setText(msg)

    def closeWin(self):
        exec

    def setTextWarningColor(self, none):
        self.label.setStyleSheet('color:red')

    def setTextSuccessColor(self, none):
        self.label.setStyleSheet('color:green')


class MyLogin(QMainWindow, Ui_Form):
    loginSuc = pyqtSignal()
    tipsSg = pyqtSignal(str)
    showTipsSg = pyqtSignal()

    def __init__(self, parent=None):
        super(MyLogin, self).__init__(parent)
        self.setupUi(self)
        self.updateCode()
        self.setMyTheme()

    def setMyTheme(self):
        self.pushButton.setStyleSheet('background:rgba(100,100,100,0.3);color:green;border:none')
        self.label_2.setStyleSheet('background:rgba(105,105,105,0.0);')
        self.label.setStyleSheet('background:rgba(105,105,105,0.0);')
        self.label_5.setStyleSheet('background:rgba(105,105,105,0.0);')
        self.lineEdit_2.setStyleSheet('border:none')
        self.lineEdit_3.setStyleSheet('border:none')
        self.lineEdit.setStyleSheet('border:none')
        self.label.setGeometry(QtCore.QRect(68, 60, 61, 31))

    def updateCode(self):
        z.getVerificationCode()
        self.label_6.setPixmap(QPixmap('img/local.png'))

    def login(self):
        # 获取用户输入的对象
        user = self.lineEdit.text()
        pwd = self.lineEdit_2.text()
        # user = '1227947691'
        # pwd = 'zfz999107.'
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
        else:
            self.tipsSg.emit('你也太天真了吧！消息都不填完 ~ 人才')
            self.showTipsSg.emit()
            self.updateCode()

    def showTips(self, msg):

        tips.show()


class MyMain(QMainWindow, Ui_zhijiaoUi):
    setErrorMsgSg = pyqtSignal(str)
    setSuccessMsgSg = pyqtSignal(str)
    openTipsWinSg = pyqtSignal()

    def __init__(self, parent=None):
        super(MyMain, self).__init__(parent)
        self.setupUi(self)
        self.groupBox.setChecked(False)
        self.pushButton_start.setStyleSheet("color:green")
        self.groupBox.clicked.connect(self.fun1)
        self.checkBox_shuapinglun.clicked.connect(self.fun2)
        self.checkBox.clicked.connect(self.fun3)
        self.checkBox_diypinglun.clicked.connect(self.fun4)

        z.sendPer.connect(self.slotProcessBar)
        z.sendTotalCell.connect(self.slotSendTotalCell)
        z.sendCurrPage.connect(self.slotSendCurrPage)
        z.excepttionSg.connect(self.slotExceptTips)

        # self.setMyTheme()

    def setMyTheme(self):
        self.setStyleSheet('background:rgba(105,105,105,0.1);color:white')
        self.pushButton_start.setStyleSheet('border:none')

    def init(self):
        c, o = z.getLearnningCourseList()
        self.comboBox.addItems(c)

    def startFlush(self):
        # 按照默认方式刷 和 按照用户自定义
        cname = self.comboBox.currentText()
        if not self.groupBox.isChecked():
            t.setCname(cname)
            t.start()
            t.throwExceptionSg.connect(self.slotExceptTips)
        else:
            isFLC, isCm, isDiyCm, isSpd = self.getStatus()
            msg = ''
            if self.textEdit_pinlun.isEnabled():
                msg = self.textEdit_pinlun.toPlainText()
            speed = self.horizontalSlider.value()
            cobj = {
                'isFlc': isFLC,
                'isCm': isCm,
                'isDiyCm': isDiyCm,
                'isSpd': isSpd,
                'msg': msg,
                'speed': speed,
                'cname': cname
            }
            td.setCobj(cobj)
            td.start()
            td.throwExceptionSg.connect(self.slotExceptTips)
            pass
        if self.pushButton_start.text() == '开始':
            self.disableSomeTools()
        else:
            self.enableSomeTools()

    def disableSomeTools(self):
        self.comboBox.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.pushButton_start.setStyleSheet("color:red")
        self.pushButton_start.setText('运行中')

    def enableSomeTools(self):
        self.comboBox.setEnabled(True)
        self.pushButton_start.setEnabled(True)
        self.pushButton_start.setStyleSheet("color:green")
        self.pushButton_start.setText('开始')

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
        self.progressBar_total.setValue(value)
        if self.progressBar_total.value() == 100:
            self.enableSomeTools()
            self.setSuccessMsgSg.emit('恭喜~ 恭喜~ 该课件已顺利完成辣~ ^_~')
            self.openTipsWinSg.emit()

    def slotExceptTips(self, msg):
        msg = msg + '没办法，需要您在重新登陆一下。蟹蟹~'
        self.enableSomeTools()
        self.setErrorMsgSg.emit(msg)
        self.openTipsWinSg.emit()

    def slotClearComBox(self):
        self.comboBox.clear()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    LoginPage = MyLogin()
    MainPage = MyMain()
    tips = Tips()
    pygame.mixer.init()
    track = pygame.mixer.music.load(filename)
    print(filename)
    pygame.mixer.music.play(-1)

    # ···············登陆页面信号······················
    # 登陆失败
    LoginPage.tipsSg.connect(tips.setText)
    LoginPage.showTipsSg.connect(tips.show)
    # 登陆成功
    LoginPage.show()
    LoginPage.loginSuc.connect(MainPage.show)
    LoginPage.loginSuc.connect(MainPage.init)
    LoginPage.loginSuc.connect(LoginPage.hide)  # 隐藏登陆界面
    # ·······················································

    # ··················主页面信号····················
    MainPage.openTipsWinSg.connect(tips.show)  # 若有提示
    # 若出错
    MainPage.setErrorMsgSg.connect(MainPage.hide)
    MainPage.setErrorMsgSg.connect(tips.setText)
    MainPage.setErrorMsgSg.connect(tips.setTextWarningColor)
    MainPage.setErrorMsgSg.connect(LoginPage.show)
    MainPage.setErrorMsgSg.connect(MainPage.slotClearComBox)
    # 若成功
    MainPage.setSuccessMsgSg.connect(tips.setText)
    MainPage.setSuccessMsgSg.connect(tips.setTextSuccessColor)
    # ················································

    sys.exit(app.exec_())
