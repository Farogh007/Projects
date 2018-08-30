import sys
import os
import cv2
import time
import sqlite3
from PyQt4 import QtGui, QtCore, Qt
from START_ui import Ui_MainWindow_START
import subprocess
import numpy as np
import urllib2
import cookielib
import SessionManager as SessionManager
from PyQt4.QtGui import *
import itertools 


# function for calling time function
localtime = time.asctime( time.localtime(time.time()))

# function for calling Database
con = sqlite3.connect("Database/2016/db_2016.sqlite")
c = con.cursor()


# Fuction for Streaming Video
class Video():
    def __init__(self,capture):
        self.capture = capture
        self.currentFrame=np.array([])
 
    def captureNextFrame(self):
        """                           
        capture frame and reverse RBG BGR and return opencv image                                      
        """
        ret, readFrame=self.capture.read()
        if(ret==True):
            self.currentFrame=cv2.cvtColor(readFrame,cv2.COLOR_BGR2RGB)
 
    def convertFrame(self):
        """     converts frame to format suitable for QtGui            """
        try:
            height,width=self.currentFrame.shape[:2]
            img=QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            img=QtGui.QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None



# function to covert bgr to grb.
def bgr2rgb(bgrImage):
		# Loading b g r components
		b,g,r = cv2.split(bgrImage)
		# Converting to RGB
		return cv2.merge([r,g,b])


# Main Programe of User Interface starts from here...
class Gui(QtGui.QMainWindow):

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow_START()
		self.ui.setupUi(self)
		self.output = ""
		self.application = ""
		self.behaviour()			 # calling behaviour on startup.
		self.Show_FeeStructure()     # calling Show fee Function on startup.
		self.video = Video(cv2.VideoCapture(0))
		self._timer = QtCore.QTimer(self)
		self._timer.timeout.connect(self.play)
		self._timer.start(27)
		self.session = SessionManager.configuration()
		self.imageName = "C:\\test.jpg"
		self.recent = "C:\\test.jpg"
		self.filename = ""
		self.extension = ""
		self.inputMode = "INPUT"
		self.outputMode = "OUTPUT"


	# Function for calling sms window
	def sms(self):
		self.executeScript("SMS_MAIN.py")

	def executeScript(self, parameter):
		parameter = "python " + parameter + " 1"
		subprocess.call(parameter)

	# FUnction to Show Fee.
	def Show_FeeStructure(self):
		for row in c.execute('SELECT * FROM Show_Fee '):
			self.ui.textBrowser_KG1_41.setText(str(row[1]))
			self.ui.textBrowser_KG2_41.setText(str(row[2]))
			self.ui.textBrowser_ONE_41.setText(str(row[3]))
			self.ui.textBrowser_TWO_41.setText(str(row[4]))
			self.ui.textBrowser_THREE_41.setText(str(row[5]))
			self.ui.textBrowser_FOUR_41.setText(str(row[6]))
			self.ui.textBrowser_FIVE_41.setText(str(row[7]))
			self.ui.textBrowser_SIX_41.setText(str(row[8]))
			self.ui.textBrowser_SEVEN_41.setText(str(row[9]))
			self.ui.textBrowser_EIGHT_41.setText(str(row[10]))
			self.ui.textBrowser_NINE_41.setText(str(row[11]))
			self.ui.textBrowser_TEN_41.setText(str(row[12]))

	# Fuction for TAB_WIDGET 1 Starts from here..
	def reset_page1(self):
		self.ui.lineEdit_ID_1.clear()
		self.ui.textBrowser_NAME.clear()
		self.ui.textBrowser_CLASS.clear()
		self.ui.textBrowser_ROLL.clear()
		self.ui.textBrowser_AYEAR.clear()
		self.ui.textBrowser_FATHER.clear()
		self.ui.textBrowser_MOTHER.clear()
		self.ui.textBrowser_MOBILE.clear()
		self.ui.textBrowser_ADDRESS.clear()
		self.ui.textBrowser_STATUS_1.clear()
		self.ui.label_PHOTO.clear()

	# Function for Searching ID From DataBase.
	def query_page1(self):
		SORT = 0
		SORT = int(str(self.ui.lineEdit_ID_1.text()))

		for row in c.execute('SELECT * FROM student_detail WHERE ID = ?', (SORT, )):
			self.ui.textBrowser_NAME.setText(row[1])
			self.ui.textBrowser_CLASS.setText(row[2])
			self.ui.textBrowser_ROLL.setText(str(row[3]))
			self.ui.textBrowser_AYEAR.setText(str(row[4]))
			self.ui.textBrowser_FATHER.setText(row[5])
			self.ui.textBrowser_MOTHER.setText(row[6])
			self.ui.textBrowser_MOBILE.setText(str(row[7]))
			self.ui.textBrowser_ADDRESS.setText(row[8])
			self.ui.textBrowser_STATUS_1.setText("Record Found !!")

		# selecting an image using id and displaying same image on Qlabel.
		for row in c.execute('SELECT * FROM image WHERE ID = ?', (SORT, )):
			pixmap = QPixmap(row[2])
			self.ui.label_PHOTO.setPixmap(pixmap)
			self.ui.label_PHOTO.show()

		# displaying data for attaindance table
		
		
		
	# Fuction for TAB_WIDGET 2 Starts from here..
	def reset_page2(self):
		self.ui.lineEdit_NAME_2.clear()
		self.ui.lineEdit_CLASS_2.clear()
		self.ui.lineEdit_ROLL_2.clear()
		self.ui.lineEdit_AYEAR_2.clear()
		self.ui.lineEdit_FATHER_2.clear()
		self.ui.lineEdit_MOTHER_2.clear()
		self.ui.lineEdit_MOBILE_2.clear()
		self.ui.textEdit_ADDRESS_2.clear()
		self.ui.textBrowser_STATUS_2.clear()

	# Function for Filling New Details.
	def fill_details_page2(self):
		ROLL = AYEAR = MOBILE = 0
		NAME = self.ui.lineEdit_NAME_2.text()
		CLASS = self.ui.lineEdit_CLASS_2.text()
		ROLL = int(str(self.ui.lineEdit_ROLL_2.text()))
		AYEAR = int(str(self.ui.lineEdit_AYEAR_2.text()))
		FATHER = self.ui.lineEdit_FATHER_2.text()
		MOTHER = self.ui.lineEdit_MOTHER_2.text()
		MOBILE = int(str(self.ui.lineEdit_MOBILE_2.text()))
		ADDRESS = str(self.ui.textEdit_ADDRESS_2.toPlainText())

		for row in c.execute('SELECT * FROM Show_Fee'):
			if (CLASS == 'nur'):
				TF = row[0]
			elif (CLASS == 'kg1'):		   # here Total Fee (TF) Column in databse is filled from fee table in database according				                                                   
				TF = row[1]				   # to user class input during filling new details. 
			elif (CLASS == 'kg2'):
				TF = row[2]													
			elif (CLASS == 'one'):
				TF = row[3]
			elif (CLASS == 'two'):
				TF = row[4]
			elif (CLASS == 'three'):
				TF = row[5]
			elif (CLASS == 'four'):
				TF = row[6]
			elif (CLASS == 'five'):
				TF = row[7]
			elif (CLASS == 'six'):
				TF = row[8]
			elif (CLASS == 'seven'):
				TF = row[9]
			elif (CLASS == 'eight'):
				TF = row[10]
			elif (CLASS == 'nine'):
				TF = row[11]
			elif (CLASS == 'ten'):
				TF = row[12] 

		
		c.execute('''INSERT OR IGNORE INTO student_detail (name,class,roll,admission,F_name,M_name,mobile,address) VALUES ( ?,?,?,?,?,?,?,? )''', (str(NAME),str(CLASS),str(ROLL),str(AYEAR),str(FATHER),str(MOTHER),str(MOBILE),str(ADDRESS), ) )

		c.execute('''INSERT OR IGNORE INTO student_fees (name,number,Jan_TF,Feb_TF,Mar_TF,Apr_TF,May_TF,Jun_TF,Jul_TF,Aug_TF,Sep_TF,Oct_TF,Nov_TF,Dec_TF,Jan_PF,Feb_PF,Mar_PF,Apr_PF,May_PF,Jun_PF,Jul_PF,Aug_PF,Sep_PF,Oct_PF,Nov_PF,Dec_PF,Jan_DF,Feb_DF,Mar_DF,Apr_DF,May_DF,Jun_DF,Jul_DF,Aug_DF,Sep_DF,Oct_DF,Nov_DF,Dec_DF) VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?  )''', (str(NAME),str(MOBILE),TF,TF,TF,TF,TF,TF,TF,TF,TF,TF,TF,TF, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0, ) )
			
		c.execute('''INSERT OR IGNORE INTO student_attendence (name,Jan_CA,Feb_CA,Mar_CA,Apr_CA,May_CA,Jun_CA,Jul_CA,Aug_CA,Sep_CA,Oct_CA,Nov_CA,Dec_CA,Jan_TC,Feb_TC,Mar_TC,Apr_TC,May_TC,Jun_TC,Jul_TC,Aug_TC,Sep_TC,Oct_TC,Nov_TC,Dec_TC) VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )''', ( str(NAME),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, ) )
		
		c.execute('''INSERT OR IGNORE INTO image (name) VALUES (?)''', (str(NAME), ) )
		con.commit()
		self.ui.textBrowser_STATUS_2.setText("Detail Sucessfully Recorded !!")
	

	# Camera Functions.
	def play(self):
		try:
			self.video.captureNextFrame()
			self.ui.videoFrame.setPixmap(
                self.video.convertFrame())
			self.ui.videoFrame.setScaledContents(True)
		except TypeError:
				print "No frame"

	def capture(self):
		self.video.captureNextFrame()
		image = bgr2rgb(self.video.currentFrame)
		self.session.refresh_Input(self.inputMode)
		self.recent = self.session.imageFilename_Input(self.inputMode)
		cv2.imwrite(self.recent, image)

		# Now Creating Thumbnail for current image
		thumb_img = cv2.imread(self.recent)
	
		# Resizing the original image for displaying on Qlabel.
		r = 210.0 / thumb_img.shape[1]
		dim = (150, int(thumb_img.shape[0] * r))

		# perform the actual resizing of the image and show it
		resized = cv2.resize(thumb_img, dim, interpolation = cv2.INTER_AREA)
		self.session.refresh_Output(self.outputMode)
		self.thumb = self.session.imageFilename_Output(self.outputMode)
		cv2.imwrite(self.thumb, resized)

		# Writing the current filepath to database.
		for row in c.execute('SELECT * FROM image ORDER BY id DESC LIMIT 1'):	   # selecting last row of image table
			c.execute('UPDATE image SET image_path = ? WHERE id = ?', (str(self.thumb),row[0] ))
			con.commit()
			self.ui.textBrowser_STATUS_2.setText("Image Saved To Databse !!")

	# Function to Show Clicked Image.
	def showFromStream(self):
		cv2.imshow("Captured Image", SessionManager.imread(self.recent))
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	

	# Fuction for TAB_WIDGET 3 Starts from here..
	def reset_page3(self):
		self.ui.lineEdit_MONTH_3.clear()
		self.ui.lineEdit_OPTION_3.clear()
		self.ui.textBrowser_TOTALSTUDENT_3.clear()
		self.ui.textBrowser_TOTALFEE_3.clear()
		self.ui.textBrowser_COLLECTED_3.clear()
		self.ui.textBrowser_DUE_3.clear()
		self.ui.lineEdit_NUR_3.clear()
		self.ui.lineEdit_KG1_3.clear()
		self.ui.lineEdit_KG2_3.clear()
		self.ui.lineEdit_ONE_3.clear()
		self.ui.lineEdit_TWO_3.clear()
		self.ui.lineEdit_THREE_3.clear()
		self.ui.lineEdit_FOUR_3.clear()
		self.ui.lineEdit_FIVE_3.clear()
		self.ui.lineEdit_SIX_3.clear()
		self.ui.lineEdit_SEVEN_3.clear()
		self.ui.lineEdit_EIGHT_3.clear()
		self.ui.lineEdit_NINE_3.clear()
		self.ui.lineEdit_TEN_3.clear()
		self.ui.textBrowser_STATUS_3.clear()
		self.ui.textBrowser_OUTPUT_3.clear()

	# Function for Updating Fee.
	def Update_Fee(self):
		NUR = KG1 = KG2 = ONE = TWO = THREE = FOUR = FIVE = SIX = SEVEN = EIGHT = NINE = TEN = 0

		NUR = int(str(self.ui.lineEdit_NUR_3.text()))
		KG1 = int(str(self.ui.lineEdit_KG1_3.text()))
		KG2	= int(str(self.ui.lineEdit_KG2_3.text()))
		ONE = int(str(self.ui.lineEdit_ONE_3.text()))
		TWO = int(str(self.ui.lineEdit_TWO_3.text()))
		THREE =	int(str(self.ui.lineEdit_THREE_3.text()))
		FOUR = int(str(self.ui.lineEdit_FOUR_3.text()))
		FIVE = int(str(self.ui.lineEdit_FIVE_3.text()))
		SIX = int(str(self.ui.lineEdit_SIX_3.text()))
		SEVEN = int(str(self.ui.lineEdit_SEVEN_3.text()))
		EIGHT = int(str(self.ui.lineEdit_EIGHT_3.text()))
		NINE = int(str(self.ui.lineEdit_NINE_3.text()))
		TEN = int(str(self.ui.lineEdit_TEN_3.text()))

		for row in c.execute('SELECT * FROM Show_Fee'):
			c.execute('UPDATE Show_Fee SET Nur = ?, Kg1 = ?, Kg2 = ?, One = ?, Two = ?, Three = ?, Four = ?, Five = ?, Six = ?, Seven = ?, Eight = ?, Nine = ?, Ten = ?', (NUR ,KG1 ,KG2 ,ONE ,TWO ,THREE ,FOUR ,FIVE ,SIX ,SEVEN ,EIGHT ,NINE ,TEN ) )
			con.commit()
			self.ui.textBrowser_STATUS_3.setText("New Fee Updated !!")

	# Function for Query Fee.
	def query_page3(self):
		SORT_MONTH = 0
		SORT_OPTION = 0
		SORT_MONTH = str(self.ui.lineEdit_MONTH_3.text())
		SORT_OPTION = int(str(self.ui.lineEdit_OPTION_3.text()))


		# January
		if (SORT_MONTH == 'jan' and SORT_OPTION == 1 ):
			for row in c.execute('SELECT id,name,Jan_PF,Jan_DF FROM  student_fees WHERE Jan_PF = Jan_TF'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Jan_PF = Jan_TF'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Jan_TF in c.execute('SELECT sum(Jan_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Jan_TF[0]))
			for Jan_PF in c.execute('SELECT sum(Jan_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Jan_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Jan_TF[0] - Jan_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

		elif (SORT_MONTH == 'jan' and SORT_OPTION == 2 ):
			for row in c.execute('SELECT id,name,Jan_PF,Jan_DF FROM  student_fees WHERE Jan_PF > 0 AND Jan_PF < Jan_TF'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Jan_PF > 0 AND Jan_PF < Jan_TF'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Jan_TF in c.execute('SELECT sum(Jan_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Jan_TF[0]))
			for Jan_PF in c.execute('SELECT sum(Jan_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Jan_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Jan_TF[0] - Jan_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

		elif (SORT_MONTH == 'jan' and SORT_OPTION == 3 ):
			for row in c.execute('SELECT id,name,Jan_PF,Jan_DF FROM  student_fees WHERE Jan_PF = 0 AND Jan_DF = 0'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Jan_PF = 0 AND Jan_DF = 0'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Jan_TF in c.execute('SELECT sum(Jan_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Jan_TF[0]))
			for Jan_PF in c.execute('SELECT sum(Jan_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Jan_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Jan_TF[0] - Jan_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

		# February
		if (SORT_MONTH == 'feb' and SORT_OPTION == 1 ):
			for row in c.execute('SELECT id,name,Feb_PF,Feb_DF FROM  student_fees WHERE Feb_PF = Feb_TF'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Feb_PF = Feb_TF'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Feb_TF in c.execute('SELECT sum(Feb_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Feb_TF[0]))
			for Feb_PF in c.execute('SELECT sum(Feb_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Feb_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Feb_TF[0] - Feb_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

		elif (SORT_MONTH == 'feb' and SORT_OPTION == 2 ):
			for row in c.execute('SELECT id,name,Feb_PF,Feb_DF FROM  student_fees WHERE Feb_PF > 0 AND Feb_PF < Feb_TF'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Feb_PF > 0 AND Feb_PF < Feb_TF'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Feb_TF in c.execute('SELECT sum(Feb_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Feb_TF[0]))
			for Feb_PF in c.execute('SELECT sum(Feb_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Feb_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Feb_TF[0] - Feb_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

		elif (SORT_MONTH == 'feb' and SORT_OPTION == 3 ):
			for row in c.execute('SELECT id,name,Feb_PF,Feb_DF FROM  student_fees WHERE Feb_PF = 0 AND Feb_DF = 0'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Feb_PF = 0 AND Feb_DF = 0'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Feb_TF in c.execute('SELECT sum(Feb_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Feb_TF[0]))
			for Feb_PF in c.execute('SELECT sum(Feb_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Feb_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Feb_TF[0] - Feb_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")
		

		# March
		if (SORT_MONTH == 'mar' and SORT_OPTION == 1 ):
			for row in c.execute('SELECT id,name,Mar_PF,Mar_DF FROM  student_fees WHERE Mar_PF = Mar_TF'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Mar_PF = 0 AND Mar_DF = 0'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Mar_TF in c.execute('SELECT sum(Mar_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Mar_TF[0]))
			for Jan_PF in c.execute('SELECT sum(Jan_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Mar_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Mar_TF[0] - Jan_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

		elif (SORT_MONTH == 'mar' and SORT_OPTION == 2 ):
			for row in c.execute('SELECT id,name,Mar_PF,Mar_DF FROM  student_fees WHERE Mar_PF > 0 AND Mar_PF < Mar_TF'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Mar_PF > 0 AND Mar_PF < Mar_TF'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Mar_TF in c.execute('SELECT sum(Mar_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Mar_TF[0]))
			for Mar_PF in c.execute('SELECT sum(Jan_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Mar_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Mar_TF[0] - Mar_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

		elif (SORT_MONTH == 'mar' and SORT_OPTION == 3 ):
			for row in c.execute('SELECT id,name,Mar_PF,Mar_DF FROM  student_fees WHERE Mar_PF = 0 AND Mar_DF = 0'):
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
				self.ui.textBrowser_OUTPUT_3.insertPlainText(str(row[0])+"            "+str(row[2])+"           "+str(row[3])+"               "+str(row[1])+"\n")
				self.ui.textBrowser_OUTPUT_3.moveCursor(QTextCursor.End)
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Mar_PF = 0 AND Mar_DF = 0'):
				self.ui.textBrowser_TOTALSTUDENT_3.setText(str(row[0]))
			for Mar_TF in c.execute('SELECT sum(Mar_TF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_TOTALFEE_3.setText(str(Mar_TF[0]))
			for Mar_PF in c.execute('SELECT sum(Mar_PF) AS "Total Salary" FROM student_fees'):
				self.ui.textBrowser_COLLECTED_3.setText(str(Mar_PF[0]))
				self.ui.textBrowser_DUE_3.setText(str(Mar_TF[0] - Mar_PF[0]))
			self.ui.textBrowser_STATUS_3.setText("Record Found !!")

	# Fuction for TAB_WIDGET 4 Starts from here..
	def reset_page4(self):
		self.ui.lineEdit_ID_42.clear()
		self.ui.lineEdit_MONTH_42.clear()
		self.ui.lineEdit_FEEAMMOUNT_42.clear()
		self.ui.textBrowser_NAME_42.clear()
		self.ui.textBrowser_CLASS_42.clear()
		self.ui.textBrowser_PAIDFEE_4.clear()
		self.ui.textBrowser_DUEFEE_4.clear()
		self.ui.textBrowser_STATUS_4.clear()
	
	# Function for Submitting fee.			
	def feeSubmit_page4(self):
		ID_SORT_PAGE4 = 0
		SORT_MONTH = 0
		PF = 0
		ID_SORT_PAGE4 = int(str(self.ui.lineEdit_ID_42.text()))
		SORT_MONTH = str(self.ui.lineEdit_MONTH_42.text())
		PF = int(str(self.ui.lineEdit_FEEAMMOUNT_42.text()))

		if (SORT_MONTH == 'jan'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Jan_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Jan_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# February
		elif (SORT_MONTH == 'feb'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Feb_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Feb_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# March
		elif (SORT_MONTH == 'mar'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Mar_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Mar_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# April
		elif (SORT_MONTH == 'apr'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Apr_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Apr_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# May
		elif (SORT_MONTH == 'may'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET May_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET May_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
		# June			
		elif (SORT_MONTH == 'jun'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Jun_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Jun_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# July
		elif (SORT_MONTH == 'jul'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Jul_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Jul_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# August
		elif (SORT_MONTH == 'aug'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Aug_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Aug_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# September
		elif (SORT_MONTH == 'sep'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Sep_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Sep_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					
		# October
		elif (SORT_MONTH == 'oct'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Oct_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Oct_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
		
		# November			
		elif (SORT_MONTH == 'nov'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Nov_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Nov_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()
					con.commit()
						
		# December
		elif (SORT_MONTH == 'dec'):
				
				for row in c.execute('SELECT * FROM student_fees WHERE ID = ?', (ID_SORT_PAGE4, )):
					c.execute('UPDATE student_fees SET Dec_PF = ? WHERE id = ?', (PF,ID_SORT_PAGE4 ))
					TF = row[2]
					DF = (TF - PF)
					c.execute('UPDATE student_fees SET Dec_DF = ? WHERE id = ?', (DF,ID_SORT_PAGE4 ))
					con.commit()
					self.ui.textBrowser_STATUS_4.setText("FEE Submitted !!")

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					self.ui.textBrowser_NAME_42.setText(row[1])
					self.ui.textBrowser_CLASS_42.setText(str(row[2]))
					self.ui.textBrowser_PAIDFEE_4.setText(str(PF))
					self.ui.textBrowser_DUEFEE_4.setText(str(DF))

				for row in c.execute('SELECT * FROM student_detail WHERE id = ?', (ID_SORT_PAGE4, )):
					fo = open("Files/Fee_Data.txt", "a+")
					fo.write("\r\n---------------------------------------------------------")
					fo.write ("\r\nID Number : ");
					a1=(str)(ID_SORT_PAGE4)
					fo.write (a1);
					fo.write ("\r\nName : ");
					b1=(str)(row[1])
					fo.write (b1);
					fo.write ("          Class : ");
					b2=(str)(row[2])
					fo.write (b2);
					fo.write ("          Month : ");
					b3=(str)(SORT_MONTH)
					fo.write (b3);
					fo.write ("\r\nTotal Fee  Rs : ");
					c1=(str)(TF)
					fo.write (c1);
					fo.write ("\r\nSubmitted Fee Rs : ");
					d1=(str)(PF)
					fo.write (d1);
					fo.write ("\r\nDue Fee Rs : ");
					e1=(str)(DF)
					fo.write (e1);
					fo.write ("\r\nTime : ");
					fo.write (localtime);
					fo.close()


	# Fuction for TAB_WIDGET 5 (Message) Starts from here..

	def reset_page5(self):								   # function for reset page and text files.
		self.ui.lineEdit_B_MONTH_5.clear()
		self.ui.lineEdit_B_SENDFROM_5.clear()
		self.ui.lineEdit_B_TO_5.clear()
		self.ui.lineEdit_B1_SENDFROM_5.clear()
		self.ui.lineEdit_B1_TO_5.clear()
		self.ui.lineEdit_B_USERNAME_5.clear()
		self.ui.lineEdit_B_PASSWORD_5.clear()
		self.ui.lineEdit_S_ID_5.clear()
		self.ui.lineEdit_S_NAME_5.clear()
		self.ui.lineEdit_S_NUMBER_5.clear()
		self.ui.textEdit_S_MESSAGE_5.clear()
		self.ui.textBrowser_B_5.clear()
		self.ui.textBrowser_S_5.clear()
		self.ui.textBrowser_S_STATUS_5.clear()
		with open("Files/in.txt",'w'):
			pass
		with open("Files/out.txt",'w'):
			pass
	def clear_OutFile(self):					   # function for clearing out.text
		with open("Files/out.txt",'w'):
			pass


	def Due_Fee_Search(self):	   # function for displaying due student list and writing number in text file.
		SORT_MONTH = 0
		SORT_MONTH = str(self.ui.lineEdit_B_MONTH_5.text())

		if (SORT_MONTH == 'jan'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Jan_PF = 0 AND Jan_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Jan_PF = 0 AND Jan_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'feb'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Feb_PF = 0 AND Feb_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Feb_PF = 0 AND Feb_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'mar'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Mar_PF = 0 AND Mar_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Mar_PF = 0 AND Mar_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'apr'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Apr_PF = 0 AND Apr_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Apr_PF = 0 AND Apr_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'may'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE May_PF = 0 AND May_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE May_PF = 0 AND May_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'jun'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Jun_PF = 0 AND Jun_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Jun_PF = 0 AND Jun_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'jul'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Jul_PF = 0 AND Jul_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Jul_PF = 0 AND Jul_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'aug'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Aug_PF = 0 AND Aug_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Aug_PF = 0 AND Aug_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'sep'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Sep_PF = 0 AND Sep_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Sep_PF = 0 AND Sep_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'oct'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Oct_PF = 0 AND Oct_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Oct_PF = 0 AND Oct_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'nov'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Nov_PF = 0 AND Nov_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Nov_PF = 0 AND Nov_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")
		elif (SORT_MONTH == 'dec'):
			for row in c.execute('SELECT id,number,name FROM  student_fees WHERE Dec_PF = 0 AND Dec_DF = 0'):
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				self.ui.textBrowser_B_5.insertPlainText(str(row[0])+"            "+str(row[1])+"           "+str(row[2])+"\n")
				self.ui.textBrowser_B_5.moveCursor(QTextCursor.End)
				fo = open("Files/in.txt", "a+")
				fo.write (str(row[1])+'\n');
				fo.close()
			for row in c.execute('SELECT COUNT(*) AS "Total_Student" FROM student_fees WHERE Dec_PF = 0 AND Dec_DF = 0'):
				self.ui.textBrowser_S_STATUS_5.setText(str(row[0])+"  record found")

			
	def Input_to_Output(self):	   # function for taking selected number from in.txt and pasting in out.txt.
		SORT_FROM = 0
		SORT_TO = 0
		SORT_FROM = int(str(self.ui.lineEdit_B_MONTH_5.text()))
		SORT_TO = int(str(self.ui.lineEdit_B_MONTH_5.text()))

	
	def send_Bulk_sms(self):	  # Function for sending bulk messages and extracting number one by one from out.txt file
		Username = 0
		Passwd = 0
		
		Username = int(str(self.ui.lineEdit_B_USERNAME_5.text()))
		Passwd = str(self.ui.lineEdit_B_PASSWORD_5.text())
		Message = str(self.ui.textEdit_B_MESSAGE_5.toPlainText())

		c.execute('''INSERT OR IGNORE INTO temp (username,password,message) VALUES ( ?,?,? )''', (str(Username),str(Passwd),str(Message), ) )
		con.commit()

		for row in c.execute('SELECT * FROM temp'):
			
			username = str(row[0])
			passwd = str(row[1])

		#logging into the sms site
		url ='http://site24.way2sms.com/Login1.action?'
		data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

		#For cookies
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

		def bkc(url, data, message, number, opener):	
			#Adding header details
			opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
			try:
				usock = opener.open(url, data)
			except IOError:
				self.ui.textBrowser_S_STATUS_5.setText("N0 Internet !!")

				#return()
			
			jession_id =str(cj).split('~')[1].split(' ')[0]
			send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
			send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
			opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
			try:
				sms_sent_page = opener.open(send_sms_url,send_sms_data)
			except IOError:
				self.ui.textBrowser_S_STATUS_5.setText("Error Occured")
				#return()
			
			self.ui.textBrowser_S_STATUS_5.setText("  Message Send") 
			#return ()

		number = np.loadtxt('FIles/out.txt', dtype = np.str)
		for item in number:
			for row in c.execute('SELECT * FROM temp'):
				message = row[2]
			message = "+".join(message.split(' '))
			bkc(url, data, 	message, item, opener)

	


	

	def send_Single_sms(self):	  # Function for Sending single message
		number = 0

		number = int(str(self.ui.lineEdit_S_NUMBER_5.text()))
		message = str(self.ui.textEdit_S_MESSAGE_5.toPlainText())
		
		
		if __name__ == "__main__":
			username = "*******"
			passwd = "*******"

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
				self.ui.textBrowser_S_STATUS_5.setText("N0 Internet !!")
				#return()
				
			jession_id =str(cj).split('~')[1].split(' ')[0]
			send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
			send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+str(number)+'&message='+message+'&msgLen=136'
			opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
			
			try:
				sms_sent_page = opener.open(send_sms_url,send_sms_data)
			except IOError:
				self.ui.textBrowser_S_STATUS_5.setText("Error !!")
				#return()
			self.ui.textBrowser_S_STATUS_5.setText("Message Send !!")
	
	# Fuction for Connection with buttons.
	def behaviour(self):
		self.connect(self.ui.pushButton_SUBMIT, Qt.SIGNAL("clicked()"), self.query_page1)
		self.connect(self.ui.pushButton_RESET_1, Qt.SIGNAL("clicked()"), self.reset_page1)
		self.connect(self.ui.pushButton_SUBMIT_2, Qt.SIGNAL("clicked()"), self.fill_details_page2)
		self.connect(self.ui.pushButton_RESET_2, Qt.SIGNAL("clicked()"), self.reset_page2)
		self.connect(self.ui.pushButton_CAPTURE, Qt.SIGNAL("clicked()"), self.capture)
		self.connect(self.ui.pushButton_SHOWfromStream, Qt.SIGNAL("clicked()"), self.showFromStream)
		self.connect(self.ui.pushButton_SUBMIT_3, Qt.SIGNAL("clicked()"), self.query_page3)
		self.connect(self.ui.pushButton_RESET_3, Qt.SIGNAL("clicked()"), self.reset_page3)
		self.connect(self.ui.pushButton_UPDATEFEE_3, Qt.SIGNAL("clicked()"), self.Update_Fee)
		self.connect(self.ui.pushButton_SUBMITFEE_42, Qt.SIGNAL("clicked()"), self.feeSubmit_page4)
		self.connect(self.ui.pushButton_RESET_42, Qt.SIGNAL("clicked()"), self.reset_page4)
		self.connect(self.ui.pushButton_2, Qt.SIGNAL("clicked()"), self.reset_page5)
		self.connect(self.ui.pushButton_B_CHECKRESULT_5, Qt.SIGNAL("clicked()"), self.Due_Fee_Search)
		self.connect(self.ui.pushButton_B_SENDMESSAGE_5, Qt.SIGNAL("clicked()"), self.send_Bulk_sms)
		self.connect(self.ui.pushButton_B_CLEAR_5, Qt.SIGNAL("clicked()"), self.clear_OutFile)
		self.connect(self.ui.pushButton_S_SENDMESSAGE_5, Qt.SIGNAL("clicked()"), self.send_Single_sms)
		self.connect(self.ui.pushButton_SENDMESSAGE, Qt.SIGNAL("clicked()"), self.sms)
	
# Running programs in Main Function.
def main():
	app = QtGui.QApplication(sys.argv)
	ex = Gui()
	ex.show()
	
	
	sys.exit(app.exec_())

if __name__ == '__main__':
	if os.getcwd() not in sys.path:
			sys.path.append(os.getcwd())
	main()
