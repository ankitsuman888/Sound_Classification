from threading import Timer
from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QPushButton, QSystemTrayIcon, QVBoxLayout, QWidget, QDialog, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QGuiApplication, QIcon, QImage, QPalette, QBrush, QMovie
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSize, QDateTime, Qt, QSettings, QPoint
import sys
import time

# for pyinstaller.
#------------------------------------------------------------------------------
import sklearn.neighbors.typedefs
import sklearn.neighbors.quad_tree
import sklearn.tree
import sklearn.tree._utils

 
class StartWait(QMainWindow):
    
    def __init__(self):

        QMainWindow.__init__(self)
        
        self.setFixedSize(350, 150)

        self.setWindowTitle(' Sound Classification v3.0 ')
        self.setWindowIcon(QIcon('assets/icon.png'))
        
        # make transparent background only gif will be visible.
        #----------------------------------------------------------------------
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setWindowOpacity(0.5)
        #self.setAttribute(Qt.WA_NoSystemBackground)
        
        # remove icon from taskbar.
        #----------------------------------------------------------------------
        #self.setWindowFlags(Qt.Tool)
        #self.setVisible(False)
        
        # removing the windows title bar
        #----------------------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # no minimized window.
        #----------------------------------------------------------------------
        self.setWindowState(Qt.WindowNoState)
        #self.setWindowState(Qt.WindowActive)

        # please wait label.
        #----------------------------------------------------------------------
        self.Label_pw = QLabel(self)
        self.Label_pw.setText("Please Wait")
        self.Label_pw.resize(360, 30)
        self.Label_pw.setAlignment(Qt.AlignCenter)
        self.Label_pw.setStyleSheet("font-size:30px; font-weight:bold; color:#28ADDD")                
        
        # progress bar on app start-up.
        #----------------------------------------------------------------------
        self.Label_ani = QLabel(self)
        self.Label_ani.resize(350, 65)
        self.Label_ani.move(0, 30)
        movie = QMovie("assets/progressBar.gif")
        self.Label_ani.setMovie(movie)
        movie.start()

            
        # button definition to close the StartWait window
        #----------------------------------------------------------------------
        self.button_close= QPushButton('',self)
        self.button_close.setStyleSheet("background:transparent")   
        self.button_close.resize(0,0)
        self.button_close.move(0,0)
        self.button_close.clicked.connect(self.send_signal_close)
        
        # running thread here.
        #----------------------------------------------------------------------
        self.thread_running_keras()
                                
    def send_signal_close(self):       
        try:
            print('signal send successfully !')
            self.hide()
                        
            print('Now opening Main Application.')
            from Gunshot_Detection_WINDOW_MAIN import MainWindow
            self.dialog = MainWindow()
            self.dialog.show()
    
        except Exception as e:
            print('error occured ',e)
 
    # import keras in thread so that when application run it will take less time in startup.
    #---------------------------------------------------------------------------------------
    def load_keras(self):
        
        # here we are using while loop because we want to load keras only once.
        #----------------------------------------------------------------------
        while(True):
            import keras
            import tensorflow
                        
            # here we want to close the StartWait window.
            print('tensorflow loaded sucessfuilly!')
            
            # remember whenever defining the button.click(), keep it always inisde the same class.
            #-------------------------------------------------------------------------------------
            #self.button_close.animateClick()
            self.button_close.click()
            
            print('button clicked')                                 
            break
               
    def thread_running_keras(self):                        
        
        # running thread to load keras module.
        #----------------------------------------------------------------------
        thread_keras = Timer(0, self.load_keras)
        thread_keras.daemon = True
        thread_keras.start()
    
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
 
def run():
    if __name__ =='__main__':
                
        QApplication.processEvents()
        QCoreApplication.processEvents()
        
        my_app = QCoreApplication.instance()        
        if my_app is None:
            my_app = QApplication(sys.argv)                        
        window = StartWait()
        window.show()
            
        sys.exit(my_app.exec_())

try:
    run()
except:
    print('\nSERVICE SHUTDOWN\n')
    