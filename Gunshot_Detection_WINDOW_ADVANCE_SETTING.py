# -*- coding: utf-8 -*-
import sys 
import re
import os
from threading import Timer, Thread

from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton,QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QMovie, QPixmap, QColor
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint

from Gunshot_Clean_Model import clean_classData, clean_evidence, clean_notification_data


######################################################################################################################################
########################   Advance setting Dialog Windows for changing themes, cleaning data, dummy data generation    ###############  
######################################################################################################################################


class AdvanceSettingWindow(QDialog):
       
    def __init__(self, parent=None):
        
        # to prevent GUI lockup in long run.
        #----------------------------------------------------------------------
        QApplication.processEvents()
        
        QDialog.__init__(self, parent)
        #super(AdvanceSettingWindow, self).__init__(parent)
        self.setFixedSize(500, 400)
        self.setWindowTitle(' Advance Settings')
        self.setWindowIcon(QIcon('assets/icon.png'))

        # if background image is not available then takin color as background.
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
            color = QColor("#2d2d2d")
            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), color)
            self.setPalette(p)
        
            
        # Sub Background part with transparency at the middle notification
        #----------------------------------------------------------------------
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(425, 160)
        self.Label_sbg.move(40, 120)
        self.Label_sbg.setStyleSheet("background-color:#50000000; border-radius:10px; border: 0px solid #000000")
        
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(425, 50)
        self.Label_sbg.move(40, 120)
        self.Label_sbg.setStyleSheet("background-color:#000000; border-top-left-radius:10px; border-top-right-radius:10px")
            
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(425, 30)
        self.Label_sbg.move(40, 250)
        self.Label_sbg.setStyleSheet("background-color:#000000; border-bottom-left-radius:10px; border-bottom-right-radius:10px")
                      
        # setting title text image here {'set notification for'}.
        #----------------------------------------------------------------------
        self.Label_title_ani = QLabel(self)
        self.Label_title_ani.resize(420, 55)
        self.Label_title_ani.move(120, 120)
        movie = QMovie("assets/notiTitle.png")
        self.Label_title_ani.setMovie(movie)
        movie.start()
        
        # setting text for the option.
        #----------------------------------------------------------------------
        ss = "color:#000000; font-size:16px; font-weight:bold; background-color:#0D86B1; border-radius:10px; border: 3px solid #000000"
        
        width = 425
        height = 35
        
        x_axis = 40
        y_axis = 25
        
        self.Label1 = QLabel(self)              
        self.Label1.setText('   Clean Model Data                :')
        self.Label1.resize(width, height)
        self.Label1.move(x_axis,  y_axis)
        self.Label1.setStyleSheet(ss)
            
        self.Label1 = QLabel(self)              
        self.Label1.setText('   Clean Evidence Data           :')
        self.Label1.resize(width, height)
        self.Label1.move(x_axis, y_axis + 45)
        self.Label1.setStyleSheet(ss)
        
        self.Label1 = QLabel(self)              
        self.Label1.setText('   Record Dummy Data           :')
        self.Label1.resize(width, height)
        self.Label1.move(x_axis, y_axis + 270)
        self.Label1.setStyleSheet(ss)
               
        self.Label2 = QLabel(self)              
        self.Label2.setText('   Set Notification                   :' )
        self.Label2.resize(width, height)
        self.Label2.move(x_axis, y_axis + 315)
        self.Label2.setStyleSheet(ss)

        # Blocking the the any other window. 
        ##############################################################################
        self.setWindowModality(Qt.ApplicationModal)
            
            
        # disabling minimize button.
        #----------------------------------------------------------------------
#        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        
#        self.settings = QSettings(" ", " ")
#        self.restoreGeometry(self.settings.value("geometry", ""))
#        self.restoreState(self.settings.value("windowState", ""))
    
            
        # displays the position of the window. (x, y, w, h) and extracting the values.
        # after extracting the value setting the position to the center of the parent.
        ##############################################################################
#        x = self.frameGeometry()        
#        x = str(x)
#        val = re.findall(r'\d+', x)
#        val = [int(val[1]), int(val[2])]
#        print(val)       
#        self.move(val[0]+260 , val[1]+100)
            
        self.initUI()
        
        # calling stylesheet here.
        #----------------------------------------------------------------------        
        from Gunshot_Recognition_CSS import styleSheetAdvanceSetting
        self.setStyleSheet(styleSheetAdvanceSetting)

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  close event   #####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#    def closeEvent(self, event):
#        
#        # here sending value to hide the blur image over the main window.
#        import Gunshot_Detection_WINDOW_MAIN
#        Gunshot_Detection_WINDOW_MAIN.main_advance_setting_close = 3
#        print('In advance setting close value: ',Gunshot_Detection_WINDOW_MAIN.main_advance_setting_close)
#        
#        QMainWindow.closeEvent(self, event)

# ------------------------------------------------------------------------------------------------------------------------------------------#    
##################################################  init FUNCTION OF CLASS   ################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
           
    def initUI(self):
        self.InputBoxNotification()
        self.ButtonSetNotification()
        self.ButtonDummyData()
        self.ButtonEvidenceData()
        self.ButtonModelData()
        
        # self.show     ---> background window will not movable.
        self.show()   # ---> background window will be movable.
        
        # defining the blur image over the background.
        self.label_blur_img = QLabel(self)
        color = QColor(0, 0, 0, 200)                                            # rgba color code here.
        pixmap = QPixmap(1000, 500)
        pixmap.fill(color)
#        pixmap = QPixmap('assets/pg_bg1.png')
        self.label_blur_img.setPixmap(pixmap)
        self.label_blur_img.resize(1000,500)

# ------------------------------------------------------------------------------------------------------------------------------------------#    
####################################################  NOTIFICATION BUTTON    ################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
    # Displaying current notification set for
    # -------------------------------------------------------------------------
    def InputBoxNotification(self):
        
        styleSheet = "color:#000000; border-radius:10px; font-size:40px; font-weight:bold"
        
        from Gunshot_Detection_DATA_SAVING import DisplayDataNotification
        data = DisplayDataNotification()
        x = data[0]
        
        self.Label_className = QLabel(self)
        self.Label_className.setText(x)
        self.Label_className.setStyleSheet(styleSheet)
        self.Label_className.setAlignment(Qt.AlignCenter)
        self.Label_className.move(50, 185)
        self.Label_className.resize(405,50)
                   
    # Button to set class name, phone number, email id for notification.
    def ButtonSetNotification(self):
        self.button_noti = QPushButton('SET',self)
        self.button_noti.setToolTip(' Set the notification.')
        self.button_noti.setObjectName("enabledAdvance")
        self.button_noti.resize(127,29)
        self.button_noti.move(335,343)
        self.button_noti.clicked.connect(self.on_click_notification)
        
    # This click event is used for going back to the main window.
    def on_click_notification(self):
        
        self.label_blur_img.show()   
        
        x = 'Set Notification'
        y = ' Do you really want to make changes to the notification.        '
        selection_sub = QMessageBox.information(self, x, y , QMessageBox.Yes, QMessageBox.No)
        self.setWindowIcon(QIcon('assets/icon.png')) 
                            
        if(selection_sub == QMessageBox.Yes):
            
            self.hide()
            
            from Gunshot_Detection_WINDOW_SET_NOTIFICATION import SetNotificationWindow
            self.dialog = SetNotificationWindow(self)
            self.dialog.exec_()           
        
        else:
            pass
        
        self.label_blur_img.hide()
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
####################################################   MODEL CLEAN BUTTON   #################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
   
    # all buttons for functionality
    #--------------------------------------------------------------------------
    def ButtonModelData(self):
        self.button_modelData = QPushButton('CLEAN',self)
        self.button_modelData.setToolTip('Clean the model data. ')
        self.button_modelData.setObjectName("enabledAdvance")  
        self.button_modelData.resize(127,29)
        self.button_modelData.move(335,28)
        self.button_modelData.clicked.connect(self.on_click_modelData)
        
    # button event for cleaning the model data.
    #--------------------------------------------------------------------------
    def on_click_modelData(self):       

        self.label_blur_img.show()
                    
        x = 'This will clean all the trained model data.        '
        selection_sub = QMessageBox.information(self, 'Clean The Model Data', x , QMessageBox.Yes, QMessageBox.No)
        self.setWindowIcon(QIcon('assets/icon.png')) 
                            
        if(selection_sub == QMessageBox.Yes):
            
            # calling the function cleanup function.
            #------------------------------------------------------------------
            clean_classData()     
            # calling function to clean the notification data.
            #------------------------------------------------------------------
            clean_notification_data()
            
            # displaying message box.
            #------------------------------------------------------------------
            x = 'All model data successfully cleared.       '
            QMessageBox.information(self, 'Message', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
            # closing advance setting window here. 
            #------------------------------------------------------------------
            self.close()

            # closing the mainwindow here by setting variable value as 1, 
            # which will get checked by in Main window under thread.
            #------------------------------------------------------------------
            import Gunshot_Detection_WINDOW_MAIN
            Gunshot_Detection_WINDOW_MAIN.main_advance_setting_close = 1
            print('In advance setting close value: ',Gunshot_Detection_WINDOW_MAIN.main_advance_setting_close)
            
            from Gunshot_Detection_WINDOW_MAIN import MainWindow
            self.dialog_main = MainWindow()
            self.dialog_main.show()
           
        else:
            pass
        
        self.label_blur_img.hide()

# ------------------------------------------------------------------------------------------------------------------------------------------#    
####################################################   EVIDENCE CLEAN BUTTON   ##############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

    def ButtonEvidenceData(self):
        self.button_evidenceData = QPushButton('CLEAN',self)        
        self.button_evidenceData.setToolTip('Clean the evidence. ')
        self.button_evidenceData.setObjectName("enabledAdvance")  
        self.button_evidenceData.resize(127,29)
        self.button_evidenceData.move(335,73)
        self.button_evidenceData.clicked.connect(self.on_click_evidence_data)
    
    # button event for cleaning the evidence data.
    def on_click_evidence_data(self):    

        self.label_blur_img.show()
            
        x = 'This will clean all the evidence data.     '  
        selection_sub = QMessageBox.information(self, 'Clean The Evidence Data', x , QMessageBox.Yes, QMessageBox.No)
        self.setWindowIcon(QIcon('assets/icon.png')) 
                            
        if(selection_sub == QMessageBox.Yes):

            # calling the function cleanup function.
            clean_evidence()            
            
            # displaying message box.            
            x = 'All evidence successfully cleared.       '
            QMessageBox.information(self, 'Message', x , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png')) 
                       
        else:
            pass
  
        self.label_blur_img.hide()
    
# ------------------------------------------------------------------------------------------------------------------------------------------#    
###################################################  DUMMY DATA RECORD BUTTON   #############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
  
    def ButtonDummyData(self):        
        self.button_dummyData = QPushButton('RECORD',self)        
        self.button_dummyData.setToolTip('Record dummy data. ')
        self.button_dummyData.setObjectName("enabledAdvance")   
        self.button_dummyData.resize(127,29)
        self.button_dummyData.move(335,298)
        self.button_dummyData.clicked.connect(self.on_click_dummyData)
        
    # here displaying the Dialog box for recording.        
    def on_click_dummyData(self): 

        self.label_blur_img.show()   
        
        x = 'Record Dummy Data'
        y = ' Do you really want to record dummy data.       '
        selection_sub = QMessageBox.information(self, x, y , QMessageBox.Yes, QMessageBox.No)
        self.setWindowIcon(QIcon('assets/icon.png')) 
                            
        if(selection_sub == QMessageBox.Yes):
            
            self.hide()
            
            from Gunshot_Detection_WINDOW_DUMMY_RECORDING import dummyRecordingClass
            self.dialog = dummyRecordingClass(self)
            self.dialog.exec_()           
        
        else:
            pass
        
        self.label_blur_img.hide()            


############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
 
def run():
    if __name__ =='__main__':
                
        QApplication.processEvents()        
        my_app = QCoreApplication.instance()        
        if my_app is None:
            my_app = QApplication(sys.argv)                        
        window = AdvanceSettingWindow()
        window.show()
            
        sys.exit(my_app.exec_())

try:
    run()
except:
    print('\nSERVICE SHUTDOWN\n')