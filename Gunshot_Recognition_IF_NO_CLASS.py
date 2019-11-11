#######################################################################################################################################
#### Here checking the if any data is available in the model or not, if not then asking for add data first to get access to app #######  
#######################################################################################################################################

from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton,QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint

import re
import sys
import shutil
import os
from pydub import AudioSegment
from threading import Timer

className = ''
live_record_stop = 0
close_main_window = 0

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
###########################################     MAIN FUNCTION STARTS FROM HERE     ##########################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #     
    
class CheckingClassAvailability(QMainWindow):
    
    def CreatingEverything():
        print('hello')
        # create folders        
        
        # create csv file
        
        # Replace the CSV file with new empty one.        
        with open('audio/classes.csv', 'w') as IdData:
            IdData.write('{},{}'.format('class_id','class_name'))
            
        with open('audio/dummy_class.csv', 'w') as IdData:
            IdData.write('{},{}'.format('Id','class_name'))
            # add 0, silence ,here
 
  
    def __init__(self, parent=None):
        
        QMainWindow.__init__(self, parent)       
        self.setFixedSize(400, 400)
        self.setWindowTitle(' Sound Classification v3.0 ')
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        # disabling minimize button.
        #----------------------------------------------------------------------
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        
        # Blocking the the any other window. 
        #----------------------------------------------------------------------
        self.setWindowModality(Qt.ApplicationModal)
             
        # displays the position of the window. (x, y, w, h) and extracting the values.
        # after extracting the value setting the position to the center of the parent.
        #-----------------------------------------------------------------------------
        #self.settings = QSettings(" ", " ")
        #self.restoreGeometry(self.settings.value("geometry", ""))
        #self.restoreState(self.settings.value("windowState", ""))
        #x = self.frameGeometry()        
        #x = str(x)
        #val = re.findall(r'\d+', x)
        #val = [int(val[1]), int(val[2])]        
        #self.move(val[0]+300 , val[1]+60)
        
        # Background Image.
        #----------------------------------------------------------------------
        if(os.path.exists('assets/main_background.jpg') == True):
            # Background Image.
            self.Label_bg = QLabel(self)
            self.Label_bg.resize(1000, 500)
            self.Label_bg.move(-300, -50)        
            movie = QMovie("assets/main_background.jpg")
            self.Label_bg.setMovie(movie)
            movie.start()
        else:
            # Background Color.
            color = QColor("#3484A9")
            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), color)
            self.setPalette(p)
            
        # Defining all Label here.
        #----------------------------------------------------------------------   
        self.Label_title = QLabel(self)
        self.Label_title_text = QLabel(self)
        self.Label_title_sub_text = QLabel(self)     
        self.Label_body = QLabel(self)             
        self.Label_footer = QLabel(self)
     
        self.initUI()
        
        from Gunshot_Recognition_CSS import styleSheetIfNoClass
        self.setStyleSheet(styleSheetIfNoClass)
        
    def initUI(self):
        self.ConstantLabel()          
        self.AnimationImage()
        self.ClassNameTextBox()
        self.ClassNameLabel()
        self.ButtonAddClass()
        self.ButtonRecord()
        self.ButtonTrain()
        self.Button_Message_Signal_Trained()
        
        # enabling the train button here. 
        #----------------------------------------------------------------------
        global live_record_stop
        
        if(live_record_stop == 1):
            # Enabling the "TRAINING" button.
            self.button_train.setEnabled(True)
            self.button_train.setToolTip('Data collected, click to start training.       ')
            self.button_train.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
                    
            live_record_stop = 0
             
        else:
            # disabling the "TRAINING" button.
            self.button_train.setToolTip('Train button is currently disabled.   ')
            self.button_train.setEnabled(False)
            self.button_train.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)        
         
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
         
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
#############################################  CLOSE EVENT FOR MAIN WINDOW   ################################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #    
    
    def closeEvent(self, event):
        global close_main_window
        
        self.label_blur_img.show()
        msgBox = QMessageBox.question(self, 'End the Service', 'Do you really want to quit ?\t',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        if msgBox == QMessageBox.Yes:
            try:
                close_main_window = 1
                print('close through IF_NO_CLASS')
                            
            except:
                pass
        else:
            event.ignore()
        
        self.label_blur_img.hide()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
#####################################################  Constant Label Definiton    ##########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#                
    def ConstantLabel(self):
        
        self.Label_title.setText("")
        self.Label_title.resize(400, 100)
        self.Label_title.move(0, 0)
        self.Label_title.setObjectName("inc_title")
        
        self.Label_body.setText("")
        self.Label_body.resize(400, 240)
        self.Label_body.move(0, 80)
        self.Label_body.setObjectName("inc_body")
        
        self.Label_footer.setText("")
        self.Label_footer.resize(400, 80)
        self.Label_footer.move(0, 330)
        self.Label_footer.setObjectName("inc_footer")
              
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#####################################################  Animated file displaying    ##########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#                
    
    def AnimationImage(self):    
        self.Label_ani = QLabel(self)
        self.Label_ani.resize(400, 260)
        self.Label_ani.move(10, 49)
        
        movie = QMovie("assets/notfound.gif")
        self.Label_ani.setMovie(movie)
        movie.start()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
#########################################################  label displaying    ##############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#                
    
    def ClassNameLabel(self):
        
        self.Label_title_text.setText('EMPTY MODEL')
        self.Label_title_text.setObjectName("Label_title_text")
        self.Label_title_text.resize(240, 50)
        self.Label_title_text.move(90, 0)
        
        self.Label_title_sub_text.setText('Upload some data to continue using the service.')
        self.Label_title_sub_text.setObjectName("Label_title_sub_text")
        self.Label_title_sub_text.resize(300, 20)
        self.Label_title_sub_text.move(50, 40)

# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################  Name impout and providing data from the disk for training     #######################################
# ------------------------------------------------------------------------------------------------------------------------------------------#                

    def ClassNameTextBox(self):
        self.classNameText = QLineEdit(self)
        self.classNameText.setPlaceholderText("Enter the class name")
        self.classNameText.setObjectName("inc_classNameText")
        self.classNameText.move(80,280)
        self.classNameText.resize(240,30)

    def UploadTheFile(self):
        
        global className
        self.label_blur_img.show()
        
        # opening the dialog for selecting the file location.
        # If you want to add all file the add this "All Files (*);; before Audio Files (*.wav).
        #-----------------------------------------------------------------------------------------
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Gunshot Detection", "","Audio Files (*.wav)", options=options)
        
        # If file get selected then only it creates the folder directory.
        #----------------------------------------------------------------------
        if fileName:
 
            className = className.lower()

            if(os.path.isdir('audio/'+ className) == True):
                
                # remove folder an its contents.
                #--------------------------------------------------------------
                shutil.rmtree('audio/'+ className +'/'+ className)
                shutil.rmtree('audio/'+ className)
    
                os.makedirs('audio/'+ className)
                os.makedirs('audio/'+ className +'/'+ className)

            else:
                os.makedirs('audio/'+ className)
                os.makedirs('audio/'+ className +'/'+ className)
                
            # exporting the file to the location as defined above.
            #------------------------------------------------------------------
            audio = AudioSegment.from_wav(fileName)
            audio.export('audio/'+ className +'/'+ className +'.wav', format='wav')  
            
            # displaying the message that data successfully added.
            #------------------------------------------------------------------
            x = " Data successfully added. \n Now, click on the 'TRAINING' button to train the model.\t"
            QMessageBox.information(self, 'Message', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
        
            # enabling the TRAINING button after adding the file into the model.
            #-------------------------------------------------------------------
            self.button_train.setEnabled(True)
            self.button_train.setToolTip('Data added, click to start training.   ')
            self.button_train.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                                        QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                                        QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
                   

            
        self.label_blur_img.hide()
    
    # button for add data.
    #--------------------------------------------------------------------------     
    def ButtonAddClass(self):
        self.button_addClass = QPushButton('ADD DATA',self)
        self.button_addClass.setToolTip('Click to add data.    ')
        self.button_addClass.setObjectName("inc_enabled")
        self.button_addClass.setProperty('Test', True)
        self.button_addClass.resize(110,40)
        self.button_addClass.move(20,340)
        self.button_addClass.clicked.connect(self.on_click_addClass)
    
    def on_click_addClass(self):
        
        global className
        
        self.label_blur_img.show()
        
        # storing the class name into the variable className.
        #----------------------------------------------------------------------
        className = self.classNameText.text()
        
        # checking with the regular expression that name is in the correct format.
        #-------------------------------------------------------------------------
        if (re.fullmatch(r"[a-z]+", className)):
             
            # getting the file location
            #------------------------------------------------------------------
            self.UploadTheFile()
                        
        else:
            x = ' Enter the Class Name in the format.\t\t       \n\n 1)  Must be in small letters. \n 2)  Name must have letters only. \n 2)  Dont provide space betwwen the words.'
            QMessageBox.critical(self, 'Live Recording.', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))  
        
        self.label_blur_img.hide()
      
      
# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################  RECORD BUTTON which open up the Recording window     ################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#                
 
    # button for record data.
    #--------------------------------------------------------------------------
    def ButtonRecord(self):
        self.button_record = QPushButton('RECORD',self)
        self.button_record.setToolTip('Click to start recording.   ')
        self.button_record.setObjectName("inc_enabled")   
        self.button_record.setProperty('Test', True)
        self.button_record.resize(120,40)
        self.button_record.move(140,340)
        self.button_record.clicked.connect(self.on_click_record)
    
    def on_click_record(self):  
        global className
        self.label_blur_img.show()
        
        className = self.classNameText.text()
        
        # checking with the regular expression that name is in the correct format.
        #-------------------------------------------------------------------------
        if (re.fullmatch(r"[a-z]+", className)):
            
            # hiding the checkAvailabiolityWindow
            #------------------------------------------------------------------
            self.hide()
            
            # opening the live Recording Dialog for recording.
            #------------------------------------------------------------------          
            from Gunshot_Detection_WINDOW_LIVE_RECORDING import LiveRecordingDialog
            self.dialog = LiveRecordingDialog(className, self)
            self.dialog.exec_() 
            
            
            # enabling and disabling the train button here.
            #------------------------------------------------------------------
            import Gunshot_Detection_WINDOW_TRAIN
            if(Gunshot_Detection_WINDOW_TRAIN.live_record_stop == 1):
                self.button_train.setEnabled(True)
                self.button_train.setStyleSheet(""" QPushButton{color:#ffffff; background-color:#000000; font-weight:bold; border-radius:10px;} 
                                            QPushButton:hover{color:#ffffff; background-color:#054A73; font-size:13px; font-weight:bold; border-radius:10px; border: 1.5px solid #ffffff;}
                                            QPushButton:pressed{color:#000000; background-color:#35BEF4; border-radius:10px; border: 1.5px solid #000000;} """)
            else:
                self.button_train.setEnabled(False)
                self.button_train.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)
                            
            self.show()
                      
        else:
            x = ' Enter the Class Name in the format.\t\t       \n\n 1)  Must be in small letters. \n 2)  Name must have letters only. \n 2)  Dont provide space betwwen the words.'
            QMessageBox.critical(self, 'Live Recording.', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
        
        self.label_blur_img.hide()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
######################################  TRAINING BUTTON which open up the Recording window     ##############################################
# ------------------------------------------------------------------------------------------------------------------------------------------#                

    # button to train the model.
    #--------------------------------------------------------------------------
    def ButtonTrain(self):
        self.button_train = QPushButton('TRAINING',self)
        self.button_train.setEnabled(False)
        self.button_train.setToolTip('Currently unavailable.    ')
        self.button_train.setStyleSheet(""" QPushButton{color:#000000; background-color:#6B6B6B; border-radius:10px;} """)
        self.button_train.resize(110,40)
        self.button_train.move(270,340)
        self.button_train.clicked.connect(self.on_click_train)
    
    def on_click_train(self):
        global className
        self.label_blur_img.show()        
                
        # poping up the message box to do training
        #----------------------------------------------------------------------
        msgBox = QMessageBox.question(self, 'Model Training', ' Do you really want to train the model with the available data?\t \n Once training get strated you cannot go back.    ', QMessageBox.Yes, QMessageBox.No)        
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        if msgBox == QMessageBox.Yes:
                              
            # writing name into the CSV file.
            #------------------------------------------------------------------
            from Gunshot_Data_CSV import updateTrainClass
            updateTrainClass(className)
            
            # poping up the progressbar window here.
            #------------------------------------------------------------------
            from Gunshot_Recognition_PROGRESS_BAR import TrainingProgressBarSmall
            self.dialog_training = TrainingProgressBarSmall(self)
            self.dialog_training.show()
            
            # hiding empty model window and main window.
            #------------------------------------------------------------------
            self.hide()

            # to start training in the background.            
            #------------------------------------------------------------------
            self.TrainingLoop()  

        else:
            #event.ignore()
            print('exit')      
        
        self.label_blur_img.hide()              

# ------------------------------------------------------------------------------------------------------------------------------------------#    
################################################  THREAD WITH TRAINING LOOP   ###############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#       
    
    # thread to start the training.
    #--------------------------------------------------------------------------
    def TrainingLoop(self): 
        thread_train = Timer(1, self.do_training_loop)
        thread_train.daemon = True
        thread_train.start()                             
        
    # Definition contains do training part and button enabling.
    #--------------------------------------------------------------------------
    def do_training_loop(self):
 
        # calling training method from Gunshot_Recognition_CNN.py
        #----------------------------------------------------------------------
        from Gunshot_Recognition_CNN import do_training
        do_training()
        print('Training completed')
                                     
        # going back to the Training window and hiding the Progress bar window.
        #----------------------------------------------------------------------
        self.dialog_training.close()
        print('Training progress bar closed')
        
        # send signal for click the button here to pop up the message.
        #----------------------------------------------------------------------
        self.button_xxx.click()
        print('button clicked')

    # Here i have created the hidden button in the training window so, when we come back from the training
    # the message 'successfully' trained will appear and for that we have auto-click event in above do_training_loop.
    #----------------------------------------------------------------------------------------------------------------         
    def Button_Message_Signal_Trained(self):
        self.button_xxx= QPushButton('',self)
        self.button_xxx.setStyleSheet("background: transparent")   
        self.button_xxx.resize(0,0)
        self.button_xxx.move(0,0)
        self.button_xxx.clicked.connect(self.send_signal_trained)
       
    def send_signal_trained(self): 
        print('\n send_signal_trained under 354')
            
        
        x = " Model Trained Successfully, Click 'OK' to go back.       \n\n 1) You can add more data and retrain the model. \n 2) You can do recognition with current trained model. \t"
        QMessageBox.information(self, 'Training Completed.', x , QMessageBox.Ok)
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        print('empty call window is called.\n')
        
        # hiding the blur image in the main window here.
        #----------------------------------------------------------------------
        global close_main_window
        close_main_window = 2
        print('Hiding main window')     
                                                  
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
#        window =  CheckingClassAvailability()
#        window.show()
#
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except:
#    print('\nSERVICE SHUTDOWN')
#    
