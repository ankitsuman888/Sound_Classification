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


######################################################################################################################################
########################   Advance setting Dialog Windows for changing themes, cleaning data, dummy data generation    ###############  
######################################################################################################################################


class SetNotificationWindow(QDialog):
       
    def __init__(self, parent=None):
        
        # to prevent GUI lockup in long run.
        #----------------------------------------------------------------------
        QApplication.processEvents()
        
        QDialog.__init__(self, parent)
        #super(AdvanceSettingWindow, self).__init__(parent)
        self.setFixedSize(500, 400)
        self.setWindowTitle(' Set Notification')
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
        self.Label_sbg.resize(450, 265)
        self.Label_sbg.move(25, 60)
        self.Label_sbg.setStyleSheet("background-color:#50000000; border-radius:10px")
        
        # setting '?' text.
        #----------------------------------------------------------------------        
        self.setWhatsThis("This dialog allows to set the notification for certain class \nand notification can be received to the registered phone \nnumber and email address.")
        
        # setting title text image here {'set notification for'}.
        #----------------------------------------------------------------------
        self.Label_title_ani = QLabel(self)
        self.Label_title_ani.resize(420, 55)
        self.Label_title_ani.move(120, 5)
        
        movie = QMovie("assets/notiTitle.png")
        self.Label_title_ani.setMovie(movie)
        movie.start()
                    
        self.initUI()
        
        # calling stylesheet here.
        #----------------------------------------------------------------------        
        from Gunshot_Recognition_CSS import styleSheetNotification
        self.setStyleSheet(styleSheetNotification)       


# ------------------------------------------------------------------------------------------------------------------------------------------#    
##################################################  init FUNCTION OF CLASS   ################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
           
    def initUI(self):
        self.InputBoxNotification()
        self.ButtonSetNotification()
        self.setNotification()
                
        # self.show     ---> background window will not movable.
        # self.show()   ---> background window will be movable.

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  close event   #####################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    def closeEvent(self, event):

        self.hide()
        
        from Gunshot_Detection_WINDOW_ADVANCE_SETTING import AdvanceSettingWindow
        self.dialog = AdvanceSettingWindow(self)
        self.dialog.exec_()
 
#        QMainWindow.closeEvent(self, event)
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################    Displaying the current class, email_Id and phone_number    #########################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
            
    # Displaying current notification set for
    def InputBoxNotification(self):
        
        ss = "color:#000000; font-size:15px; font-weight:bold"
        
        # setting text for the option.          
        self.Label_text1 = QLabel(self)              
        self.Label_text1.setText(' Class Name        :')
        self.Label_text1.resize(160, 30)
        self.Label_text1.move(50, 108)
        self.Label_text1.setStyleSheet(ss)
            
        self.Label_text1 = QLabel(self)              
        self.Label_text1.setText(' Email ID              :')
        self.Label_text1.resize(160, 30)
        self.Label_text1.move(50, 195)
        self.Label_text1.setStyleSheet(ss)
            
        self.Label_text1 = QLabel(self)              
        self.Label_text1.setText(' Phone Number  :')
        self.Label_text1.resize(160, 30)
        self.Label_text1.move(50, 280)
        self.Label_text1.setStyleSheet(ss)
        
        styleSheet = "background-color:#000000; color:#808080; border-radius:10px; padding-left:0px; font-size:15px; font-weight:bold"
        
        from Gunshot_Detection_DATA_SAVING import DisplayDataNotification
        data = DisplayDataNotification()
        
        x = data[0]
        y = data[1]
        z = data[2]
        
        width = 400
        height = 25
        
        x_axis = 50
        
        self.Label_className = QLabel(self)
        self.Label_className.setText(x)
        self.Label_className.setStyleSheet(styleSheet)
        self.Label_className.move(x_axis, 79)
        self.Label_className.resize(width,height)
        self.Label_className.setWhatsThis(x)
        self.Label_className.setAlignment(Qt.AlignCenter)
        
        self.Label_email = QLabel(self)
        self.Label_email.setText(y)
        self.Label_email.setStyleSheet(styleSheet)
        self.Label_email.move(x_axis, 167)
        self.Label_email.resize(width,height)
        self.Label_email.setWhatsThis(y)
        self.Label_email.setAlignment(Qt.AlignCenter)
        
        self.Label_phone = QLabel(self)
        self.Label_phone.setText(z)
        self.Label_phone.setStyleSheet(styleSheet)
        self.Label_phone.move(x_axis, 252)
        self.Label_phone.resize(width,height)
        self.Label_phone.setWhatsThis(z)
        self.Label_phone.setAlignment(Qt.AlignCenter)
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
##############################   Defining the imput box for email_ID & Phone Number and ComboBox selection here    ###################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
 
    # Defining input box for class name, email Id, phone Number. 
    #--------------------------------------------------------------------------
    def setNotification(self):
        
        styleSheet = "color:#0E86B2; background-color:#000000; border-radius:0px; font-size:15px; font-weight:bold"
        width = 250
        height = 25
                    
        # Defining the text box input for the EMAIL ID.      
        #----------------------------------------------------------------------
        self.textbox_email = QLineEdit(self)
        self.textbox_email.setStyleSheet(styleSheet)
        self.textbox_email.move(200, 198)
        self.textbox_email.resize(width,height)
        self.textbox_email.setAlignment(Qt.AlignCenter)

        # Defining the text box input for the PHONE NUMBER.
        #----------------------------------------------------------------------        
        self.textbox_phone = QLineEdit(self)
        self.textbox_phone.setStyleSheet(styleSheet)
        self.textbox_phone.move(200, 283)
        self.textbox_phone.resize(width,height)
        self.textbox_phone.setAlignment(Qt.AlignCenter)
                
        # Initially the ComboBox text is NONE so diabling the input box.
        #----------------------------------------------------------------------
        self.textbox_phone.setDisabled(True)
        self.textbox_phone.setPlaceholderText("Currently Not Available.")
        self.textbox_email.setDisabled(True)
        self.textbox_email.setPlaceholderText("Currently Not available.")
        
        # Defining the drop box and class Name selection is taken from the 'audio/classes.csv'.
        #----------------------------------------------------------------------
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("NONE")
        self.comboBox.move(200, 110)
        self.comboBox.resize(width,height)
        self.comboBox.setStyleSheet("color:#0E86B2; background-color:#000000; border-radius:0px; padding-left:20px; font-size:15px; font-weight:bold")


        # Now adding the element from the CSV file.
        #----------------------------------------------------------------------
        with open('audio/classes.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader, None)                                                  # skipping header
            for row in reader:
                print(row)
                self.comboBox.addItem(row[1])
        
        self.comboBox.activated[str].connect(self.on_select_ComboBox) 
        
    # taking input from QComboBox.
    #--------------------------------------------------------------------------
    def on_select_ComboBox(self, text):
        self.comboBox_text = text
            
        if(text == 'NONE'):
            # Disabling the email and phone textbox input.
            #------------------------------------------------------------------
            self.textbox_phone.setDisabled(True)
            self.textbox_phone.setPlaceholderText("Currently Not Available.")
            self.textbox_email.setDisabled(True)
            self.textbox_email.setPlaceholderText("Currently Not available.")
        
        else:
            # Enabling the email and phone textbox input.
            #------------------------------------------------------------------
            self.textbox_phone.setDisabled(False)
            self.textbox_phone.setPlaceholderText("Enter the Phone Number.")
            self.textbox_email.setDisabled(False)
            self.textbox_email.setPlaceholderText("Enter the Email ID.")
        
# ------------------------------------------------------------------------------------------------------------------------------------------#    
##################################################  SET BUTTON FUNCTIONALITY   ##############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
        
    # Button to set class name, phone number, email id for notification.
    #--------------------------------------------------------------------------
    def ButtonSetNotification(self):
        self.button_noti = QPushButton('SET',self)
        self.button_noti.setToolTip('Enter the value and click to set the notification.\t          ')
        self.button_noti.setObjectName("enabledNoti")   
        self.button_noti.resize(120,40)
        self.button_noti.move(185,340)
        self.button_noti.clicked.connect(self.on_click_notification)
        
        # setting the question masrk (what is this).
        #----------------------------------------------------------------------
        self.button_noti.setWhatsThis("set button")
        
    # This click event is used for going back to the main window.
    #--------------------------------------------------------------------------
    def on_click_notification(self):
        
        # showinging the blur image over the background.
        #----------------------------------------------------------------------
        self.label_blur_img = QLabel(self)
        color = QColor(0, 0, 0, 200)                                            # rgba color code here.
        pixmap = QPixmap(1000, 500)
        pixmap.fill(color)
#        pixmap = QPixmap('assets/pg_bg1.png')
        self.label_blur_img.setPixmap(pixmap)
        self.label_blur_img.resize(1000,500)        
        self.label_blur_img.show()
        
        # initially we have nothing selected so, we get error when we click on 'SET button'.
        # so handling this by putting in the try excpet block.
        #----------------------------------------------------------------------
        try:      
            self.Class = self.comboBox_text
        except:
            self.Class = 'NONE'
            
        self.Email = self.textbox_email.text()
        self.Phone = self.textbox_phone.text()
        
        self.Email = str(self.Email)
        self.Phone = str(self.Phone)
        
        i = 0
        
        # Class Name from the the drop down menu
        #----------------------------------------------------------------------
        className = self.Class
        
        # 1) If class Name in the drop down is selectes as None then, we are not sending any notification.
        # and we are setting everything as NULL.
        #----------------------------------------------------------------------
        if (className == 'NONE'):
            
            self.Class = 'NULL'
            self.Email = 'NULL'
            self.Phone = 'NULL'            
            
            print('Data collected succesfully |',self.Class, self.Email, self.Phone)
                        
            # here writing data into the csv.
            #----------------------------------------------------------------------
            print('Writing data into the CSV.')
            from Gunshot_Detection_DATA_SAVING import saving_data_notification
            saving_data_notification(self.Class, self.Email, self.Phone)
            
            # poping up the message for diabling the notification.
            #--------------------------------------------------------------             
            x = 'Success !'
            y = 'Notification successfully disabled \t'
            QMessageBox.information(self, x, y , QMessageBox.Ok)
            self.setWindowIcon(QIcon('assets/icon.png'))
            
            # closing the dialog.
            self.close()
        

        # 2) Display class name and send notification only to email ID.
        #----------------------------------------------------------------------
        elif(self.Class !='NONE' and self.Email !='' and self.Phone ==''):
            
            self.Phone = 'NULL' 
            
            # Regular expression for emial id.
            #------------------------------------------------------------------
            if (re.fullmatch(r"([a-zA-Z0-9.^~&*%$#!_-]+)@([a-zA-Z0-9]+).([a-zA-Z]{2,3}|[0-9]{1,3})", self.Email)):
                i = i + 1
                        
            if(i == 1):
                                
                print('Data collected succesfully |',self.Class, self.Email, self.Phone)
                
                # here writing data into the csv.
                #--------------------------------------------------------------
                print('Writing data into the CSV.')
                from Gunshot_Detection_DATA_SAVING import saving_data_notification
                saving_data_notification(self.Class, self.Email, self.Phone)
                
                i = 0
                                
                # poping up the message for the successfully written the data in to the csv.
                #--------------------------------------------------------------             
                x = 'Data Added Successfully'
                y = 'Notification avtivated for '+ self.Class +'  \nfor the EMAIL ID : '+self.Email+'\t'
                QMessageBox.information(self, x, y , QMessageBox.Ok)
                self.setWindowIcon(QIcon('assets/icon.png'))
                
                # closing the dialog.
                self.close()
            
            else:
                # displaying message if wrong value is given for threshold frequency.
                #----------------------------------------------------------------------
                x = ' Enter data in the correct format as given.\t'
                x = x + '\n\n 1) Email ID     :  xxxxx@xxxxxx.xxx'
                x = x + '\n 2) Phone No  :  xxxxxxxxxx (upto 10)'
        
                QMessageBox.critical(self, 'Wrong format', x , QMessageBox.Ok)
                self.setWindowIcon(QIcon('assets/icon.png'))
                                
                i = 0

             
            
        # 3) Display class name and send notification only to Mobile.
        #----------------------------------------------------------------------
        elif(self.Class !='NONE' and self.Email =='' and self.Phone !=''):
            
            self.Email = 'NULL'
            
            # Regular expression for phone number.
            #------------------------------------------------------------------
            if (re.fullmatch(r"[0-9]{10}", self.Phone)):
                i = i + 1
                        
            if(i == 1):
                                
                print('Data collected succesfully |',self.Class, self.Email, self.Phone)
                
                # here writing data into the csv.
                #--------------------------------------------------------------
                print('Writing data into the CSV.')
                from Gunshot_Detection_DATA_SAVING import saving_data_notification
                saving_data_notification(self.Class, self.Email, self.Phone)
                
                i = 0
                                
                # poping up the message for the successfully written the data in to the csv.
                #--------------------------------------------------------------             
                x = 'Data Added Successfully'
                y = 'Notification avtivated for '+ self.Class +'  \nfor the PHONE NUMBER : '+self.Phone+'  \t'
                QMessageBox.information(self, x, y , QMessageBox.Ok)
                self.setWindowIcon(QIcon('assets/icon.png'))
                
                # closing the dialog.
                self.close() 
            
            else:
                # displaying message if wrong value is given for threshold frequency.
                #----------------------------------------------------------------------
                x = ' Enter data in the correct format as given.\t'
                x = x + '\n\n 1) Email ID     :  xxxxx@xxxxxx.xxx'
                x = x + '\n 2) Phone No  :  xxxxxxxxxx (upto 10)'
        
                QMessageBox.critical(self, 'Wrong format', x , QMessageBox.Ok)
                self.setWindowIcon(QIcon('assets/icon.png'))
                                
                i = 0
            
        # 4) Display class name and send notification both Mobile and Email ID.
        #----------------------------------------------------------------------
        else:
            
            # Regular expression for emial id.
            #------------------------------------------------------------------
            if (re.fullmatch(r"([a-zA-Z0-9.^~&*%$#!_-]+)@([a-zA-Z0-9]+).([a-zA-Z]{2,3}|[0-9]{1,3})", self.Email)):
                i = i + 1
            
            # Regular esxpression for Phone number.
            #------------------------------------------------------------------
            if (re.fullmatch(r"[0-9]{10}", self.Phone)):
                i = i + 1
            
            if(i == 2):
                                
                print('Data collected succesfully |',self.Class, self.Email, self.Phone)
                
                # here writing data into the csv.
                #--------------------------------------------------------------
                print('Writing data into the CSV.')
                from Gunshot_Detection_DATA_SAVING import saving_data_notification
                saving_data_notification(self.Class, self.Email, self.Phone)
                
                i = 0
                                
                # poping up the message for the successfully written the data in to the csv.
                #--------------------------------------------------------------             
                x = 'Data Added Successfully'
                y = 'Sending Notification for class : \''+ self.Class +'\' on \t\t\n\n 1) Email   : \t'+ self.Email +' \n 2) Phone  :\t'+self.Phone
                QMessageBox.information(self, x, y , QMessageBox.Ok)
                self.setWindowIcon(QIcon('assets/icon.png'))
                
                # closing the dialog.
                self.close()
                                                   
            else:
                # displaying message if wrong value is given for threshold frequency.
                #----------------------------------------------------------------------
                x = ' Enter data in the correct format as given.\t'
                x = x + '\n\n 1) Email ID     :  xxxxx@xxxxxx.xxx'
                x = x + '\n 2) Phone No  :  xxxxxxxxxx (upto 10)'
        
                QMessageBox.critical(self, 'Wrong format', x , QMessageBox.Ok)
                self.setWindowIcon(QIcon('assets/icon.png'))
                                
                i = 0
                        
        self.label_blur_img.hide()
        

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
#        window = SetNotificationWindow()
#        window.show()
#            
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except:
#    print('\nSERVICE SHUTDOWN\n')