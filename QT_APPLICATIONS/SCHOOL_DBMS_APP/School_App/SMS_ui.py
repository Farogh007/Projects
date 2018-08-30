# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SMS.ui'
#
# Created: Fri Jul 01 18:15:26 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow_SMS(object):
    def setupUi(self, MainWindow_SMS):
        MainWindow_SMS.setObjectName(_fromUtf8("MainWindow_SMS"))
        MainWindow_SMS.resize(487, 312)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("C:/Users/farogh94/Desktop/sms-alt-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow_SMS.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow_SMS)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 10, 241, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 70, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_NUMBER = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_NUMBER.setGeometry(QtCore.QRect(280, 70, 201, 20))
        self.lineEdit_NUMBER.setObjectName(_fromUtf8("lineEdit_NUMBER"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 110, 71, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_PIC = QtGui.QLabel(self.centralwidget)
        self.label_PIC.setGeometry(QtCore.QRect(20, 80, 141, 141))
        self.label_PIC.setText(_fromUtf8(""))
        self.label_PIC.setObjectName(_fromUtf8("label_PIC"))
        self.pushButton_SEND = QtGui.QPushButton(self.centralwidget)
        self.pushButton_SEND.setGeometry(QtCore.QRect(300, 270, 75, 31))
        self.pushButton_SEND.setObjectName(_fromUtf8("pushButton_SEND"))
        self.pushButton_RESET = QtGui.QPushButton(self.centralwidget)
        self.pushButton_RESET.setGeometry(QtCore.QRect(390, 270, 75, 31))
        self.pushButton_RESET.setObjectName(_fromUtf8("pushButton_RESET"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 280, 61, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.textBrowser_STATUS = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser_STATUS.setGeometry(QtCore.QRect(90, 270, 171, 31))
        self.textBrowser_STATUS.setObjectName(_fromUtf8("textBrowser_STATUS"))
        self.textEdit_MESSAGE = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_MESSAGE.setGeometry(QtCore.QRect(280, 110, 201, 141))
        self.textEdit_MESSAGE.setObjectName(_fromUtf8("textEdit_MESSAGE"))
        MainWindow_SMS.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow_SMS)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_SMS)

    def retranslateUi(self, MainWindow_SMS):
        MainWindow_SMS.setWindowTitle(_translate("MainWindow_SMS", "SMS", None))
        self.label.setText(_translate("MainWindow_SMS", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#00007f;\">SEND UNLIMITTED SMS</span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindow_SMS", "<html><head/><body><p><span style=\" font-size:10pt; color:#005500;\">Number :</span></p></body></html>", None))
        self.label_3.setText(_translate("MainWindow_SMS", "<html><head/><body><p><span style=\" font-size:10pt; color:#005500;\">Message :</span></p></body></html>", None))
        self.pushButton_SEND.setText(_translate("MainWindow_SMS", "SEND", None))
        self.pushButton_RESET.setText(_translate("MainWindow_SMS", "RESET", None))
        self.label_4.setText(_translate("MainWindow_SMS", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">STATUS :</span></p></body></html>", None))

