import sys
import os
import csv
from PyQt5.Qt import QApplication, QClipboard, QImage, QPalette, QBrush, QIcon, QDialog, QCoreApplication, QLabel, QColor, QMovie
from PyQt5 import QtCore, QtWidgets 
from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import QSize

class TotalClassAvailable(QDialog):
    def __init__(self, parent=None):

        # to prevent GUI lockup in long run.
        #----------------------------------------------------------------------
        QApplication.processEvents()        
        
        QDialog.__init__(self, parent)

        self.setFixedSize(QSize(500, 400))    
        self.setWindowTitle("Classes Availability")
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
        
        # Sub Background part with transparency.
        #----------------------------------------------------------------------
        self.Label_sbg = QLabel(self)              
        self.Label_sbg.setText('')
        self.Label_sbg.resize(450, 320)
        self.Label_sbg.move(25, 60)
        self.Label_sbg.setStyleSheet("background-color:#50000000; border-radius:10px")
            
        
        # reading the csv for findinout the total class available.
        #----------------------------------------------------------------------
        class_sound = ''
        with open('audio/classes.csv', 'r') as file:
            # skipping the header of the csv file.
            f_csv = csv.reader(file) 
            next(f_csv) # can access the header by  header = next(f_csv)
            
            class_sound = '\tId    \t\tName \n           ' + '----------------'*3
            
            reader = csv.reader(file)
            for row in reader:
                class_sound  = class_sound + '\n\t'+row[0]+' :\t\t'+row[1]


        # Adding text field here.
        #----------------------------------------------------------------------
        self.b = QPlainTextEdit(self)
               
        # self.b.setDisabled(True)
        self.b.setReadOnly(True)                                                 # Read only.               
        self.b.insertPlainText("\n")
        
        self.b.setStyleSheet("color:#91000C; font-size:15px; font-weight:bold; background-color:#000000")
        
        self.b.insertPlainText(class_sound)
        self.b.move(50,80)
        self.b.resize(400,280)


        # class header text.
        #----------------------------------------------------------------------
        x = '       Total Classes Available : '
        self.header = QLabel(self)
        self.header.setText(x)
        self.header.resize(340, 25)
        self.header.move(70, 15)
        self.header.setStyleSheet("color:#000000; font-size:20px; font-weight:bold")
 
        self.numClass = QLabel(self)    
        self.numClass.setText(row[0])
        self.numClass.resize(25, 25)
        self.numClass.move(360, 16)
        self.numClass.setStyleSheet("color:#91000C; font-size:20px; font-weight:bold")


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
#        window = TotalClassAvailable()
#        window.show()
#            
#        sys.exit(my_app.exec_())
#
#try:
#    run()
#except:
#    print('\nSERVICE SHUTDOWN\n')