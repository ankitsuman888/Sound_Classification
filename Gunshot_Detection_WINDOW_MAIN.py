import sys 
import csv
import time
import datetime
from threading import Timer, Thread
import os

from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint

from Gunshot_Recognition_model import do_recognition, frequency_value
from Gunshot_Audio_Capturing import Recording

import Gunshot_Recognition_IF_NO_CLASS

from Gunshot_Recognition_IF_NO_CLASS import CheckingClassAvailability
from Gunshot_Detection_DATA_SAVING import DisplayDataNotification
from Gunshot_send_notification import send_email, send_sms
from Gunshot_Detection_DATA_SAVING import saving_data_file
from Gunshot_Detection_WINDOW_ADVANCE_SETTING import AdvanceSettingWindow
from Gunshot_Detection_WINDOW_TRAIN import TrainWindow  


###########################################################################################################################################
###########################################################################################################################################
###########################################################################################################################################

# global variable, which is used when user cancel the recording in the live recording dialog box.
main_advance_setting_close = 0
stop = True

def updateCSV(Sound,Accuracy,Time,Date,Distance):
    with open("Data_Record/sound_record.csv", 'a') as soundData:
        soundData.write('\n{},{},{},{},{}'.format(Sound,Accuracy,Time,Date,Distance))

def activeRecog():
    import Gunshot_Detection_WINDOW_TRAIN
    data = "audio_record/output.wav"
    x = do_recognition(data, Gunshot_Detection_WINDOW_TRAIN.freq_thres)
    return(x)
        
        
###########################################################################################################################################
####################################################  Main Class Start Here ###############################################################  
###########################################################################################################################################
class MainWindow(QMainWindow):

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
######################################################   MAIN FUNCTION   ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
           
    def __init__(self):

        QMainWindow.__init__(self)
#        super(MainWindow, self).__init__()
        
#        QApplication.processEvents()
#        QCoreApplication.processEvents()
  
        self.setFixedSize(1000, 500)
        self.setWindowTitle(" Sound Classification v3.0 ")
        self.setWindowIcon(QIcon("assets/icon.png"))
        
        # disable the windows title bar.
        #----------------------------------------------------------------------
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setWindowFlags(Qt.CustomizeWindowHint)        
        
        #--------------------------------------------------------------------------------------------
        # This part is for the window postion.
        # At First geometry will be null, so by default the window appear on the center of the screen.
        # Next, when training window get closed the last postion will be saved and in that position 
        # this window will appear.
        #--------------------------------------------------------------------------------------------        
        
        self.settings = QSettings(" ", " ")
        if not self.settings.value("geometry") == None:
            self.restoreGeometry(self.settings.value("geometry"))
        if not self.settings.value("windowState") == None:
            self.restoreState(self.settings.value("windowState"))
        
        # if background image is not available then takin color as background.
        #----------------------------------------------------------------------
        if(os.path.exists('assets/main_background.jpg') == True):
            # Setting background Image.
            oImage = QImage("assets/main_background.jpg")
            sImage = oImage.scaled(QSize(1000, 500))
            palette = QPalette()
            palette.setBrush(10, QBrush(sImage))                     
            self.setPalette(palette)
        else:
            # Background Color.
            color = QColor("#3484A9")
            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), color)
            self.setPalette(p)
        
 
        # defining all labels here.        
        #----------------------------------------------------------------------
        self.Label_sbg_title = QLabel(self)
        self.Label_sbg_l = QLabel(self)
        self.Label_sbg_l1 = QLabel(self) 
        self.Label_sbg_l2 = QLabel(self) 
        self.Label_sbg_l3 = QLabel(self) 
        self.Label_sbg_l4 = QLabel(self) 
        self.Label_sbg_l11 = QLabel(self) 
        self.Label_sbg_l21 = QLabel(self) 
        self.Label_sbg_l31 = QLabel(self) 
        self.Label_sbg_l41 = QLabel(self)
        self.Label_sbg_x = QLabel(self)
        self.Label_sbg_r = QLabel(self) 
        self.Label_sbg_r1 = QLabel(self) 
        self.Label_sbg_r2 = QLabel(self)
        self.Label_copyright = QLabel(self)
        
        self.Label_predict1 = QLabel(self)
        self.Label_accu1 = QLabel(self)
        self.Label_date = QLabel(self)        
        self.Label_avg_freq = QLabel(self)       
        self.Label_predict11 = QLabel(self)
        self.Label_predict12 = QLabel(self)
        self.Label_predict13 = QLabel(self)
        self.Label_predict14 = QLabel(self)
        self.Label_predict15 = QLabel(self)
        self.button_advance = QPushButton("Go To Advance Settings",self)
        self.button_train = QPushButton("TRAINING",self)
        self.button_stop = QPushButton("STOP", self)
        self.button_start = QPushButton("START", self)
              
        # setting title text image here 'SOUND CLASSIFICATION'.
        #----------------------------------------------------------------------
        if(os.path.exists('assets/title.png') == True):
            self.Label_title_ani = QLabel(self)
            self.Label_title_ani.resize(900, 150)
            self.Label_title_ani.move(100, 1)        
            movie = QMovie("assets/title.png")
            self.Label_title_ani.setMovie(movie)
            movie.start()
        else:
            self.Label_title_ani = QLabel(self)
            self.Label_title_ani.setText("SOUND CLASSIFICATION")
            self.Label_title_ani.setStyleSheet("color:#000000; font-weight:bold; font-size:50px")
            self.Label_title_ani.resize(900, 150)
            self.Label_title_ani.move(170, 1) 
            

        # Defining blur label here.
        #----------------------------------------------------------------------
        self.label_blur_img = QLabel(self)
        
        # Running the display time here.
        #----------------------------------------------------------------------
        self.threadTimeDisplay()
        
        # calling init function here.
        #----------------------------------------------------------------------
        self.initUI()

        # calling stylesheet here.
        #----------------------------------------------------------------------        
        from Gunshot_Recognition_CSS import styleSheetMain
        self.setStyleSheet(styleSheetMain)
        

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
#############################################  CLOSE EVENT FOR MAIN WINDOW   ################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
   
    def closeEvent(self, event):
        
        # When service is active then poping up the message to stop the service first.
        #-----------------------------------------------------------------------------
        global stop
        
        self.label_blur_img.show()
        if(stop == False):        
            msgBox = QMessageBox.warning(self, "Warning !", "STOP the service first before closing the application.\t", QMessageBox.Ok)            
            self.setWindowIcon(QIcon("assets/icon.png"))
            
            if msgBox == QMessageBox.Ok:
                event.ignore()
            else:
                event.ignore()
        else:
            # closing the app and ending the child loop here.
            #----------------------------------------------------------------------
            global main_advance_setting_close
            main_advance_setting_close = 2
        
        self.label_blur_img.hide()
        
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
######################################### init FUNCTION TO DECLARE EVERYTHING  ##############################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
   
    def initUI(self):
        self.styleSheetDisplay()
        self.constantLabel() 
        self.copyrightLabel()         
        self.inactive()
        self.prediction_inactive()   
        self.date_n_time()
        self.ButtonStart()
        self.ButtonStop()
        self.ButtonTrainWindow()
        self.AdvanceButton()
        
        self.show()
        
        # checking that model is empty or not and calling it at last so that other features of main window 
        # will be active like button etc.
        self.calling_empty_class()
        
 
    def styleSheetDisplay(self):
        
        # prediction label on leftt side.
        #----------------------------------------------------------------------
        self.Label_predict1.setObjectName("predictionLabels")
        self.Label_predict1.resize(270, 30)
        self.Label_predict1.move(190, 170)
        
        self.Label_avg_freq.setObjectName("predictionLabels_X")
        self.Label_avg_freq.resize(270, 30)
        self.Label_avg_freq.move(190, 305)
        
        self.Label_accu1.setObjectName("predictionLabels")
        self.Label_accu1.resize(270, 30)
        self.Label_accu1.move(190, 215)
        
        # prediction label on right side.
        #----------------------------------------------------------------------
        self.Label_predict11.setObjectName("prediction5")
        self.Label_predict11.resize(350, 30)
        self.Label_predict11.move(580, 235)
        
        self.Label_predict12.setObjectName("prediction5")
        self.Label_predict12.resize(350, 30)
        self.Label_predict12.move(580, 275)
        
        self.Label_predict13.setObjectName("prediction5")
        self.Label_predict13.resize(350, 30)
        self.Label_predict13.move(580, 315)  
        
        self.Label_predict14.setObjectName("prediction5")
        self.Label_predict14.resize(350, 30)
        self.Label_predict14.move(580, 355)
        
        self.Label_predict15.setObjectName("prediction5")
        self.Label_predict15.resize(350, 30)
        self.Label_predict15.move(580, 395)
        
        # date and time.
        #----------------------------------------------------------------------        
        self.Label_date.setObjectName("DateTime")
        self.Label_date.resize(275, 30)
        self.Label_date.move(190, 260)
         
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
###########################################     FUNCTION THAT CHECKS FOR CLASS     ##########################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    

# If the classes.csv is empty then window will appear before the main window else if there is any class then 
# only main window will appear.

   
    # here we are checking that window will appear or not.
    #--------------------------------------------------------------------------
    def calling_empty_class(self):
        
        # defining the blur image over the background.
        #----------------------------------------------------------------------
        color = QColor(0, 0, 0, 200)                                            # rgba color code here.
        pixmap = QPixmap(1000, 500)
        pixmap.fill(color)      
#        pixmap = QPixmap("assets/pg_bg1.png")
        self.label_blur_img.setPixmap(pixmap)
        self.label_blur_img.resize(1000, 500)
             
                
        # opening the csv file and checking if there is any class available or not.
        #--------------------------------------------------------------------------
        with open("audio/classes.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                row
            Id = row[0]
            print(Id)

        # starting the thread that checks for if the CheckClassAvailability window is closed or not.
        #-------------------------------------------------------------------------------------------
        self.closeMain = Timer(0, self.CloseThreadMainWindowSub)
        self.closeMain.daemon = True
        self.closeMain.start()
        
        self.dialog_cca = CheckingClassAvailability(self)   
            
        if(Id == "class_id" or Id == '' or Id == ' '):
            try:    
                self.label_blur_img.show()                 
                self.dialog_cca.show()
                print("no class available ")
            except Exception as e:
                print(e)
                        
        else:
            try:
                self.label_blur_img.hide()
                self.dialog_cca.hide()                                                       
                print("showing only maindow. new data available")           
            except Exception as e:
                print(e)         
            
          
    # checking and closing the main window here. 
    #--------------------------------------------------------------------------
    def CloseThreadMainWindowSub(self):

        global main_advance_setting_close
        
        while(True):
            time.sleep(0.5)   
            
            QApplication.processEvents()
            QCoreApplication.processEvents()
            
#            print('Child Thread Running', main_advance_setting_close, Gunshot_Recognition_IF_NO_CLASS.close_main_window)
            
            # EMPTY MODEL : closing the main window through the IF_NO_CLASS window
            # if no data is available.
            #----------------------------------------------------------------------
            if(Gunshot_Recognition_IF_NO_CLASS.close_main_window == 1):
                Gunshot_Recognition_IF_NO_CLASS.close_main_window = 0
                self.close()
                print("Closing the Main window ( data is not available )-----------")
                break
                
                
            # AFTER TRAINING : hiding the main window just after the training get completed 
            # after the first training when no data is available.                  
            #------------------------------------------------------------------------------
            elif(Gunshot_Recognition_IF_NO_CLASS.close_main_window == 2):
                Gunshot_Recognition_IF_NO_CLASS.close_main_window = 0
                self.label_blur_img.hide()
                self.label_blur_img.hide()
                self.label_blur_img.hide()
                self.label_blur_img.hide()
                self.label_blur_img.hide()
                print("cloing the blur background.---------------------------------")
                
            
            # DATA CLEANED : hiding the main window when we clean the data from the 
            # model and then poping up the main main window.
            #----------------------------------------------------------------------
            elif(main_advance_setting_close == 1):                
                main_advance_setting_close = 0                
                self.hide() 
                print("Hiding the window after main data cleaned.------------------")
  
                         
            # DATA AVAILABLE : when we have data in the model and then we close the 
            # app in that case we are ending the child loop.
            #----------------------------------------------------------------------
            elif(main_advance_setting_close == 2): 
                print("Closing the Main window ( data is available ).--------------")                              
                self.close()
                break
                        
            else:
                pass
            
        print("Child Thread Running Ended.")
                    
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
###########################################   FUNCTION TO DISPLAY DATE AND TIME   ##########################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    # This function is called in the main loop function to print the date and time.                 
    #------------------------------------------------------------------------------
    def date_n_time(self):                
        self.datetime =  QDateTime.currentDateTime().toString("HH:mm:ss | ddd | dd-MM-yyyy")
           
        self.Label_date.setText(self.datetime)
#        self.Label_date.resize(275, 30)
#        self.Label_date.move(190, 260)
#        self.Label_date.setObjectName("DateTime")

    def loopTime(self):        
        while(True):
            self.date_n_time()
            time.sleep(1)
                        
            # ending the thread when main window get closed.
            #------------------------------------------------------------------
            global main_advance_setting_close   
            if(main_advance_setting_close == 2):
                break
            
            QApplication.processEvents()
            QCoreApplication.processEvents()
            
        print("Running Time display Thread Ended.")
        
    def threadTimeDisplay(self):
        self.threadTime = Timer(1, self.loopTime)
        self.threadTime.daemon = True
        self.threadTime.start()

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
##################################################  DEFINING THE CONSTANT LABEL HERE  #######################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #            

    def constantLabel(self):

        # Sub Background part with transparency for title bar
        #----------------------------------------------------------------------             
        self.Label_sbg_title.setText(" ")
        self.Label_sbg_title.resize(960, 110)
        self.Label_sbg_title.move(20, 20)
        self.Label_sbg_title.setObjectName("Title")
            
        #######################################################################    
        # Sub Background part with transparency for LEFT SIDE.
        #----------------------------------------------------------------------
             
        self.Label_sbg_l.setText(" ")
        self.Label_sbg_l.resize(470, 315)
        self.Label_sbg_l.move(20, 150)
        self.Label_sbg_l.setObjectName("sbg_l")
       
        height = 40
        width = 430
        x_axis = 40
        y_axis = 165
                    
        self.Label_sbg_l1.setText(" ")
        self.Label_sbg_l1.resize(width, height)
        self.Label_sbg_l1.move(x_axis, y_axis)
        self.Label_sbg_l1.setObjectName("sbg_lx")
                     
        self.Label_sbg_l2.setText(" ")
        self.Label_sbg_l2.resize(width, height)
        self.Label_sbg_l2.move(x_axis, y_axis + 45)
        self.Label_sbg_l2.setObjectName("sbg_lx")
                         
        self.Label_sbg_l3.setText(" ")
        self.Label_sbg_l3.resize(width, height)
        self.Label_sbg_l3.move(x_axis, y_axis + 90)
        self.Label_sbg_l3.setObjectName("sbg_lx")
                       
        self.Label_sbg_l4.setText(" ")
        self.Label_sbg_l4.resize(width, height)
        self.Label_sbg_l4.move(x_axis, y_axis + 135)
        self.Label_sbg_l4.setObjectName("sbg_lx")
                
        width = 140
               
        self.Label_sbg_l11.setText(" SOUND CLASS  :")
        self.Label_sbg_l11.resize(width, height)
        self.Label_sbg_l11.move(x_axis, y_axis)
        self.Label_sbg_l11.setObjectName("sbg_lxx")
                         
        self.Label_sbg_l21.setText(" PROBABILITY   :")
        self.Label_sbg_l21.resize(width, height)
        self.Label_sbg_l21.move(x_axis, y_axis + 45)
        self.Label_sbg_l21.setObjectName("sbg_lxx")
                         
        self.Label_sbg_l31.setText(" DATE & TIME     :")
        self.Label_sbg_l31.resize(width, height)
        self.Label_sbg_l31.move(x_axis, y_axis + 90)
        self.Label_sbg_l31.setObjectName("sbg_lxx")
                         
        self.Label_sbg_l41.setText(" FREQUENCY      :")
        self.Label_sbg_l41.resize(width, height)
        self.Label_sbg_l41.move(x_axis, y_axis + 135)
        self.Label_sbg_l41.setObjectName("sbg_lxx")
        
        height = 105
        width = 464
        x_axis = 23
        y_axis = 360
                
        self.Label_sbg_x.setText('')
        self.Label_sbg_x.resize(width, height)
        self.Label_sbg_x.move(x_axis, y_axis)
        self.Label_sbg_x.setObjectName("x_bottom")
        
        #######################################################################            
        # Sub Background part with transparency for RIGHT SIDE.
        #----------------------------------------------------------------------
             
        self.Label_sbg_r.setText(" ")
        self.Label_sbg_r.resize(470, 315)
        self.Label_sbg_r.move(510, 150)
        self.Label_sbg_r.setObjectName("sbg_r")

        x_axis = 530
        y_axis = 165
                 
        self.Label_sbg_r1.setText(" NEXT TOP 5 ")
        self.Label_sbg_r1.resize(430, 40)
        self.Label_sbg_r1.move(x_axis, y_axis)
        self.Label_sbg_r1.setAlignment(Qt.AlignCenter)
        self.Label_sbg_r1.setObjectName("sbg_r1")
                 
        self.Label_sbg_r2.setText(" ")
        self.Label_sbg_r2.resize(430, 240)
        self.Label_sbg_r2.move(x_axis, y_axis + 45)
        self.Label_sbg_r2.setAlignment(Qt.AlignCenter)
        self.Label_sbg_r2.setObjectName("sbg_r2")
                
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
#########################################  RECOGNITION OF LEFT SIDE DISPLAYED HERE  #########################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #            
    
    # Label start showing when we click on the start button.
    #--------------------------------------------------------------------------       
        
    def active(self): 
        
        x = activeRecog()
        #x[0][1] = x[0][1]
        x[0][1] = x[0][1] +" %"
        x[0][0] = x[0][0].upper()
        
        #self.Label_predict1.setText('')        
        self.Label_predict1.setText(x[0][0])
#        self.Label_predict1.resize(270, 30)
#        self.Label_predict1.move(190, 170)
#        self.Label_predict1.setObjectName("predictionLabels")
        
        self.Label_accu1.setText(x[0][1])
#        self.Label_accu1.resize(270, 30)
#        self.Label_accu1.move(190, 215)
#        self.Label_accu1.setObjectName("predictionLabels_X")
            
    # Label start showing when serice is in active or we click on stop button.
    # Further initial state of app also define this.
    #--------------------------------------------------------------------------    
    def inactive(self):
        
        self.Label_predict1.setText("Service is not active")
#        self.Label_predict1.resize(270, 30)
#        self.Label_predict1.move(190, 170)
#        self.Label_predict1.setObjectName("predictionLabels")
       
        self.Label_accu1.setText("NULL")
#        self.Label_accu1.resize(270, 30)
#        self.Label_accu1.move(190, 215)
#        self.Label_accu1.setObjectName("predictionLabels")

        # frequency value printing.
        #----------------------------------------------------------------------
        self.Label_avg_freq.setText("NULL")
#        self.Label_avg_freq.resize(270, 30)
#        self.Label_avg_freq.move(190, 305)
#        self.Label_avg_freq.setObjectName("predictionLabels_X")
        
                   
    # Label start showing when it found nothing but service is still active.
    #--------------------------------------------------------------------------
    def listening(self):
              
        self.Label_predict1.setText("Listening . . .")
#        self.Label_predict1.resize(270, 30)
#        self.Label_predict1.move(190, 170)
#        self.Label_predict1.setObjectName("predictionLabels")
               
        self.Label_accu1.setText("NULL")
#        self.Label_accu1.resize(270, 30)
#        self.Label_accu1.move(190, 215)
#        self.Label_accu1.setObjectName("predictionLabels_X")

             
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
############################################### TOP FIVE PREDICTION OF THE RIGHT SIDE DISPLAY ###############################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    def prediction_active(self):
                
        x = activeRecog()
        
        if (len(x[1][0])<5):
            x[1][0] = x[1][0] + "\t"
        
        if (len(x[2][0])<5):
            x[2][0] = x[2][0] + "\t"
        
        if (len(x[3][0])<5):
            x[3][0] = x[3][0] + "\t"
        
        if (len(x[4][0])<5):
            x[4][0] = x[4][0] + "\t"
        
        if (len(x[5][0])<5):
            x[5][0] = x[5][0] + "\t"
        
        value1 = "1)  " + x[1][0].upper() + "\t   : " + x[1][1] + " %"
        self.Label_predict11.setText(value1)
#        self.Label_predict11.resize(350, 30)
#        self.Label_predict11.move(580, 235)
#        self.Label_predict11.setObjectName("prediction5")

        value2 = "2)  "+ x[2][0].upper() + "\t   : " + x[2][1] + " %"
        self.Label_predict12.setText(value2)
#        self.Label_predict12.resize(350, 30)
#        self.Label_predict12.move(580, 275)
#        self.Label_predict12.setObjectName("prediction5")
        
        value3 = "3)  "+ x[3][0].upper() + "\t   : " + x[3][1] + " %"
        self.Label_predict13.setText(value3)
#        self.Label_predict13.resize(350, 30)
#        self.Label_predict13.move(580, 315)      
#        self.Label_predict13.setObjectName("prediction5")

        value4 = "4)  "+ x[4][0].upper() + "\t   : " + x[4][1] + " %"         
        self.Label_predict14.setText(value4)
#        self.Label_predict14.resize(350, 30)
#        self.Label_predict14.move(580, 355)
#        self.Label_predict14.setObjectName("prediction5")

        value5 = "5)  "+ x[5][0].upper() + "\t   : " + x[5][1] + " %"          
        self.Label_predict15.setText(value5)
#        self.Label_predict15.resize(350, 30)
#        self.Label_predict15.move(580, 395)
#        self.Label_predict15.setObjectName("prediction5")
            
    def prediction_inactive(self):  
                
        value = "1) Service is not active "                
        self.Label_predict11.setText(value)
#        self.Label_predict11.resize(270, 30)
#        self.Label_predict11.move(580, 235)
#        self.Label_predict11.setObjectName("prediction5")
        
        value = "2) Service is not active "
        self.Label_predict12.setText(value)
#        self.Label_predict12.resize(270, 30)
#        self.Label_predict12.move(580, 275)
#        self.Label_predict12.setObjectName("prediction5")
        
        value = "3) Service is not active "
        self.Label_predict13.setText(value)
#        self.Label_predict13.resize(270, 30)
#        self.Label_predict13.move(580, 315)      
#        self.Label_predict13.setObjectName("prediction5")
        
        value = "4) Service is not active "     
        self.Label_predict14.setText(value)
#        self.Label_predict14.resize(270, 30)
#        self.Label_predict14.move(580, 355)
#        self.Label_predict14.setObjectName("prediction5")
       
        value = "5) Service is not active "       
        self.Label_predict15.setText(value)
#        self.Label_predict15.resize(270, 30)
#        self.Label_predict15.move(580, 395)
#        self.Label_predict15.setObjectName("prediction5")

    def prediction_listening(self): 
         
        value = "1) Please wait. "                
        self.Label_predict11.setText(value)
#        self.Label_predict11.resize(270, 30)
#        self.Label_predict11.move(580, 235)
#        self.Label_predict11.setObjectName("prediction5")
       
        value = "2) Please wait. "
        self.Label_predict12.setText(value)
#        self.Label_predict12.resize(270, 30)
#        self.Label_predict12.move(580, 275)
#        self.Label_predict12.setObjectName("prediction5")
        
        value = "3) Please wait. "
        self.Label_predict13.setText(value)
#        self.Label_predict13.resize(270, 30)
#        self.Label_predict13.move(580, 315)      
#        self.Label_predict13.setObjectName("prediction5")
       
        value = "4) Please wait. "    
        self.Label_predict14.setText(value)
#        self.Label_predict14.resize(270, 30)
#        self.Label_predict14.move(580, 355)
#        self.Label_predict14.setObjectName("prediction5")
        
        value = "5) Please wait. "       
        self.Label_predict15.setText(value)
#        self.Label_predict15.resize(270, 30)
#        self.Label_predict15.move(580, 395)
#        self.Label_predict15.setObjectName("prediction5")
        
#-----------------------------------------------------------------------------------------------------------------------------------------#
########################################### METHOD FOR FREQUENCY & COPYRIGHT DISPLAYING   #################################################   
#-----------------------------------------------------------------------------------------------------------------------------------------#
    
    # Displaying the frequency of incoming sound sample.
    #--------------------------------------------------------------------------
    def avg_frequency_display(self):        
        
        f = frequency_value()
        f = str(f)
        print("frequency  : ",f)            
        self.Label_avg_freq.setText(f)

    # Displaying the copyright text.
    #--------------------------------------------------------------------------
    def copyrightLabel(self):
        
        self.Label_copyright.setText("All Rights Reserved © NCTC 2018.")
        self.Label_copyright.resize(1000,20)
        self.Label_copyright.move(0, 478)
        self.Label_copyright.setObjectName("copyright")

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
######################################################   START BUTTON   ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
      
    def ButtonStart(self):
        
        self.button_start.resize(120,40)
        self.button_start.move(41,375)     
        self.button_start.setObjectName("enabled")
        self.button_start.setProperty('Test', True)
        self.button_start.setToolTip("Start the service.  ")
        
        # click event for starting the recognition part when start button is clicked.
        # ---------------------------------------------------------------------------
        self.button_start.clicked.connect(lambda: self.on_click_start(self.button_start))
        
        # Changing the color and enabling /disabling the button when start button is clicked.
        #------------------------------------------------------------------------------------
        self.button_start.clicked.connect(lambda: self.on_click_start_rest(self.button_stop))
        self.button_start.clicked.connect(lambda: self.on_click_start_rest(self.button_train))
        self.button_start.clicked.connect(lambda: self.on_click_start_rest(self.button_advance))
 
    def on_click_start(self, widget):
        
        print("\nSERVICE STARTED\n")
        global stop
        stop = False
        
        # On clicking the start button disabling the START button to prevent further clicking.
        self.button_start.setObjectName("disabled")
        self.button_start.setToolTip("Service is already active   ")    
        self.button_start.setEnabled(False)                           

        # Update the style
        widget.setStyle(widget.style())
                            
        self.Mythread()
     
        #print('start Thread is alive', self.thread.is_alive())

    def on_click_start_rest(self, widget):
        
        # When start button is enabled then disabling the TRAIN button.
        self.button_train.setObjectName("disabled")
        self.button_train.setToolTip("Stop the service first.   ") 
        self.button_train.setEnabled(False)
        
        # Disabling the advance setting button when app is active.   
        self.button_advance.setObjectName("Advance_disabled")
        self.button_advance.setToolTip("Stop the service first to access advance setting.         ")
        self.button_advance.setEnabled(False) 
        
        # On clicking the start button enabling the STOP button to stop the service.
        self.button_stop.setObjectName("enabled")
        self.button_stop.setToolTip("Click to stop the service.   ")
        self.button_stop.setEnabled(True)
        
        # Update the style
        widget.setStyle(widget.style())

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
######################################################   STOP BUTTON   ######################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    def ButtonStop(self):
        
        self.button_stop.resize(120,40)
        self.button_stop.move(194,375)
        self.button_stop.setObjectName("disabled")
        self.button_stop.setProperty('Test', True)       
        self.button_stop.setToolTip("Service is already inactive.  ")
        self.button_stop.setEnabled(False)
  
        # click event for stopping the recognition part when stop button is clicked.
        # ---------------------------------------------------------------------------
        self.button_stop.clicked.connect(lambda: self.on_click_stop(self.button_stop))
        
        # Changing the color and enabling /disabling the button when stop button is clicked.
        #------------------------------------------------------------------------------------
        self.button_stop.clicked.connect(lambda: self.on_click_stop_rest(self.button_start))
        self.button_stop.clicked.connect(lambda: self.on_click_stop_rest(self.button_train))
        self.button_stop.clicked.connect(lambda: self.on_click_stop_rest(self.button_advance))              

    def on_click_stop(self, widget):
        
        global stop
        stop = True   
                        
        # On clicking the stop button disabling the STOP button to prevent further clicking.
        self.button_stop.setObjectName("disabled")
        self.button_stop.setToolTip("Service is already inactive.   ")
        self.button_stop.setEnabled(False)
        
        # Update the style
        widget.setStyle(widget.style())
                 
        print("\nSERVICE STOPPED\n")
        
        time.sleep(1)
        
        self.inactive()
        self.prediction_inactive()
        print("stop Thread is alive", self.thread_pred.is_alive())
        
    def on_click_stop_rest(self, widget):
        
        # Enaabling the advance setting button when app is inactive.
        self.button_advance.setObjectName("Advance_enabled")
        self.button_advance.setEnabled(True)
        
        # On clicking the stop button enabling the START button to start the service.        
        self.button_start.setObjectName("enabled")
        self.button_start.setToolTip("Click here to start the service.   ") 
        self.button_start.setEnabled(True)
            
        # On clicking the stop button enabling the TRAIN button to goto training window.         
        self.button_train.setObjectName("enabled") 
        self.button_train.setToolTip("Click here to open training window.   ")                  
        self.button_train.setEnabled(True)
        
        # Update the style
        widget.setStyle(widget.style())
        
 
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
###################################################   TRAINING  BUTTON   ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
 
    def ButtonTrainWindow(self):
        
        self.button_train.resize(125,40)
        self.button_train.move(345,375)
        self.button_train.setObjectName("enabled")
        self.button_train.setProperty('Test', True)  
        self.button_train.setToolTip("Click here to open training window.   ")
        self.button_train.clicked.connect(self.on_click_train)
        
    def on_click_train(self):
        
        # saving the last known postion of the main window so that another window can appear on the same position.
        self.settings = QSettings(" ", " ")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        # Poping up the training window.
        #----------------------------------------------------------------------
        self.dialog = TrainWindow()
        self.dialog.show()
        
        # hiding up the main window.
        #----------------------------------------------------------------------
        self.hide()
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
##############################################  ADVANCE SETTING BUTTON   ####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

    # Advance setting button.
    def AdvanceButton(self):
        
        self.button_advance.resize(300,27)
        self.button_advance.move(105, 435)
        self.button_advance.setProperty('Test', True)  
        self.button_advance.setObjectName("Advance_enabled")
        self.button_advance.setToolTip("Click here to open advance setting window.   ")
        self.button_advance.clicked.connect(self.on_click_advanceButton)
                
    def on_click_advanceButton(self):
        
        # saving the last known postion of the main window so that another window can appear on the same position.
        self.settings = QSettings(" ", " ")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        # showing the blur image over the background.
        self.label_blur_img.show()
        
        # Showing dialog box on the burron click event.
        self.dialog = AdvanceSettingWindow(self)
        self.dialog.exec_()
        
        self.label_blur_img.hide()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
################################################  THREAD FOR THE LOOP   #####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
    # This thread is going to be get executed when click event for start button happen.
    def Mythread(self):
        
        # 0 means thread start executing after 0 second of button click event.
        self.thread_pred = Timer(0, self.loop)
        self.thread_pred.start()
                 
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#############################################  MAIN LOOP TO DO RECOGNITION   ################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
  
    def loop(self):
                
        global stop

        try :
            while(True):
                
                QApplication.processEvents()
                QCoreApplication.processEvents()
                
#                time.sleep(0.5)
                
                print("Recognition is in progress.")
                                
                now = datetime.datetime.now()
                Ctime = now.strftime("%I:%M:%S : %p")
                Cdate = str(datetime.datetime.now().date())
    
                if(stop == True):
                    break
                
                Recording()
                
                if(stop == True):
                    break
                           
                x = activeRecog()
                
                self.avg_frequency_display()
                
                if(stop == True):
                    break
                
                if(int(float(x[0][1])) >= 50):
                    print(x[0][0],'  ', int(float(x[0][1])), end ="%  ")
                    
                    self.active()
                    self.prediction_active()
                                                         
                    # calling function that Opens the CSV file to read the latest data that user 
                    # saved for notification user generally saved the class, email, phone number.
                    #-------------------------------------------------------------------------------
                    data = DisplayDataNotification()
                    
                    if(x[0][0] == data[0]):
                        
                        send_email(data[0], data[1], x[0][1])                       # data[class, email, phone]
                        send_sms(data[0], data[2], x[0][1])                         # x[0][1] = probability
                        
                        # Here updating the CSV file (sound_evidence.csv)
                        # -----------------------------------------------------------------------------
                        saving_data_file(x[0][0], x[0][1])
                    
                else:
                    self.listening()
                    self.prediction_listening()
                    print('Found Nothing,', end =" ")
                
                
                print("Completed\n")
                
                # writting the data into the csv file.
                #--------------------------------------------------------------
                if(int(float(x[0][1]) >= 90)):
                    updateCSV(x[0][0], x[0][1], Ctime, Cdate, "null")
            
        except Exception as e:
            print("ERROR : ", e)
               
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
 
#def run():
#    if __name__ =='__main__':
#                
#        QApplication.processEvents()        
#        my_app = QCoreApplication.instance()        
#        if my_app is None:
#            my_app = QApplication(sys.argv)                        
#        window = MainWindow()
#        window.show()
#            
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except:
#    print('\nSERVICE SHUTDOWN\n')

                  
                    