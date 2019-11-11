# -*- coding: utf-8 -*-
import sys 
import os
import re
import csv
from threading import Timer, Thread

from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton, QComboBox, QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint

from Gunshot_Clean_Model import clean_classData, clean_evidence

close = 0
stop = 0
############################################################################################################################################
###################   THIS DIALOG BOX ALLOWS USER TO TRAIN THE MODEL WITH THE DEFAULT PARAMETERS OR USER DEFINED   #########################
############################################################################################################################################

class UserTraining(QDialog):

    def __init__(self, parent=None):
                
        # To prevent GUI lockup in long run.
        #----------------------------------------------------------------------
        QApplication.processEvents()
        
        QDialog.__init__(self, parent)
        self.setFixedSize(500, 450)
        self.setWindowTitle(' Model Re-Training.')
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
        
        # Defining the constant Labels.
        #----------------------------------------------------------------------
        self.Label_sbg = QLabel(self)   
        self.Label_title_ani = QLabel(self)
        
        self.Label_ratio = QLabel(self)
        self.Label_dropout = QLabel(self)
        self.Label_epoches = QLabel(self)
        self.Label_batch_size = QLabel(self)    
        self.Label_sbb = QLabel(self)
        self.button_user = QPushButton('TRAIN',self)
        self.button_default = QPushButton('DEFAULT',self)
        
        self.Label_timer = QLabel(self)
                
        # Blocking the the any other window. 
        ##############################################################################
        self.setWindowModality(Qt.ApplicationModal)
            
        self.initUI()
        
        # calling stylesheet here.
        #----------------------------------------------------------------------        
        from Gunshot_Recognition_CSS import styleSheetDummy
        self.setStyleSheet(styleSheetDummy)
        
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  close event   #####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    def closeEvent(self, event):
        
        self.label_blur_img .show()
        
        global close
        if(close == 1):
            x = " Model training is under process cannot close now.\t"
            msgBox = QMessageBox.warning(self, 'Unable to close.', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
            if(msgBox == QMessageBox.Ok):
                event.ignore()
            else:
                event.ignore()
            
        self.label_blur_img.hide()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  init FUNCTION   ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
        
    def initUI(self):
        self.constantLabels()
        self.ButtonDefaultTraining()
        self.ButtonUserTraining()
        self.LineEdit_UserInput()           

        # self.show     ---> background window will not movable.
        self.show()   # ---> background window will be movable.
        
        # defining the blur image over the background.
        #----------------------------------------------------------------------
        self.label_blur_img = QLabel(self)
        color = QColor(0, 0, 0, 200)                                            # rgba color code here.
        pixmap = QPixmap(1000, 500)
        pixmap.fill(color)
        self.label_blur_img.setPixmap(pixmap)
        self.label_blur_img.resize(1000,500)

# ------------------------------------------------------------------------------------------------------------------------------------------#    
###################################################  Constant Labels definition   ###########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    def constantLabels(self):
        
        # Sub Background part with transparency title
        #----------------------------------------------------------------------        
        self.Label_sbg.setText('')
        self.Label_sbg.resize(440, 60)
        self.Label_sbg.move(30, 15)
        self.Label_sbg.setStyleSheet("background-color:#50000000; border-radius:10px")
            
        # Sub Background part with transparency bottom
        #----------------------------------------------------------------------        
        self.Label_sbb.setText('')
        self.Label_sbb.resize(440, 60)
        self.Label_sbb.move(30, 370)
        self.Label_sbb.setStyleSheet("background-color:#000000; border-bottom-left-radius:20px; border-bottom-right-radius:20px")
        
        # setting title text image here {'training settings'}.
        #----------------------------------------------------------------------
        self.Label_title_ani.resize(500, 55)
        self.Label_title_ani.move(150, 18)        
        movie = QMovie("assets/training.png")
        self.Label_title_ani.setMovie(movie)
        movie.start()
        
        # styleSheet and other parameters.
        #----------------------------------------------------------------------
        styleSheet = "font-family:Arial, Helvetica, sans-serif; background-color:#3484A9; border: 2px solid #000000; font-weight:bold; padding-left:10px; font-size:18px; border-radius:10px"
        width = 440
        height = 35
        x_axis = 30
        y_axis = 110

        # Sub Background part for ratio.
        #----------------------------------------------------------------------             
        self.Label_ratio.setText('Train & Test Data Ratio is         :')
        self.Label_ratio.resize(width, height)
        self.Label_ratio.move(x_axis, y_axis)
        self.Label_ratio.setStyleSheet(styleSheet)

        # Sub Background part for Dropout Value.
        #----------------------------------------------------------------------             
        self.Label_dropout.setText('Dropout Value is                        :')
        self.Label_dropout.resize(width, height)
        self.Label_dropout.move(x_axis, y_axis + 40)
        self.Label_dropout.setStyleSheet(styleSheet)
        
        # Sub Background part for epoches.
        #----------------------------------------------------------------------             
        self.Label_epoches.setText('Number of Epoches is              :')
        self.Label_epoches.resize(width, height)
        self.Label_epoches.move(x_axis, y_axis + 80)
        self.Label_epoches.setStyleSheet(styleSheet)
        
        # Sub Background part for batch size.
        #----------------------------------------------------------------------             
        self.Label_batch_size.setText('Batch Size is                              :')
        self.Label_batch_size.resize(width, height)
        self.Label_batch_size.move(x_axis, y_axis + 120)
        self.Label_batch_size.setStyleSheet(styleSheet)
                                 
        # Sub Background part for Timer.
        #----------------------------------------------------------------------             
        self.Label_timer.setText('Ready to Re-Train the model')
        self.Label_timer.setAlignment(Qt.AlignCenter)
        self.Label_timer.resize(width, height + 60)
        self.Label_timer.move(x_axis, y_axis + 170)
        self.Label_timer.setStyleSheet("color:#000000; background-color:#50000000; font-size:25px; font-family:Impact, Charcoal, sans-serif; border: 2px solid #000000; border-top-right-radius:20px; border-top-left-radius:20px")
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#################################################  TEXT BOX FOR All THE USER DATA   #########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
    def LineEdit_UserInput(self):
        
        styleSheet = "border-top-right-radius:20px; border-bottom-right-radius:10px; background-color:#000000; color:#ffffff; padding-left:15px; padding-right:15px; font-size:15px; font-weight:bold; border-style: solid; border-width: 2px; border-color:#000000"
        width = 120
        height = 35
        x_axis = 350
        y_axis = 110
        
        # default parameters.
        #----------------------------------------------------------------------
        self.ratio = 0.8
        self.dropout = 0.5
        self.epoches = 20
        self.batch_size = 32
        
        # text Box for text train.
        #----------------------------------------------------------------------
        self.textbox_ratio = QLineEdit(self)
        self.textbox_ratio.setStyleSheet(styleSheet)
        self.textbox_ratio.setPlaceholderText(str(self.ratio))
        self.textbox_ratio.setAlignment(Qt.AlignCenter)
        self.textbox_ratio.move(x_axis, y_axis)
        self.textbox_ratio.resize(width, height)

        # text Box for dropout.
        #----------------------------------------------------------------------
        self.textbox_dropout = QLineEdit(self)
        self.textbox_dropout.setStyleSheet(styleSheet)
        self.textbox_dropout.setPlaceholderText(str(self.dropout))
        self.textbox_dropout.setAlignment(Qt.AlignCenter)
        self.textbox_dropout.move(x_axis, y_axis + 40)
        self.textbox_dropout.resize(width, height)

        # text Box for epoches.
        #----------------------------------------------------------------------
        self.textbox_epoches = QLineEdit(self)
        self.textbox_epoches.setStyleSheet(styleSheet)
        self.textbox_epoches.setPlaceholderText(str(self.epoches))
        self.textbox_epoches.setAlignment(Qt.AlignCenter)
        self.textbox_epoches.move(x_axis, y_axis + 80)
        self.textbox_epoches.resize(width, height)
        
        # text Box for batch size.
        #----------------------------------------------------------------------
        self.textbox_batch_size = QLineEdit(self)
        self.textbox_batch_size.setStyleSheet(styleSheet)
        self.textbox_batch_size.setPlaceholderText(str(self.batch_size))
        self.textbox_batch_size.setAlignment(Qt.AlignCenter)
        self.textbox_batch_size.move(x_axis, y_axis + 120)
        self.textbox_batch_size.resize(width, height)                          
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  THREAD FOR Training   ##############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    # Here we want to show the message box of 'please wait' while in the background the the recording takes place.
    # After completion of the recording a message box will appear that take back to advance setting dialog box.        
    
    # defining global timeLength.
    timeLength = 1
             
    def trainingMethod(self):           
        
        # calling training method from Gunshot_Recognition_CNN.py
        #----------------------------------------------------------------------
        from Gunshot_Recognition_CNN import user_do_training
        user_do_training(self.ratio, self.dropout, self.epoches, self.batch_size)
         
        # Enabling all the things after training.
        #----------------------------------------------------------------------
        self.EnableAllThing()
        
        # Setting the Label_Timer value as
        #----------------------------------------------------------------------
        global stop
        stop = 1
        self.Label_timer.setText("Ready to Re-Train the model")
        
        #----------------------------------------------------------------------
        global close
        close = 0
                 
    def thread_training(self):   
        
        # starting the thread just after 1 sec to handle any in process error.
        #----------------------------------------------------------------------
        thread_rec = Timer(1, self.trainingMethod)
        thread_rec.daemon = True         # daemon thread     --> when main program exit the associated thread also exit or die.
        thread_rec.start()               # non-daemon thread --> even if main program exit the thread runs on background / block main program.       
                
# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  Default training BUTTON   ###########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
    def ButtonDefaultTraining(self):

        self.button_default.setToolTip('Click to start Training using default paramters. ')
        self.button_default.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#000000; font-size:15px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
            
        self.button_default.resize(120,40)
        self.button_default.move(270,380)                
        self.button_default.clicked.connect(self.on_click_defaultTraiing)
              
    def on_click_defaultTraiing(self):
             
        self.label_blur_img.show()
        
        # default parameters.
        #------------------------------------------------------------------
        self.ratio = 0.8
        self.dropout = 0.5
        self.epoches = 20
        self.batch_size = 32
                
        x = "Do you wnat to train the model with the default value? \t\n\n "
        x = x + "1) Ratio \t:  "+str(self.ratio)+"\n 2) Dropout \t:  "+str(self.dropout)+"\n 3) Epoches \t:  "+str(self.epoches)+"\n 4) batch_Size \t:  "+str(self.batch_size)
        msgBox = QMessageBox.warning(self, 'Set Default.', x , QMessageBox.Yes, QMessageBox.No)
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        if(msgBox == QMessageBox.Yes):
            print("Training with default value.")

            # Running thread timer training.
            #------------------------------------------------------------------                
            self.Thread_Training_Time()
                        
            # calling training thread functoin here.
            #------------------------------------------------------------------
            self.thread_training()
            
            # During traing disabling all things.
            #------------------------------------------------------------------
            self.DisableAllThing()
            
            #------------------------------------------------------------------
            global close
            close = 1
            
        else:
            pass
            
        self.label_blur_img.hide()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  User training BUTTON   ##############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    def ButtonUserTraining(self):

        self.button_user.setToolTip('Click to start Training with selected paramters. ')
        self.button_user.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#000000; font-size:15px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
            
        self.button_user.resize(120,40)
        self.button_user.move(110,380)                
        self.button_user.clicked.connect(self.on_click_UserTraining)
        
    def on_click_UserTraining(self):
                
        self.label_blur_img.show()
                
        # saving the input time from the textbox to the timeLength variable.
        #----------------------------------------------------------------------
        self.ratio = self.textbox_ratio.text()
        self.dropout = self.textbox_dropout.text()
        self.epoches = self.textbox_epoches.text()
        self.batch_size = self.textbox_batch_size.text()
                                
        # regular expression for matching digit of length uptp 5.
        # r"[1-9]{1}([0-9]{1,4})*|[0]{1}([1-9]{1,4})+"  
        # r"[1-9]{1}|[1-9]{1}[0-9]{1}"
        
        if(self.ratio =="" or self.dropout=="" or self.epoches=="" or self.batch_size==""):
            
            x = ' Please provide all the required values  \t'
            QMessageBox.critical(self, ' Missing Input. ', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
            # default parameters.
            #------------------------------------------------------------------
            self.ratio = 0.8
            self.dropout = 0.5
            self.epoches = 20
            self.batch_size = 32
        
        else:
            count = 0
            if (re.fullmatch(r"[0]*.[1-9]{1,2}|[0]*.[0-9]{1}[1-9]{1}", str(self.ratio))):
                count = count + 1
            
            if (re.fullmatch(r"[0]*.[1-9]{1,2}|[0]*.[0-9]{1}[1-9]{1}", str(self.dropout))):
                count = count + 2

            if (re.fullmatch(r"[1-9]{1}|[0]*[1-9]{1}[0-9]{1,3}", str(self.epoches))):
                count = count + 3

            try:
                if(int(self.batch_size) > 0 and int(self.batch_size) <= 1024):
                    count = count + 4
            except:
                pass
                
            if(count == 10):
                
                # converting the values.
                #--------------------------------------------------------------
                self.ratio = float(self.ratio)
                self.dropout = float(self.dropout)
                self.epoches = int(self.epoches)
                self.batch_size = int(self.batch_size)
                
                print(self.ratio, self.dropout, self.epoches, self.batch_size,'\n')
                print("training")
                
                # Running thread timer training.
                #--------------------------------------------------------------                
                self.Thread_Training_Time()
                
                # calling training thread functoin here.
                #--------------------------------------------------------------
                self.thread_training()
                
                # During traing disabling all things.
                #--------------------------------------------------------------
                self.DisableAllThing()
                
                #--------------------------------------------------------------
                global close
                close = 1
                
                            
            else:
                x = ' One of the value is not in the proper format.  \t\t\t'
                x = x + '\n\n 1) Ratio : must be between 0 to 1 with upto two decimal places.'
                x = x + '\n 2) Dropout : must be between 0 to 1 with upto two decimal places.'
                x = x + '\n 3) Epoches : must be interger { 0 not allowed }.'
                x = x + '\n 4) Batch Size : upto 1024 { 0 not allowed }.'
        
                QMessageBox.critical(self, ' Input Error. ', x , QMessageBox.Ok)
                self.setWindowIcon(QIcon('assets/icon.png'))
                                                                
        self.label_blur_img.hide()
                              

# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  Enable and Disable function   #######################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
    def Thread_Training_Time(self):
        
        th_timer = Timer(0, self.TrainingTimeCalculation)
        th_timer.daemon = True
        th_timer.start()
        
    def TrainingTimeCalculation(self):
        
        import time
        
        from Gunshot_Recognition_Training_Time_Calculation import calculateTrainingTime
        timeLength = calculateTrainingTime()
        
        user_input = int(timeLength)       
        
        timer_min = user_input - 1       
        timer_sec = 59
        
        self.Label_timer.setStyleSheet("color:#3484A9; background-color:#000000; font-size:70px; font-family:Impact, Charcoal, sans-serif; border: 2px solid #000000; border-radius:20px")
        self.Label_timer.resize(440, 150)
                
        global stop
        while (True):
            
            QApplication.processEvents()
            QCoreApplication.processEvents()
                        
            if(stop == 1):
                stop = 0
                break

            if(len(str(timer_min))<2):
                timer_min = '0'+str(timer_min)
            
            timer =  str(timer_min) +' : '+ str(timer_sec)
            self.Label_timer.setText(timer)
           
            time.sleep(1)
            
            timer_min = int(timer_min)
            timer_sec = int(timer_sec)
            
            if(timer_min == 0 and timer_sec == 0):
                self.Label_timer.setText("Please Wait")                
                break
                     
            if(timer_sec == 0):
                timer_min = timer_min - 1
                timer_sec = 59
                                
            else:
                timer_sec = timer_sec - 1
                
                if(len(str(timer_sec))<2):
                    timer_sec = '0'+str(timer_sec)
        
        self.Label_timer.setStyleSheet("color:#000000; background-color:#50000000; font-size:25px; font-family:Impact, Charcoal, sans-serif; border: 2px solid #000000; border-top-right-radius:20px; border-top-left-radius:20px")
        self.Label_timer.resize(440, 95)
                
# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  Enable and Disable function   #######################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    def EnableAllThing(self):

       # Enabling the Buttons.
       #-----------------------------------------------------------------------
       self.button_user.setEnabled(True) 
       self.button_user.setToolTip('Click to start Training with selected paramters. ')
       self.button_user.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#000000; font-size:15px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)            
    
       self.button_default.setEnabled(True)
       self.button_default.setToolTip('Click to start Training with selected paramters. ')
       self.button_default.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#000000; font-size:15px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)            
           
       # Enabling the Input Box.
       #-----------------------------------------------------------------------
       self.textbox_ratio.setEnabled(True)
       self.textbox_dropout.setEnabled(True)
       self.textbox_epoches.setEnabled(True)
       self.textbox_batch_size.setEnabled(True)
       
    def DisableAllThing(self):
       
       # Disabling the Buttons.
       #-----------------------------------------------------------------------
       self.button_user.setEnabled(False) 
       self.button_user.setToolTip('Currently Disabled. ')
       self.button_user.setStyleSheet(""" QPushButton{color:#000000; background-color:#000000; border-radius:10px;} """)
 
       self.button_default.setEnabled(False)
       self.button_default.setToolTip('Currently Disabled. ')
       self.button_default.setStyleSheet(""" QPushButton{color:#000000; background-color:#000000; border-radius:10px;} """)
       
       # Disabling the Input Box.
       #-----------------------------------------------------------------------
       self.textbox_ratio.setEnabled(False)
       self.textbox_dropout.setEnabled(False)
       self.textbox_epoches.setEnabled(False)
       self.textbox_batch_size.setEnabled(False)
        
###########################################################################################################################################
###########################################################################################################################################
###########################################################################################################################################
 
def run():
    if __name__ =='__main__':
                
        QApplication.processEvents()        
        my_app = QCoreApplication.instance()        
        if my_app is None:
            my_app = QApplication(sys.argv)                        
        window = UserTraining()
        window.show()
            
        sys.exit(my_app.exec_())

try:
    run()
except Exception as e:
    print('\nSERVICE SHUTDOWN\n', e)     