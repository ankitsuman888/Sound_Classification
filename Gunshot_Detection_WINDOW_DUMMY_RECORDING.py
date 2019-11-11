# -*- coding: utf-8 -*-
import sys 
import re
import os
from threading import Timer, Thread

from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton,QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint

from Gunshot_Audio_Capturing import dummyRecording

# calling pyqt5 file class here.
from Gunshot_Recognition_PROGRESS_BAR import RecordingProgressBar


############################################################################################################################################
###################   THIS CLASS HAVE DIALOG BOX FOR DUMMY DATA RECORDING WHICH APPERS ON DUMMY BUTTON CLICK EVENT   #######################
############################################################################################################################################

class dummyRecordingClass(QDialog):


    def __init__(self, parent=None):
                
        # To prevent GUI lockup in long run.
        #----------------------------------------------------------------------
        QApplication.processEvents()
        
        QDialog.__init__(self, parent)
        #super(AdvanceSettingWindow, self).__init__(parent)
        self.setFixedSize(500, 400)
        self.setWindowTitle(' Dummy Recording.')
        self.setWindowIcon(QIcon('assets/icon.png'))
               
        # Background Image.
        #----------------------------------------------------------------------
        if(os.path.exists('assets/main_background.jpg') == True):
            # Background Image.
            self.Label_bg = QLabel(self)
            self.Label_bg.resize(1000, 500)
            self.Label_bg.move(-255, -50)        
            movie = QMovie("assets/main_background.jpg")
            self.Label_bg.setMovie(movie)
            movie.start()
        else:
            # Background Color.
            color = QColor('#3484A9')
            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), color)
            self.setPalette(p)
        
        # Sub Background part with transparency
        #----------------------------------------------------------------------        
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(470, 325)
        self.Label_sbg.move(15, 60)
        self.Label_sbg.setStyleSheet("background-color:#70000000; border-radius:10px")
        
        # setting title text image here {'set notification for'}.
        #----------------------------------------------------------------------
        self.Label_title_ani = QLabel(self)
        self.Label_title_ani.resize(500, 55)
        self.Label_title_ani.move(28, 10)
        
        movie = QMovie("assets/dummy_text.png")
        self.Label_title_ani.setMovie(movie)
        movie.start()
            
        # Sub Background part with transparency
        #----------------------------------------------------------------------        
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(450, 220)
        self.Label_sbg.move(25, 83)
        self.Label_sbg.setStyleSheet("background-color:#50000000; border: 10px solid #000000") 

        # Sub Background part with transparency
        #----------------------------------------------------------------------
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(400, 180)
        self.Label_sbg.move(50, 103)
        self.Label_sbg.setStyleSheet("background-color:#3484A9;  border: 5px solid #000000")
            
        # Sub Background part with transparency
        #----------------------------------------------------------------------
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(400, 110)
        self.Label_sbg.move(50, 103)
        self.Label_sbg.setStyleSheet("background-color:#20000000")

        # setting text here
        #----------------------------------------------------------------------
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText("           Enter the value in the input box and click \n on the 'RECORD' button to start collecting dummy data.\n\n \t          ( Enter in minutes only)")
        self.Label_sbg.resize(360, 80)
        self.Label_sbg.move(70, 120)
        self.Label_sbg.setStyleSheet("background:transparent; font-weight:bold; font-size:13px; font-family:Arial, Helvetica, sans-serif")
            
        # Blocking the the any other window. 
        ##############################################################################
        self.setWindowModality(Qt.ApplicationModal)
       
#        # disabling minimize button.
#        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
#        
#        self.settings = QSettings(" ", " ")
#        self.restoreGeometry(self.settings.value("geometry", ""))
#        self.restoreState(self.settings.value("windowState", ""))

             
#        # displays the position of the window. (x, y, w, h) and extracting the values.
#        # after extracting the value setting the position to the center of the parent.
#        ##############################################################################
#        x = self.frameGeometry()        
#        x = str(x)
#        val = re.findall(r'\d+', x)
#        val = [int(val[1]), int(val[2])]
#        print(val)       
#        self.move(val[0]+260 , val[1]+100)
 
        self.Button_Message_Signal_Recording()
           
        self.initUI()
        
        # calling stylesheet here.
        #----------------------------------------------------------------------        
        from Gunshot_Recognition_CSS import styleSheetDummy
        self.setStyleSheet(styleSheetDummy)
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  close event   #####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    def closeEvent(self, event):

        # closing Dummy Recording Box here.
        self.hide()
                                           
        # opening the Advance setting Dialog here.
        from Gunshot_Detection_WINDOW_ADVANCE_SETTING import AdvanceSettingWindow
        self.dialog = AdvanceSettingWindow(self)
        self.dialog.exec_()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  init FUNCTION   ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
        
    def initUI(self):
        self.ButtonDummyRecord()
        self.dummyRecordLabel()           

        # self.show     ---> background window will not movable.
        self.show()   # ---> background window will be movable.
        
        # defining the blur image over the background.
        #----------------------------------------------------------------------
        self.label_blur_img = QLabel(self)
        color = QColor(0, 0, 0, 200)                                            # rgba color code here.
        pixmap = QPixmap(1000, 500)
        pixmap.fill(color)
#        pixmap = QPixmap('assets/pg_bg1.png')
        self.label_blur_img.setPixmap(pixmap)
        self.label_blur_img.resize(1000,500)
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#################################################  TEXT BOX FOR TIME INPUT IN MIN   #########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
    def dummyRecordLabel(self):
        self.textbox_dummy = QLineEdit(self)
        self.textbox_dummy.setStyleSheet("color:#000000; background-color:#ffffff; border-radius:0px; padding-left:0px; font-size:15px; font-weight:bold; border-style: solid; border-width: 2px; border-color:#000000")
        self.textbox_dummy.setPlaceholderText("Minutes")
        self.textbox_dummy.setAlignment(Qt.AlignCenter)
        self.textbox_dummy.move(205, 230)
        self.textbox_dummy.resize(80,30)                          
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  THREAD FOR RECORDING   ##############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    # Here we want to show the message box of 'please wait' while in the background the the recording takes place.
    # After completion of the recording a message box will appear that take back to advance setting dialog box.        
    
    # defining global timeLength.
    timeLength = 1
             
    def rec(self):           
        global timeLength        
        
        # calling recording function here. 
        dummyRecording(timeLength)
             
        # closing the progress bar here.
        self.dialog_record_progress_bar.close()
     
        # send signal for click the button here to pop up the message.               
        self.button_rec.click()     
        
    def thread_dummyRecording(self):   
        
        # starting the thread just after 1 sec to handle any in process error.
        thread_rec = Timer(1, self.rec)
        thread_rec.daemon = True         # daemon thread     --> when main program exit the associated thread also exit or die.
        thread_rec.start()               # non-daemon thread --> even if main program exit the thread runs on background / block main program.       
        
        #Thread(target = self.rec, daemon = True).start()
        #Thread(target = self.messageWait).start()
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  DUMMY RECORD BUTTON   ###############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
    def ButtonDummyRecord(self):
        self.button_dummy = QPushButton('RECORD',self)
        self.button_dummy.setToolTip('Click to start recording (enter value in minutes).              ')
        self.button_dummy.setObjectName("enabledDummy")
        self.button_dummy.resize(120,40)
        self.button_dummy.move(185,325)                
        self.button_dummy.clicked.connect(self.on_click_dummyRecording)
              
    def on_click_dummyRecording(self):
        
        # Defining global timeLength variable.
        global timeLength
        
        self.label_blur_img.show()
        
        # saving the input time from the textbox to the timeLength variable.
        timeLength = self.textbox_dummy.text()
        timeLength = str(timeLength)        
                        
        # regular expression for matching digit of length uptp 5.
        # r"[1-9]{1}([0-9]{1,4})*|[0]{1}([1-9]{1,4})+"

        if (re.fullmatch(r"[1-9]{1}|[1-9]{1}[0-9]{1}", timeLength)):
            x = '  Recording time is set for ' +  timeLength + ' minute.      \t\n  Do you really want to continue ? \t'

            msgBox = QMessageBox.warning(self, 'Dummy Recording.', x , QMessageBox.Yes, QMessageBox.No)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
            if (msgBox == QMessageBox.Yes):
                
                # Minimize & Maximizing every dialog box and windows here.
                #######################################################################

                self.hide()
                #AdvanceSettingWindow.close(self)

                # recording thread function.          
                self.thread_dummyRecording() 
                            
                # showing the progress bar here by passing the "timeLength".
                #--------------------------------------------------------------                
                self.dialog_record_progress_bar = RecordingProgressBar(timeLength, self)
                self.dialog_record_progress_bar.exec_()                
                       
            else:
                pass                                   
                    
        else:
            x ='Enter the correct value.\t\t\t  \n\n1)  Only integers are allowed. \n2)  Recording upto 139 min. \n3)  ZERO is not allowed. \n4)  Dont include ZERO in the beginning.'   
            QMessageBox.critical(self, 'Time Length', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
        self.label_blur_img.hide()
                              
    # Here i have created the hidden button in the dummy recording window so, when we come back from the training
    # the message 'successfully' trained will appear and for that we have auto-click event in above do_training_loop.         
    def Button_Message_Signal_Recording(self):
        self.button_rec= QPushButton('',self)
        self.button_rec.setStyleSheet("background: transparent")   
        self.button_rec.resize(0,0)
        self.button_rec.move(0,0)
        self.button_rec.clicked.connect(self.send_signal_recording)
        #self.button_xxx.animateClick()
        #self.button_xxx.click()
       
    def send_signal_recording(self): 

        x = " Dummy Data Recording done successfully, Click 'OK' to go back. \t"
        QMessageBox.information(self, 'Recording Successful.', x , QMessageBox.Ok)
        self.setWindowIcon(QIcon('assets/icon.png'))
   
        
###########################################################################################################################################
###########################################################################################################################################
###########################################################################################################################################
 
#def run():
#    if __name__ =='__main__':
#                
#        QApplication.processEvents()        
#        my_app = QCoreApplication.instance()        
#        if my_app is None:
#            my_app = QApplication(sys.argv)                        
#        window = dummyRecordingClass()
#        window.show()
#            
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except:
#    print('\nSERVICE SHUTDOWN\n')       
        