import re
import os
import shutil
import csv
import sys
from threading import Timer, Thread
from pydub import AudioSegment

from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton,QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QPixmap, QColor, QFont
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint

from Gunshot_Recognition_model import do_recognition
from Gunshot_Audio_Capturing import liveRecording
from Gunshot_Data_CSV import updateTrainClass
from Gunshot_Recognition_CNN import do_training

# calling pyqt5 file class here.
from Gunshot_Recognition_PROGRESS_BAR import TrainingProgressBar

######################################################################################################################################
######################################################################################################################################
######################################################################################################################################

# global variable, which is used when user cancel the recording in the live recording dialog box.
live_record_stop = 0
freq_thres = 300

# styleshhet
bm = "background-color:#a0daff; border-radius:10px; color:#000000"
mm = "background-color:#58b5ef; border-radius:10px; color:#000000"

def updateCSV(Sound,Accuracy,Time,Date,Distance):
    with open('Data_Record/sound_record.csv', 'a') as soundData:
        soundData.write('\n{},{},{},{},{}'.format(Sound,Accuracy,Time,Date,Distance))

def activeRecog():
    global freq_thres
    data = 'audio_record/output.wav'
    x = do_recognition(data, freq_thres)
    return(x)
        
#############################################################################################################################################
################################   This Window is going to be used by the admin to train the madel.   #######################################
#############################################################################################################################################

class TrainWindow(QMainWindow):

    def __init__(self):
       
        # to prevent GUI lockup in long run.
        #----------------------------------------------------------------------
        QApplication.processEvents()
        
        super().__init__()
        #super(ChildWindow, self).__init__(parent)
        self.setFixedSize(1000, 500)
        self.setWindowTitle(' Sound Classification v3.0 ')
        self.setWindowIcon(QIcon('assets/icon.png'))
                      
        # This part retrive the last saved position of the MainWindow before this windows appear.
        # displaying the this window in exact same postion.
        #----------------------------------------------------------------------------------------
        try:
            self.settings = QSettings(" ", " ")
            self.restoreGeometry(self.settings.value("geometry", ""))
            self.restoreState(self.settings.value("windowState", ""))
        except:
            pass
        
        # Disabling the the close button here.
        #----------------------------------------------------------------------
        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        
        # Background Color.
        #----------------------------------------------------------------------
        color = QColor("#3484A9")
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
        
        # Setting background Image.
        #----------------------------------------------------------------------
        oImage = QImage("assets/main_background.jpg")
        sImage = oImage.scaled(QSize(1000, 500))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))                     
        self.setPalette(palette)
        
        # defining all labels here.        
        #----------------------------------------------------------------------
        self.Label_sbg_bg1 = QLabel(self)
        self.Label_sbg_bg2 = QLabel(self)
        self.Label_sbg_title1 = QLabel(self)
        self.Label_sbg_title2 = QLabel(self)
        self.Label_predict111 = QLabel(self)
        self.Label_predict121 = QLabel(self)
        self.Label_predict131 = QLabel(self)
        self.Label_predict141 = QLabel(self)
        self.Label_setfreq = QLabel(self)
        self.Label_predict_totalClass = QLabel(self)

        self.Label_predict_className = QLabel(self)
        self.Label_predict_time = QLabel(self)
        self.Label_predict_recordText = QLabel(self)
        self.Label_predict_recordTextHeader = QLabel(self)
        
        self.Label_thres = QLabel(self)       
        self.Label_predict11 = QLabel(self)
        self.Label_predict12 = QLabel(self)
        self.Label_predict13 = QLabel(self)
        self.Label_predict14 = QLabel(self)
        self.Label_predict_timeD = QLabel(self)       
        self.Label_record = QLabel(self)
        
        # setting title text image here 'MODEL STATUS'.
        #----------------------------------------------------------------------
        self.Label_title_ani1 = QLabel(self)
        self.Label_title_ani1.resize(277, 45)
        self.Label_title_ani1.move(115, 50)        
        movie = QMovie("assets/model_status.png")
        self.Label_title_ani1.setMovie(movie)
        movie.start()
        
        # setting title text image here 'TRAINING'.
        #----------------------------------------------------------------------
        self.Label_title_ani2 = QLabel(self)
        self.Label_title_ani2.resize(205, 67)
        self.Label_title_ani2.move(640, 40)        
        movie = QMovie("assets/training.png")
        self.Label_title_ani2.setMovie(movie)
        movie.start()
               
        self.initUI()
        
        # calling stylesheet here.
        #----------------------------------------------------------------------        
        from Gunshot_Recognition_CSS import styleSheetTrain
        self.setStyleSheet(styleSheetTrain)
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  init FUNCTION   ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      
    
    def initUI(self):
        self.constantLabel()
        self.ButtonMainWindow()
        self.ClassNameBoxSet()
        self.ThresholdSetBox()
        self.labelThreshold()
        self.ButtonShowClass()
        self.ButtonAddClass()
        self.ButtonFreqThres()
        self.ButtonReTrain()
        self.DisplayAccLoss()
        self.ButtonToTrain()
        self.RecordLabel()
        self.ButtonRecord()
        self.Button_Message_Signal_Trained()
        self.show()
        
        # showinging the blur image over the background.
        #----------------------------------------------------------------------
        self.label_blur_img = QLabel(self)
        color = QColor(0, 0, 0, 200)                                            # rgba color code here.
        pixmap = QPixmap(1000, 500)
        pixmap.fill(color)
#        pixmap = QPixmap('assets/pg_bg1.png')
        self.label_blur_img.setPixmap(pixmap)
        self.label_blur_img.resize(1000,500)

        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#########################################################  CLOSE EVENT   ####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#   
    def closeEvent(self, event):
        
        self.label_blur_img.show() 
        
        msgBox = QMessageBox.question(self, 'End the Service', 'Are you sure you want to quit?\t', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)        
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        if msgBox == QMessageBox.Yes:
            QMainWindow.closeEvent(self, event)
        else:
            event.ignore()

        self.label_blur_img.hide() 

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
##################################################  DEFINING THE CONSTANT LABEL HERE  #######################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #            

    def constantLabel(self):

        # Sub Background part with transparency Right and Left.
        #----------------------------------------------------------------------
        x = 20
        y = 20
        height = 460
        width = 470
             
        self.Label_sbg_bg1.setText("")
        self.Label_sbg_bg1.resize(width, height)
        self.Label_sbg_bg1.move(x, y)
        self.Label_sbg_bg1.setObjectName("sub_bg")
        
        self.Label_sbg_bg2.setText("")
        self.Label_sbg_bg2.resize(width, height)
        self.Label_sbg_bg2.move(x + 490, y)
        self.Label_sbg_bg2.setObjectName("sub_bg")
        
        # Element of left side.
        #######################################################################

        # Sub Background title part
        #----------------------------------------------------------------------        
        self.Label_sbg_title1.setText("")
        self.Label_sbg_title1.resize(440, 70)
        self.Label_sbg_title1.move(35, 35)
        self.Label_sbg_title1.setObjectName("sub_title")
        
        height = 40
        width = 440
        x_axis = 35
        y_axis = 120
        
        self.Label_predict111.setText("TRAIN ACCU   :")
        self.Label_predict111.resize(width, height)
        self.Label_predict111.move(x_axis, y_axis)
        self.Label_predict111.setObjectName("textDisplayBg")

        self.Label_predict121.setText("TEST ACCU    :")
        self.Label_predict121.resize(width, height)
        self.Label_predict121.move(x_axis, y_axis + 45)
        self.Label_predict121.setObjectName("textDisplayBg")

        self.Label_predict131.setText("TRAIN LOSS   :")
        self.Label_predict131.resize(width, height)
        self.Label_predict131.move(x_axis, y_axis + 90)      
        self.Label_predict131.setObjectName("textDisplayBg")

        self.Label_predict141.setText("TEST LOSS     :")
        self.Label_predict141.resize(width, height)
        self.Label_predict141.move(x_axis, y_axis + 135)
        self.Label_predict141.setObjectName("textDisplayBg")
        
        self.Label_predict_totalClass.setText("SHOW SOUND CLASSES :")
        self.Label_predict_totalClass.resize(width, height)
        self.Label_predict_totalClass.move(x_axis, y_axis + 308)
        self.Label_predict_totalClass.setObjectName("textDisplayBg")
        
        # Sub Background {set frequency}
        #----------------------------------------------------------------------        
        self.Label_setfreq.setText("")
        self.Label_setfreq.resize(width, 100)
        self.Label_setfreq.move(x_axis, y_axis + 190)
        self.Label_setfreq.setObjectName("textDisSetFreq")
         
        
        # Element of right side.
        #######################################################################
        self.Label_sbg_title2.setText("")
        self.Label_sbg_title2.resize(440, 70)
        self.Label_sbg_title2.move(525, 35)
        self.Label_sbg_title2.setObjectName("sub_title")

        # Sub Background title part
        #---------------------------------------------------------------------- 
        
        height = 40
        width = 440
        x_axis = 525
        y_axis = 120

        self.Label_predict_className.setText("CLASS NAME :")
        self.Label_predict_className.resize(width, height)
        self.Label_predict_className.move(x_axis, y_axis)
        self.Label_predict_className.setObjectName("textDisplayBg")
        
        self.Label_predict_time.setText("TRAINED ON :")
        self.Label_predict_time.resize(width, height)
        self.Label_predict_time.move(x_axis, y_axis + 45)
        self.Label_predict_time.setObjectName("textDisplayBg")
        
        self.Label_predict_recordText.setText("")
        self.Label_predict_recordText.resize(width, 190)
        self.Label_predict_recordText.move(x_axis, y_axis + 100)
        self.Label_predict_recordText.setObjectName("textDisplayRecord")
        
        self.Label_predict_recordTextHeader.setText("  DATA COLLECTION  ")
        self.Label_predict_recordTextHeader.resize(width, 60)
        self.Label_predict_recordTextHeader.move(x_axis + 0, y_axis + 100)
        self.Label_predict_recordTextHeader.setAlignment(Qt.AlignCenter)
        self.Label_predict_recordTextHeader.setObjectName("textDisplayRecordHeader")
        
        
# ----------------------------------------------------------------------------------------------------------------------------------------- #
########################################   DISPLAYING THE ACUURACY & LOSS OF THE MODEL   ####################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #   
   
    def DisplayAccLoss(self):
        
        with open('Data_Record/training_data_saved.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                row

        height = 40
        width = 295
        x_axis = 180
        y_axis = 120
        
        value1 = row[4]
        self.Label_predict11.setText(value1)
        self.Label_predict11.resize(width, height)
        self.Label_predict11.move(x_axis, y_axis)
        self.Label_predict11.setObjectName("textDisplay")

        value2 = row[5]
        self.Label_predict12.setText(value2)
        self.Label_predict12.resize(width, height)
        self.Label_predict12.move(x_axis, y_axis + 45)
        self.Label_predict12.setObjectName("textDisplay")
        
        value3 = row[6]
        self.Label_predict13.setText(value3)
        self.Label_predict13.resize(width, height)
        self.Label_predict13.move(x_axis, y_axis + 90)      
        self.Label_predict13.setObjectName("textDisplay")

        value4 = row[7]   
        self.Label_predict14.setText(value4)
        self.Label_predict14.resize(width, height)
        self.Label_predict14.move(x_axis, y_axis + 135)
        self.Label_predict14.setObjectName("textDisplay")
        
        # This contains the value of last trained.
        #----------------------------------------------------------------------
        value5 = row[8]   
        self.Label_predict_timeD.setText(value5)
        self.Label_predict_timeD.resize(width, height)
        self.Label_predict_timeD.move(670, 165)
        self.Label_predict_timeD.setObjectName("textDisplay1")

# ----------------------------------------------------------------------------------------------------------------------------------------- #
#################################   SETTING UP THE THRESHOLD FOR FREQUENCY AND DISPLAYING IT   ##############################################     
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    # Displaying the current threshold of the model.
    #--------------------------------------------------------------------------
    def labelThreshold(self):
        global freq_thres        
        x = str(freq_thres)

        thresText = 'Current threshold for frequency is '+ x + '. Enter the new \nthreshold value and click on set to change the current \nthreshold vlaue.'
        
        self.Label_thres.setText(thresText)
        self.Label_thres.resize(350, 50)
        self.Label_thres.move(90, 325)
        self.Label_thres.setStyleSheet("color:#3484A9; font-size:15px; font-weight:bold; font-family: 'calibri', Garamond, 'Comic Sans MS'")
    
    # Text Box for setting the Threshold.
    #--------------------------------------------------------------------------
    def ThresholdSetBox(self):
        self.textbox2 = QLineEdit(self)
        self.textbox2.setStyleSheet("color:#808080; background-color:#000000; border-radius:10px; padding-left:10px; font-size:12px; font-weight:bold")
        self.textbox2.move(294,365)
        self.textbox2.resize(95,30)
    
# ----------------------------------------------------------------------------------------------------------------------------------------- #
#########################################################   SET THRESHOLD BUTTON  ###########################################################     
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    # Button for setying up the frequenct threshold for the model.
    #-------------------------------------------------------------------------
    def ButtonFreqThres(self):
        self.button_set = QPushButton('SET',self)
        self.button_set.setToolTip('Click to set frequency threshold.   ')
        self.button_set.setObjectName("restButtonTrain")   
        self.button_set.resize(50,30)
        self.button_set.move(375,365)
        self.button_set.clicked.connect(self.on_click_freq_thres)
              
    # This click event is used for setting up the frequency threshold. 
    #--------------------------------------------------------------------------
    def on_click_freq_thres(self):    

        # storing the theshold value in the variable freq_thres.
        #----------------------------------------------------------------------
        global freq_thres
        freq_thres = self.textbox2.text()
        
        # regular expression for matching digit of length uptp 5.
        #----------------------------------------------------------------------
        freq_thres = str(freq_thres)
        
        if (re.fullmatch(r"[0-9]{1,5}", freq_thres)):
            
            self.label_blur_img.show()
            
            x = 'Threshold set as ' + freq_thres + ' successfully ! \t'
            QMessageBox.information(self, 'Threshold', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))     
            
            self.label_blur_img.hide()
            
            # refreshing the label of threshold.
            #------------------------------------------------------------------
            self.labelThreshold()
                    
        else:
            self.label_blur_img.show()
                    
            # displaying message if wrong value is given for threshold frequency.
            #--------------------------------------------------------------------
            x = ' Enter the correct value.\t  \n\n 1) Only positive numbers are allowed. \n 2) Length must be 1 to 5.'
            QMessageBox.critical(self, 'Threshold', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
            self.label_blur_img.hide()
       
        
# ------------------------------------------------------------------------------------------------------------------------------------------#
###################################  POP UP FOR  DISPLAYING THE TOTAL CLASS AVAILABLE IN THE MODEL   ########################################
# ------------------------------------------------------------------------------------------------------------------------------------------#        
    
    # Show the total class available in the model.
    def ButtonShowClass(self):
        self.button_sh_cls = QPushButton('Click here to view',self)
        self.button_sh_cls.setToolTip('Shows the total number of classes in the model.   ')
        self.button_sh_cls.setObjectName("restButtonTrain")   
        self.button_sh_cls.resize(178,38)
        self.button_sh_cls.move(270,429)
        self.button_sh_cls.clicked.connect(self.on_click_noc)
  
    # this click event is used to print the total classes that the model is trained with.
    def on_click_noc(self):
    
        # displaying total classes.
        self.label_blur_img.show()
                
        from Gunshot_Recognition_VIEW_CLASS import TotalClassAvailable
        self.dialog = TotalClassAvailable(self)
        self.dialog.exec_()
        
        self.label_blur_img.hide()
        
# ----------------------------------------------------------------------------------------------------------------------------------------- #            
#################################################   TEXT BOX TO ENTER THE CLASS NAME   ######################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #
    
    className = ''
    
    # Text Box for setting the class name.
    def ClassNameBoxSet(self):
        self.textbox1 = QLineEdit(self)
        self.textbox1.setObjectName("classNameBox")
        self.textbox1.setPlaceholderText("Enter the class name.")
#        self.textbox1.setAlignment(Qt.AlignCenter)
        self.textbox1.move(670, 120)
        self.textbox1.resize(295,40)
 
# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################  UPLOAD FUNCTION TO SELECT DATA FROM THE DISK FOR THE MODEL    #######################################
# ------------------------------------------------------------------------------------------------------------------------------------------#                
    
    def UploadTheFile(self):
        
        # opening the dialog for selecting the file location.
        # If you want to add all file the add this "All Files (*);; before Audio Files (*.wav).
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Sound Classification v3.0", "","Audio Files (*.wav)", options=options)
        
        # If file get selected then only it creates the folder directory.
        if fileName:
            print(fileName)
            
            global className
            className = className.lower()

            if(os.path.isdir('audio/'+ className) == True):
      
                # remove folder an its contents
                shutil.rmtree('audio/'+ className +'/'+ className)
                shutil.rmtree('audio/'+ className)
    
                os.makedirs('audio/'+ className)
                os.makedirs('audio/'+ className +'/'+ className)
    
            else:
                os.makedirs('audio/'+ className)
                os.makedirs('audio/'+ className +'/'+ className)
                
            # exporting the file to the location as defined above.
            audio = AudioSegment.from_wav(fileName)
            audio.export('audio/'+ className +'/'+ className +'.wav', format='wav')  
            
            self.label_blur_img.show()
            
            # displaying the message that data successfully added.
            x = " Data successfully added. \n Now, click on the 'TRAINING' button to train the model.\t"
            QMessageBox.information(self, 'Message', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))

            self.label_blur_img.hide()
        
            # enabling the TRAINING button after adding the file into the model.
            self.button_train.setEnabled(True)
            self.button_train.setToolTip('Click to start training.   ')
            self.button_train.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
                
                
# ------------------------------------------------------------------------------------------------------------------------------------------#   
###################################################    RECORD LABEL & BUTTON   ##############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#
       
    # priniting label for live data data collection.
    def RecordLabel(self):     
#        value = 'To train the model with the live data, click on the record \nbutton to start recording. When "TRAINING" button get \nenabled, click it to start training the model.'     
        value = 'If you have the data file (*.wav), you can add it by \nclicking on the ADD DATA button or you can record the \nlive data by using RECORD button.'
        self.Label_record.setText(value)
        self.Label_record.resize(350, 60)
        self.Label_record.setAlignment(Qt.AlignCenter)
        self.Label_record.move(570, 275)
        self.Label_record.setStyleSheet("color:#3484A9; font-size:12px;  font-family:Tahoma, Geneva, sans-serif; font-weight:bold")
                    
    # Button for recording live data.
    def ButtonRecord(self):
        self.button_add_record = QPushButton('RECORD',self)
        self.button_add_record.setToolTip('Click to record live data.   ')
        self.button_add_record.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
                  
        self.button_add_record.resize(120,40)
        self.button_add_record.move(610,350)
        self.button_add_record.clicked.connect(self.on_click_record)
    
    # Button record event for RECORD Button.    
    def on_click_record(self):
        global live_record_stop        
        global className
        
        # storing the class name into the variable className.
        #----------------------------------------------------------------------
        className = self.textbox1.text()

        self.label_blur_img.show()
        
        # checking with the regular expression that name is in the correct format.
        #-------------------------------------------------------------------------
        if (re.fullmatch(r"[a-z]+", className)):
            
            # start the Dialog UI for recording.
            #------------------------------------------------------------------
            from Gunshot_Detection_WINDOW_LIVE_RECORDING import LiveRecordingDialog
            self.dialog = LiveRecordingDialog(className, self)
            self.dialog.exec_() 
#            self.dialog.deleteLater()
            
            print(live_record_stop)
            
            if(live_record_stop == 1):
                
                # Enabling the "TRAINING" button.
                #--------------------------------------------------------------
                self.button_train.setEnabled(True)
                self.button_train.setToolTip('Click to start training.   ')
                self.button_train.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
            else:
                
                # disabling the "TRAINING" button.
                #--------------------------------------------------------------
                self.button_train.setToolTip('Train button is currently disabled.   ')
                self.button_train.setEnabled(False)
                self.button_train.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)                         
                      
        else:            
                    
            x = ' Enter the class Name in the format.\t\t       \n\n 1)  Must be in small letters. \n 2)  Name must have letters only. \n 2)  Dont provide space between the words.'
            QMessageBox.critical(self, 'Live Recording.', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
        self.label_blur_img.hide()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  ADD BUTTON   ######################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#   
                
    # Button to add new data to the model.    
    def ButtonAddClass(self):
        self.button_add_data = QPushButton('ADD DATA',self)
        self.button_add_data.setToolTip('Click to add data for training model.   ')
        self.button_add_data.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)   
        self.button_add_data.resize(120,40)
        self.button_add_data.move(750,350)
        self.button_add_data.clicked.connect(self.on_click_add_class)
    
    # This click event is used for training the model.
    def on_click_add_class(self):    
        
        global className
        # storing the class name into the variable className.
        className = self.textbox1.text()

        self.label_blur_img.show() 
        
        # checking with the regular expression that name is in the correct format.
        if (re.fullmatch(r"[a-z]+", className)):                       
            # getting the file location
            self.UploadTheFile()
                        
        else:               
            x = ' Enter the Class Name in the format.\t\t       \n\n 1)  Must be in small letters. \n 2)  Name must have letters only. \n 2)  Dont provide space between the words.'
            QMessageBox.critical(self, 'Live Recording.', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
        self.label_blur_img.hide()
                    
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#######################################################  RE-Train BUTTON   ##################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#   
                
    # Button to add new data to the model.    
    def ButtonReTrain(self):
        self.button_re_train = QPushButton('RE-TRAIN',self)
        self.button_re_train.setToolTip('Re train with the existing data..   ')
        self.button_re_train.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)   
        self.button_re_train.resize(120,40)
        self.button_re_train.move(545,428)
        self.button_re_train.clicked.connect(self.on_click_re_train)
    
    # This click event is used for training the model.
    def on_click_re_train(self):    
        
        self.label_blur_img.show() 
             
        x = ' Re-train the model with the existing data by adjusting some of the parameters.\t'
        msg = QMessageBox.information(self, 'Re-Train.', x , QMessageBox.Yes, QMessageBox.No)
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        if(msg == QMessageBox.Yes ):
            from Gunshot_Detection_USER_TRAIN import UserTraining
            dialog_user_training = UserTraining(self)
            dialog_user_training.exec_()
        
        else:
            pass
        
        # refreshing the Accu / loss data and training time.
        #----------------------------------------------------------------------
        self.DisplayAccLoss()
        
        self.label_blur_img.hide()
            
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  TRAIN BUTTON  #####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#             
    
    # Button for training the model.    
    def ButtonToTrain(self):
        self.button_train = QPushButton('TRAINING',self)
        self.button_train.setToolTip('Train button is currently disabled.   ')
        self.button_train.setEnabled(False)
        self.button_train.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)   
        self.button_train.resize(120,40)
        self.button_train.move(685,428)
        self.button_train.clicked.connect(self.on_click_training)

    def on_click_training(self):
        global className
        
        # saving the last known postion of the traiing window.
        self.settings = QSettings(" ", " ")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        # poping up the message box to do training
        self.label_blur_img.show()
        
        msgBox = QMessageBox.question(self, 'Model Training', ' Do you really want to train the model with the available data? \n Once training get strated you cannot go back.    ', QMessageBox.Yes, QMessageBox.No)        
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        if msgBox == QMessageBox.Yes:
                  
            # writing name into the CSV file.
            #------------------------------------------------------------------
            updateTrainClass(className)
            
            # disabling the TRAIN button to prevent further training on the same data.
            self.button_train.setToolTip('Train button is currently disabled.   ')
            self.button_train.setEnabled(False)
            self.button_train.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)
            
            # disabling the GOBACK button to prevent further training on the same data.
            self.button_mm.setToolTip('Go back button is currently disabled.   ')
            self.button_mm.setEnabled(False)
            self.button_mm.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)   
            
            # disabling the ADD DATA button to prevent further training on the same data.
            self.button_add_data.setToolTip('Add Data button is currently disabled.   ')
            self.button_add_data.setEnabled(False)
            self.button_add_data.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)  
            
            # disabling the RECORD button to prevent the purther recording.
            self.button_add_record.setToolTip('Click to record live data.   ')
            self.button_add_record.setEnabled(False)
            self.button_add_record.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """) 
                
                
            # disabling the close button to prevent further training on the same data.
            # self.setWindowFlag(Qt.WindowCloseButtonHint, False)
  
            # ProgrssBar definition part here. Running the training in the thread ( background )and poping up
            # the dialog box for waiting. after completeion pop up closed.
                        
            # poping up the progressbar window here and hiding Training Window.
            self.dialog_train = TrainingProgressBar()
            self.dialog_train.show()
            
            # closing training window here.
            self.hide()

            # to start training in the background.            
            self.TrainingLoop()  

        else:
            #event.ignore()
            print('exit')
        
        self.label_blur_img.hide()
                       
# ------------------------------------------------------------------------------------------------------------------------------------------#    
################################################  THREAD WITH TRAINING LOOP   ###############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#       
    
    # thread to start the training.
    def TrainingLoop(self): 
        thread_train = Timer(1, self.do_training_loop)
        thread_train.daemon = True
        thread_train.start()                             
        
    # Definition contains do training part and button enabling.
    def do_training_loop(self):
 
        # calling training method from Gunshot_Recognition_CNN.py 
        do_training()
                    
        # enabling the GOBACK button.
        self.button_mm.setToolTip('Go back to main window.   ')
        self.button_mm.setEnabled(True)
        self.button_mm.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
            
        # enabling the ADD DATA button.
        self.button_add_data.setToolTip('Add new classes to the model.   ')
        self.button_add_data.setEnabled(True)
        self.button_add_data.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
            
        # enabling the RECORD button.
        self.button_add_record.setToolTip('Click to record live data.   ')
        self.button_add_record.setEnabled(True)
        self.button_add_record.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
                 
        
        # going back to the Training window and hiding the Progress bar window.
        #----------------------------------------------------------------------                     
        self.show()
               
        self.dialog_train.close()
        
        # send signal for click the button here to pop up the message.
        #----------------------------------------------------------------------
        self.button_xxx.click() 

    # Here i have created the hidden button in the training window so, when we come back from the training
    # the message 'successfully' trained will appear and for that we have auto-click event in above do_training_loop.         
    #-----------------------------------------------------------------------------------------------------------------
    def Button_Message_Signal_Trained(self):
        self.button_xxx= QPushButton('',self)
        self.button_xxx.setStyleSheet("background: transparent")   
        self.button_xxx.resize(0,0)
        self.button_xxx.move(0,0)
        self.button_xxx.clicked.connect(self.send_signal_trained)
       
    def send_signal_trained(self): 
        #self.dialog1 = TrainingProgressBarMessage()
        #self.dialog1.show()

        self.label_blur_img.show() 

        x = " Model Trained Successfully, Click 'OK' to go back.       \n\n 1) You can add more data and retrain the model. \n 2) You can do recognition with current trained model. \t"
        QMessageBox.information(self, 'Training Completed.', x , QMessageBox.Ok)
        self.setWindowIcon(QIcon('assets/icon.png')) 
        
        # updating the train accu / loss data display.
        #----------------------------------------------------------------------
        self.DisplayAccLoss()

        self.label_blur_img.hide() 
     
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
#####################################################   GO BACK BUTTON   ####################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    def ButtonMainWindow(self):
        self.button_mm = QPushButton('GO BACK',self)
        self.button_mm.setToolTip('Go back to Main Window')
        self.button_mm.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
        self.button_mm.resize(120,40)
        self.button_mm.move(825,428)
        self.button_mm.clicked.connect(self.on_click_mm)
        
    # This click event is used for going back to the main window
    def on_click_mm(self):
        
        # saving the last known postion of the training window so that another window can appear on the same position.
        self.settings = QSettings(" ", " ")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        self.hide()
        
        import Gunshot_Recognition_IF_NO_CLASS
        Gunshot_Recognition_IF_NO_CLASS.close_main_window = 2
        
        from Gunshot_Detection_WINDOW_MAIN import MainWindow
        self.dialog = MainWindow()
        self.dialog.show()
        
        
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
#        window = TrainWindow()
#        window.show()
#            
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except Exception as e:
#    print('\nSERVICE SHUTDOWN\n', e)