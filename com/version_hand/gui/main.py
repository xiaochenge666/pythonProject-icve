import sys
from com.version_hand.gui.ui.loginui import *
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyMain(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMain, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMain()
    myWin.show()
    sys.exit(app.exec_())
