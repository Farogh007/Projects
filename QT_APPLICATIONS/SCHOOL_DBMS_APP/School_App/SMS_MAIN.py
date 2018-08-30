import urllib2
import cookielib
import sys
import os
import time
import sqlite3
from getpass import getpass
from stat import *
from PyQt4 import QtGui, QtCore, Qt
from SMS_ui import Ui_MainWindow_SMS
from PyQt4.QtGui import *

# function for calling Database
#con = sqlite3.connect("Database/2016/db_2016.sqlite")
#c = con.cursor()


class Gui(QtGui.QMainWindow):

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow_SMS()
		self.ui.setupUi(self)
		self.behaviour()
		pixmap = QPixmap('E:\My_Projects\Python projects\python+Database\School_App\School_App\image\SMS1.png')
		self.ui.label_PIC.setPixmap(pixmap)
		self.ui.label_PIC.show()

	def reset(self):
		self.ui.lineEdit_NUMBER.clear()
		self.ui.textEdit_MESSAGE.clear()
		self.ui.textBrowser_STATUS.clear()


	def send_sms(self):
		number = 0

		number = int(str(self.ui.lineEdit_NUMBER.text()))
		message = str(self.ui.textEdit_MESSAGE.toPlainText())
		
		
		if __name__ == "__main__":
			username = "yourusername"
			passwd = "passsword"

			message = "+".join(message.split(' '))

			#logging into the sms site
			url ='http://site24.way2sms.com/Login1.action?'
			data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
			
			#For cookies
			cj= cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

			#Adding header details
			opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
			
			try:
				usock =opener.open(url, data)
			except IOError:
				self.ui.textBrowser_STATUS.setText("N0 Internet !!")
				#return()
				
			jession_id =str(cj).split('~')[1].split(' ')[0]
			send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
			send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+str(number)+'&message='+message+'&msgLen=136'
			opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
			
			try:
				sms_sent_page = opener.open(send_sms_url,send_sms_data)
			except IOError:
				self.ui.textBrowser_STATUS.setText("Error !!")
				#return()
			self.ui.textBrowser_STATUS.setText("Message Send !!")
			#return ()
	
	def behaviour(self):
		self.connect(self.ui.pushButton_RESET, Qt.SIGNAL("clicked()"), self.reset)
		self.connect(self.ui.pushButton_SEND, Qt.SIGNAL("clicked()"), self.send_sms)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Gui()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()






message = raw_input("Enter text: ")
number = raw_input("Enter number: ")

if __name__ == "__main__":    
    username = "9525670530"
    passwd = "R3456N"

    message = "+".join(message.split(' '))

 #logging into the sms site
    url ='http://site24.way2sms.com/Login1.action?'
    data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

 #For cookies

    cj= cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

 #Adding header details
    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
    try:
        usock =opener.open(url, data)
    except IOError:
        print "error"
        #return()

    jession_id =str(cj).split('~')[1].split(' ')[0]
    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
    send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
    opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
    try:
        sms_sent_page = opener.open(send_sms_url,send_sms_data)
    except IOError:
        print "error"
        #return()

    print "success" 
    #return ()