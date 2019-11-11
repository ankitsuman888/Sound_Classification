import shutil
import sys
from threading import Timer, Thread
import os

from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton,QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint

import Gunshot_Audio_Capturing
from Gunshot_Audio_Capturing import liveRecording

######################################################################################################################################
###################################################    Live Recording Dialog   ##############################################################
######################################################################################################################################

class LiveRecordingDialog(QDialog):
    
    # Thread for recording live data.
    #--------------------------------------------------------------------------
    def threadRecording(self):              
        thread_record = Timer(1, self.RecordingLoop)
        thread_record.daemon = True
        thread_record.start()
    
    # recording function.
    #--------------------------------------------------------------------------
    def RecordingLoop(self):
        Gunshot_Audio_Capturing.stop = 0
        liveRecording(self.className)
              
    def __init__(self, className, parent=None):

        # to prevent GUI lockup in long run.
        #----------------------------------------------------------------------
        QApplication.processEvents()     
        
        # taking and saving the className into the variable.
        #----------------------------------------------------------------------
        self.className = className
        print(self.className)
        
        QDialog.__init__(self, parent)

        self.setFixedSize(500, 400)
        self.setWindowTitle('Live Recording')
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
                
        # defining label here.
        #----------------------------------------------------------------------
        self.Label_header = QLabel(self)
        self.Label_body = QLabel(self)
        self.Label_timer = QLabel(self)
        self.Label_bottom = QLabel(self)
        
        self.Label_title_ani = QLabel(self)
        
        self.LabelClassNamebg = QLabel(self)
        self.LabelClassName = QLabel(self)
                    
        self.initUI()
        
        # setting title text image here 'LIVE DATA COLLECTION'.
        #----------------------------------------------------------------------
        self.Label_title_ani.resize(450, 67)
        self.Label_title_ani.move(25, 30)        
        movie = QMovie("assets/live_data.png")
        self.Label_title_ani.setMovie(movie)
        movie.start()
        
        # showinging the blur image over the background.
        #----------------------------------------------------------------------
        self.label_blur_img = QLabel(self)
        color = QColor(0, 0, 0, 200)                                            # rgba color code here.
        pixmap = QPixmap(1000, 500)
        pixmap.fill(color)
        self.label_blur_img.setPixmap(pixmap)
        self.label_blur_img.resize(1000,500)
        

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
########################################################   CLOSE EVENT   ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
 
    # close event ,when user dont want to keep the recorded data.
    #--------------------------------------------------------------------------
    def closeEvent(self, event):       

        # sending value to Gunshot_Audio_Capturing and stop the recording.
        #----------------------------------------------------------------------
        Gunshot_Audio_Capturing.stop = 1
        
        # disabling the training button by sending the value.
        #----------------------------------------------------------------------
        import Gunshot_Detection_WINDOW_TRAIN
        Gunshot_Detection_WINDOW_TRAIN.live_record_stop = 0
                
        self.label_blur_img.show()
        
        msgBox = QMessageBox.question(self, 'Recording Canceled !', "Live Recording has been canceled, click on 'Ok'.\t ", QMessageBox.Ok)        
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        if (msgBox == QMessageBox.Ok):           
            try:
                # reading each folder name from the csv file and deleting the folder according to it.
                #------------------------------------------------------------------------------------
                folderName = self.className
                shutil.rmtree('audio/'+ folderName +'/'+ folderName)
                shutil.rmtree('audio/'+ folderName)
                
            except:
                pass
        
        self.label_blur_img.hide()
        
                
    def initUI(self):
        self.ConstantLabel()
        self.LiveClassNameDisplay()
        self.ButtonStartLiveRecording()
        self.ButtonStopLiveRecording()
        
        self.show()

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
#########################################################  CONSTANT LABEL  ##################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #   
    def ConstantLabel(self):
        width = 460
        self.x_axis = 20
        self.y_axis = 20
        
        label_sub_bg =" background-color:#80000000; border-radius:10px "
        
        self.Label_header.resize(width, 80)
        self.Label_header.move(self.x_axis, self.y_axis)
        self.Label_header.setStyleSheet(label_sub_bg)
        
        self.Label_body.resize(width, 220)
        self.Label_body.move(self.x_axis, self.y_axis + 110 )
        self.Label_body.setStyleSheet(label_sub_bg)
        
        self.Label_timer.setText("00 : 00")
        self.Label_timer.resize(width, 100)
        self.Label_timer.setAlignment(Qt.AlignCenter)
        self.Label_timer.move(self.x_axis, self.y_axis + 180)
        self.Label_timer.setStyleSheet("font-size:80px; font-weight:bold; font-family:Impact, Charcoal, sans-serif")
        
        self.Label_bottom.resize(460, 50)
        self.Label_bottom.move(self.x_axis, self.y_axis + 310)
        self.Label_bottom.setStyleSheet("background-color:#000000; border-bottom-right-radius:10px; border-bottom-left-radius:10px ")
 
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
###########################################################    TIMER     ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    def thread_timer_display(self):
        
        th_timer = Timer(0, self.DisplayTimer)
        th_timer.daemon = True
        th_timer.start()
        
    def DisplayTimer(self):
        import time
        
        timer_min = 0
        timer_sec = 0
        
        while(True):
            
            if(Gunshot_Audio_Capturing.stop == 1):
                break
            
            time.sleep(1)
            
            if(len(str(timer_min))<2):
                timer_min = "0" + str(timer_min)            
            
            if(len(str(timer_sec))<2):
                timer_sec = "0" + str(timer_sec)                
                            
            display_timer = str(timer_min)+" : "+str(timer_sec)
            self.Label_timer.setText(display_timer)            
            print(display_timer)
            
            timer_min = int(timer_min)
            timer_sec = int(timer_sec)
            
            timer_sec = timer_sec + 1
            
            if(timer_sec == 60):
                timer_min = timer_min + 1
                timer_sec = 0
                
            
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
###########################################################  CLASS NAME  ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
     
    def LiveClassNameDisplay(self):
        
        self.LabelClassNamebg.setText("CLASS NAME    : ")
        self.LabelClassNamebg.resize(460, 50)
        self.LabelClassNamebg.move( self.x_axis + 0, self.y_axis+ 110)
        self.LabelClassNamebg.setStyleSheet("padding-left:20px; color:#808080; font-size:20px; font-weight:bold; background-color:#000000; border-top-right-radius:8px; border-top-left-radius:8px")
       
        self.LabelClassName.setText(self.className)
        self.LabelClassName.resize(227, 46)
        self.LabelClassName.move(self.x_axis + 231, self.y_axis+ 112)
        self.LabelClassName.setStyleSheet("padding-left:10px; color:#000000; font-size:20px; font-weight:bold; background-color:#35BEF4; border-top-right-radius:7px")

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
##########################################################  START BUTTON  ###################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
 
    def ButtonStartLiveRecording(self):
        self.button_start_record = QPushButton('START',self)
        self.button_start_record.setToolTip('Click to start recording.   ')
        self.button_start_record.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-size:15px; font-weight:bold;} 
                                                   QPushButton:hover{color:#ffffff; background-color:#000000; font-size:25px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}""")
               
        self.button_start_record.resize(130,40)
        self.button_start_record.move(90, 335)
        self.button_start_record.clicked.connect(self.on_click_start_record)
    
    def on_click_start_record(self):

        Gunshot_Audio_Capturing.stop = 0         
        
        # enabling the stop button here.
        #----------------------------------------------------------------------
        self.button_stop_record.setToolTip('Click to stop recording.   ')
        self.button_stop_record.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-size:15px; font-weight:bold;} 
                                                   QPushButton:hover{color:#ffffff; background-color:#000000; font-size:25px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}""")
        self.button_stop_record.setEnabled(True)            
        
        # disabling start button here
        #----------------------------------------------------------------------
        self.button_start_record.setToolTip('Currently not active.   ')
        self.button_start_record.setStyleSheet(""" QPushButton{color:#808080; background-color:#000000; font-size:15px; font-weight:bold;} """)
        self.button_start_record.setEnabled(False)
                    
        self.threadRecording()
        self.thread_timer_display()
 
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
##########################################################  STOP BUTTON  ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    def ButtonStopLiveRecording(self):
        self.button_stop_record = QPushButton('STOP',self)
        self.button_stop_record.setToolTip('Currently not active.   ')
        self.button_stop_record.setStyleSheet(""" QPushButton{color:#808080; background-color:#000000; font-size:15px; font-weight:bold;} """)
        self.button_stop_record.setEnabled(False)
        self.button_stop_record.resize(130,40)
        self.button_stop_record.move(280, 335)
        self.button_stop_record.clicked.connect(self.on_click_stop_record)
    
    def on_click_stop_record(self):

        # sending value to Gunshot_Audio_Capturing and stop the recording.
        #----------------------------------------------------------------------
        Gunshot_Audio_Capturing.stop = 1
        
        # disabling the stop button here.
        #----------------------------------------------------------------------
        self.button_stop_record.setToolTip('Click to stop recording.   ')
        self.button_stop_record.setStyleSheet(""" QPushButton{color:#808080; background-color:#000000; font-size:15px; font-weight:bold;} """)
        self.button_stop_record.setEnabled(False)           
        
        # enabling start button here
        #----------------------------------------------------------------------
        self.button_start_record.setToolTip('Currently not active.   ')
        self.button_start_record.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-size:15px; font-weight:bold;} 
                                                   QPushButton:hover{color:#ffffff; background-color:#000000; font-size:25px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}""")
        self.button_start_record.setEnabled(True)
        
        # sending value to Gunshot_Audio_Capturing and stop the recording.
        #----------------------------------------------------------------------
        Gunshot_Audio_Capturing.stop = 1
        
        self.label_blur_img.show()
                
        x = " Live data collected successfully. \n Now, click on the 'TRAINING' button to train the model.\t"
        QMessageBox.information(self, 'Data Saved successfully.', x , QMessageBox.Ok)
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        self.label_blur_img.hide()
        
        # here we are sending the variable value as 1 which means that when user click on the stop button during
        # the live recording it enable the 'TRAIN' button.  
        #--------------------------------------------------------------------------------------------------------
        import Gunshot_Detection_WINDOW_TRAIN
        Gunshot_Detection_WINDOW_TRAIN.live_record_stop = 1

        self.hide()
        
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
#        window = LiveRecordingDialog("ankit")
#        window.show()
#            
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except Exception as e:
#    print('\nSERVICE SHUTDOWN\n', e)