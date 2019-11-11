from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton,QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint
import sys
import os
import re
import time
from threading import Timer


#########################################################################################################################################
#########################################################  PROGRESS BAR CLASS  ##########################################################
#########################################################################################################################################
        
# class for the progress bar, we goung to hide the title bar, increase the window fixed pos and set transparent background.
# we bring ths window at he topo of every thing.

# ------------------------------------------------------------------------------------------------------------------------------------------#    
####################################################  DUMMY RECORD PROGRESS BAR   ###########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

class RecordingProgressBar(QDialog):
    '''
    def __init__(self):
        super().__init__()
        #super(MainWindow, self).__init__()
       '''
    def __init__(self, timeLength, parent=None):
        
        QDialog.__init__(self, parent)
        
        # passing TimeLength from the Gunshot_Recognition_PROGRESS_BAR.
        self.timeLength = timeLength
        print(self.timeLength)
        
        self.setFixedSize(400, 400)
        #self.move(500, 50)
        self.setWindowTitle(' Sound Classification v3.0 ')
        self.setWindowIcon(QIcon('assets/icon.png'))

        # Blocking the the any other window. 
        #----------------------------------------------------------------------
        self.setWindowModality(Qt.ApplicationModal)
                
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        
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
            color = QColor('#c2c2c2')
            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), color)
            self.setPalette(p) 
   
        # Defining all label here.
        #----------------------------------------------------------------------
        self.Label_t3 = QLabel(self)
        self.Label_t1 = QLabel(self)
        self.Label_t1_sub = QLabel(self)
        
        self.Label_t2 = QLabel(self)
        self.Label_ani = QLabel(self)
        self.Label_timer_refresh = QLabel(self)
        
        self.initUI()
        
    def initUI(self):  

        self.constantLabel()
        self.thread_waitingTimerCalculation()
            
    def constantLabel(self):             

        # Setting animated Image.
        #----------------------------------------------------------------------        
        self.Label_ani.resize(350, 260)
        self.Label_ani.move(75, 35)        
        movie = QMovie("assets/pg1.gif")
        self.Label_ani.setMovie(movie)
        movie.start()
        
        # defining all labels here.        
        #----------------------------------------------------------------------        
        self.Label_t1.setText('Please Wait')
        self.Label_t1.setStyleSheet("color:#000000; font-size:25px; font-weight:bold")
        self.Label_t1.resize(300, 40)
        self.Label_t1.move(125, 320)
        
        self.Label_t1_sub.setText('Please wait, while we finish collecting the \n\t          dummy data.')
        self.Label_t1_sub.setStyleSheet("color:#000000; font-size:15px; font-weight:bold")
        self.Label_t1_sub.resize(400, 50)
        self.Label_t1_sub.move(40, 352)
                
        self.Label_t2.setText('')
        self.Label_t2.setStyleSheet("background-color:#ffffff; border-radius:140px; border: 4px solid #808080;")
        self.Label_t2.resize(290, 280)
        self.Label_t2.move(53, 25)
        
        self.Label_t3.setText('')
        self.Label_t3.setStyleSheet("background-color:#20ffffff")
        self.Label_t3.resize(400, 100)
        self.Label_t3.move(0, 320)

        self.Label_timer_refresh.setText('-- : --')
        self.Label_timer_refresh.setStyleSheet("font-size:35px")
        self.Label_timer_refresh.setAlignment(Qt.AlignCenter)
        self.Label_timer_refresh.resize(100, 40)
        self.Label_timer_refresh.move(150, 145)
        
    
    def thread_waitingTimerCalculation(self):
        th_timer = Timer(0, self.waitingTimeCalculation)
        th_timer.daemon = True
        th_timer.start()

    
    # Displaying the timer in the progress bar area insise the progress circle.
    #--------------------------------------------------------------------------
        
    def waitingTimeCalculation(self):
                               
        user_input = int(self.timeLength)       
        
        # When user input is 5 then timer will start with 4 min 59 sec.
        #----------------------------------------------------------------------
        timer_min = user_input - 1       
        timer_sec = 59
        
        while (True):
            
            QApplication.processEvents()
            QCoreApplication.processEvents()
                        
            if(len(str(timer_min))<2):
                timer_min = '0'+str(timer_min)
            
            timer =  str(timer_min) +':'+ str(timer_sec)
            self.Label_timer_refresh.setText(timer)
            
            time.sleep(1)
            
            timer_min = int(timer_min)
            timer_sec = int(timer_sec)
            
            if(timer_min == 0 and timer_sec == 0):
                self.Label_timer_refresh.setText("Please Wait")
                self.Label_timer_refresh.setStyleSheet("font-size:25px; font-weight:bold")
                self.Label_timer_refresh.setAlignment(Qt.AlignCenter)
                self.Label_timer_refresh.resize(150, 40)
                self.Label_timer_refresh.move(125, 145)
                break
         
            if(timer_sec == 0):
                timer_min = timer_min - 1
                timer_sec = 59
                                
            else:
                timer_sec = timer_sec - 1
                
                if(len(str(timer_sec))<2):
                    timer_sec = '0'+str(timer_sec)
        
    

# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  ???????????????????   ###############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
 

class RecordingProgressBarMessage(QMainWindow):

    def __init__(self, parent=None):
        
        QMainWindow.__init__(self, parent) 
        
        self.setFixedSize(500, 100)
        self.setWindowFlags(Qt.FramelessWindowHint)
                     
        # Blocking the the any other window. 
        ##############################################################################
        self.setWindowModality(Qt.ApplicationModal)
                                     
        oImage = QImage("assets/mess1.jpg")
        sImage = oImage.scaled(QSize(500, 100))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        
        self.button_train = QPushButton('',self)
        self.button_train.setToolTip('click to close the messagebox      ')
        self.button_train.setStyleSheet("color: #000000; font-weight:bold ;background: transparent")   
        self.button_train.resize(500,100)
        self.button_train.move(0,0)
        self.button_train.clicked.connect(self.on_click_close_message)
        
    def on_click_close_message(self):
        self.close()                        

# ------------------------------------------------------------------------------------------------------------------------------------------#    
############################################## TRAINING PROGRESS-BAR when training started  #################################################
# ------------------------------------------------------------------------------------------------------------------------------------------# 
        
class TrainingProgressBar(QMainWindow):
    
    def __init__(self, parent=None):
        
        QMainWindow.__init__(self, parent)
        
        self.setFixedSize(1000, 500)

        self.setWindowTitle(' Sound Classification v3.0 ')
        self.setWindowIcon(QIcon('assets/icon.png'))

        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        
 
        # animated label.
        #----------------------------------------------------------------------
        self.Label_ani = QLabel(self)
        self.Label_ani.resize(1000, 500)
        self.Label_ani.move(0, 0)        
        movie = QMovie("assets/training.gif")
        self.Label_ani.setMovie(movie)
        movie.start()       
        
        # defining label here for timer {training estimater timer}
        #----------------------------------------------------------------------
        self.Label_timer = QLabel(self)
        self.Label_timer.setText("--:--")
        self.Label_timer.resize(150, 60)
        self.Label_timer.move(425, 270)
        self.Label_timer.setAlignment(Qt.AlignCenter)
        self.Label_timer.setStyleSheet("color:#FFFFFF; font-size:30px")
        
        self.initUI()
        
    def initUI(self):   
        self.threadTimer()
    
    # Thread timer.
    #----------------------------------------------------------------------                
    def threadTimer(self):
        th_training_time = Timer(0, self.trainingTime)
        th_training_time.daemon = True
        th_training_time.start()        
        
    def trainingTime(self):
        
        # calling the function here to get estimated time.
        #----------------------------------------------------------------------
        from Gunshot_Recognition_Training_Time_Calculation import calculateTrainingTime
        timeLength = calculateTrainingTime()
        
        user_input = int(timeLength)       
        
        timer_min = user_input - 1       
        timer_sec = 59
        
        while (True):
            
            QApplication.processEvents()
            QCoreApplication.processEvents()
                        
            if(len(str(timer_min))<2):
                timer_min = '0'+str(timer_min)
            
            timer =  str(timer_min) +':'+ str(timer_sec)
            self.Label_timer.setText(timer)
            
            time.sleep(1)
            
            timer_min = int(timer_min)
            timer_sec = int(timer_sec)
            
            if(timer_min == 0 and timer_sec == 0):
                self.Label_timer.setText("Almost done with the model")
                self.Label_timer.resize(250, 60)
                self.Label_timer.move(380, 270)
                self.Label_timer.setAlignment(Qt.AlignCenter)
                self.Label_timer.setStyleSheet("color:#FFFFFF; font-size:18px; font-weight:bold")
                break
         
            if(timer_sec == 0):
                timer_min = timer_min - 1
                timer_sec = 59
                                
            else:
                timer_sec = timer_sec - 1
                
                if(len(str(timer_sec))<2):
                    timer_sec = '0'+str(timer_sec)        
                


# ------------------------------------------------------------------------------------------------------------------------------------------#    
#################################  TRAINING PROGRESS-BAR when there is no data available { 1st time training } ##############################
# ------------------------------------------------------------------------------------------------------------------------------------------# 

class TrainingProgressBarSmall(QMainWindow):
    
    def __init__(self, parent=None):
        
        QMainWindow.__init__(self, parent)
        
        self.setFixedSize(400, 400)

        self.setWindowTitle(' Sound Classification v3.0 ')
        self.setWindowIcon(QIcon('assets/icon.png'))

        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        
        # Set window background color
        #----------------------------------------------------------------------
        color = QColor("#000000")
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
                       
        # Blocking the the any other window. 
        #----------------------------------------------------------------------
        self.setWindowModality(Qt.ApplicationModal)
        
        # disabling minimize button.
        #----------------------------------------------------------------------
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
                     
        # animated label.
        #----------------------------------------------------------------------
        self.Label_ani = QLabel(self)
        self.Label_ani.resize(800, 400)
        self.Label_ani.move(-200, -20)        
        movie = QMovie("assets/pg6.gif")
        self.Label_ani.setMovie(movie)
        movie.start()
        
        # defining label here for timer {training estimater timer}
        #----------------------------------------------------------------------
        self.Label_timer = QLabel(self)
        self.Label_timer.setText("--:--")
        self.Label_timer.resize(150, 60)
        self.Label_timer.move(125, 160)
        self.Label_timer.setAlignment(Qt.AlignCenter)
        self.Label_timer.setStyleSheet("color:#1839D2; font-size:45px")
                
        self.initUI()
        
    def initUI(self):
        self.threadTimer()           

    # Thread timer.
    #----------------------------------------------------------------------                
    def threadTimer(self):
        th_training_time = Timer(0, self.trainingTime)
        th_training_time.daemon = True
        th_training_time.start()        
        
    def trainingTime(self):
        
        # calling the function here to get estimated time.
        #----------------------------------------------------------------------
        from Gunshot_Recognition_Training_Time_Calculation import calculateTrainingTime
        timeLength = calculateTrainingTime()
        
        user_input = int(timeLength)       
        
        timer_min = user_input - 1       
        timer_sec = 59
        
        while (True):
            
            QApplication.processEvents()
            QCoreApplication.processEvents()
                        
            if(len(str(timer_min))<2):
                timer_min = '0'+str(timer_min)
            
            timer =  str(timer_min) +':'+ str(timer_sec)
            self.Label_timer.setText(timer)
            
            time.sleep(1)
            
            timer_min = int(timer_min)
            timer_sec = int(timer_sec)
            
            if(timer_min == 0 and timer_sec == 0):
                self.Label_timer.setText("Please Wait")
                self.Label_timer.resize(190, 60)
                self.Label_timer.move(112, 160)
                self.Label_timer.setAlignment(Qt.AlignCenter)
                self.Label_timer.setStyleSheet("color:#1839D2; font-size:35px")
                break
         
            if(timer_sec == 0):
                timer_min = timer_min - 1
                timer_sec = 59
                                
            else:
                timer_sec = timer_sec - 1
                
                if(len(str(timer_sec))<2):
                    timer_sec = '0'+str(timer_sec)

# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################################  ???????????????????   ###############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------# 

class TrainingProgressBarMessage(QMainWindow):
    
    def __init__(self, parent=None):      
        QMainWindow.__init__(self, parent) 
  
        self.setFixedSize(500, 100)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Blocking the the any other window. 
        ##############################################################################
        self.setWindowModality(Qt.ApplicationModal)
             
        # background    
        #----------------------------------------------------------------------
        oImage = QImage("assets/mess.jpg")
        sImage = oImage.scaled(QSize(500, 100))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
                
        # buuton declaration
        #----------------------------------------------------------------------
        self.button_train = QPushButton('',self)
        self.button_train.setToolTip('click to close the messagebox      ')
        self.button_train.setStyleSheet("color: #000000; font-weight:bold ;background: transparent")   
        self.button_train.resize(500,100)
        self.button_train.move(0,0)
        self.button_train.clicked.connect(self.on_click_close_message)
        
    def on_click_close_message(self):
        self.close()
     

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################

    
#def run():
#    if __name__ =='__main__':
#        
#        #QApplication.processEvents()
#        my_app = QCoreApplication.instance()
#        
#        if my_app is None:
#            my_app = QApplication(sys.argv)            
#            
#        window = TrainingProgressBar()
#        window.show()
#
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except Exception as e:
#    print('\nSERVICE SHUTDOWN\n\n',e)
