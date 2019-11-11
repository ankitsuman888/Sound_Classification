import numpy as np
import random
import csv
import warnings
from PyQt5.QtCore import QDateTime

import keras
from keras.layers import Activation, Dense, Dropout, Conv2D, Flatten, MaxPooling2D
from keras.models import Sequential
from keras import backend as k
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot
from termcolor import colored
from Gunshot_Recognition_Augmentation import originalData, originalData_with_threshold, slowData, speedData, semitonesHigh, semitonesLow

warnings.filterwarnings('ignore')

# to get rid of the AVX2 instruction error.
# you can avoid the display by lowering the warning level by changing the environment setting 
# as follows before calling the execution class .
#--------------------------------------------------------------------------------------------
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Function for writing into the csv file.
#------------------------------------------------------------------------------
def update_training_CSV(Totaldata, NoClass, BatchSize, Epoches, TrainAcc, TestAcc, TrainLoss, TestLoss , DateTrain):
    with open('Data_Record/training_data_saved.csv', 'a') as IdData:
        IdData.write('\n{},{},{},{},{},{},{},{},{}'.format(Totaldata, NoClass, BatchSize, Epoches, TrainAcc, TestAcc, TrainLoss, TestLoss, DateTrain))

stop_training = 0

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
#####################################################  training with forced parameters  #####################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #   
 
def do_training():
        
    D = []
    number_of_class = 0
    
    # uploading the dummy data to the model.
    #--------------------------------------------------------------------------
    with open('audio/dummy_class.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        
        for row in reader:
            
            try:
                # selecting name and id
                #--------------------------------------------------------------
                name = row[1]
                classID = row[0]
                print (classID,'\t',colored(name,'red'))
                
                # generating the data for model.  
                #--------------------------------------------------------------
                originalData(name, classID, D)
                #slowData(name, classID, D)
                #speedData(name, classID, D)
                #semitonesHigh(name, classID, D)
                #semitonesLow(name, classID, D)
                
                # global class for counting number of classes available.
                #--------------------------------------------------------------
                number_of_class += 1
            
            except:
                print('header detected so passing it.\n')
                pass
        
    with open('audio/classes.csv', 'r') as f:
        reader = csv.reader(f)
        
        # skip the headers or the first row of the csv if 
        # we add it multiple times then it will remove multiple rows.
        #----------------------------------------------------------------------
        next(reader, None)    
        
        for row in reader:
            
            try:
                # selecting name and id
                #--------------------------------------------------------------
                name = row[1]
                classID = row[0]
                print (classID,'\t',colored(name,'cyan'))
                
                # generating the data for model.
                #--------------------------------------------------------------
                originalData(name, classID, D)
                #originalData_with_threshold(name, classID, D)
                #slowData(name, classID, D)
                #speedData(name, classID, D)
                #semitonesHigh(name, classID, D)
                #semitonesLow(name, classID, D)
                
                # global class for counting number of classes available.
                #--------------------------------------------------------------
                number_of_class += 1
            
            except:
                print('header detected so passing it.\n')
                pass
      
    k.clear_session()
          
    dataset = D
    random.shuffle(dataset)
    random.shuffle(dataset)
    random.shuffle(dataset)
    
    D_len = len(D)
    data_split = int((D_len*70)/100)
    
    train = dataset[: data_split]
    test = dataset[data_split :]
    
    X_train, y_train = zip(*train)
    X_test, y_test = zip(*test)
    
    # Reshape for CNN input.
    #--------------------------------------------------------------------------
    X_train = np.array([x.reshape( (128, 128, 1) ) for x in X_train])
    X_test = np.array([x.reshape( (128, 128, 1) ) for x in X_test])
    
    # One-Hot encoding for classes
    #--------------------------------------------------------------------------
    y_train = np.array(keras.utils.to_categorical(y_train, number_of_class))
    y_test = np.array(keras.utils.to_categorical(y_test, number_of_class))
    
    k.clear_session()
    
    model = Sequential()
    input_shape=(128, 128, 1)
    
    model.add(Conv2D(16, (3, 3), strides=(1, 1), input_shape=input_shape, padding='same'))
    model.add(Activation('relu'))
    
    model.add(Conv2D(32, (3, 3), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    
    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    
    model.add(Conv2D(128, (3, 3), strides=(1, 1), padding='same'))
    model.add(Activation('relu'))
    
    model.add(MaxPooling2D((2, 2)))
        
    model.add(Dropout(0.5))
    
    model.add(Flatten())
    
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    
    model.add(Dense(number_of_class))
    model.add(Activation('softmax'))
    
    model.compile(optimizer="Adam",	loss="categorical_crossentropy", metrics=['accuracy'])
    
    # defining the batch size and epochs.
    # num_b_size = len(test)*
    # num_epochs = int((len(D)-part)/num_b_size)
    
    set_epochs = 20
    set_batch = 32
    
    history = model.fit(X_train, y_train, epochs = set_epochs, batch_size= set_batch, validation_data= (X_test, y_test))
    
    score = model.evaluate( X_test, y_test)
    
    print('\n\nTest loss:', colored(score[0]*100, 'red'))
    print('Test accuracy:', colored(score[1]*100, 'green'))
    
    Totaldata =  D_len
    NoClass =    number_of_class
    BatchSize =  set_batch
    Epoches =    set_epochs
    TrainAcc =   round(history.history['acc'][-1]*100, 4)
    TestAcc =    round(history.history['val_acc'][-1]*100, 4)
    TrainLoss =  round(history.history['loss'][-1]*100, 4)
    TestLoss =   round(history.history['val_loss'][-1]*100, 4)
    DateTrain =  QDateTime.currentDateTime().toString()
    
    
    # inserting the details into the CSV.
    #--------------------------------------------------------------------------
    update_training_CSV(Totaldata, NoClass, BatchSize, Epoches, TrainAcc, TestAcc, TrainLoss, TestLoss, DateTrain)
            
    # saving thr trained model data.
    #--------------------------------------------------------------------------
    model.save('models/gunshot_prediction.h5')
    
    # this variable is going to be used to get back from the training progress bar window
    # to the training window.
    #------------------------------------------------------------------------------------
    global stop_training
    stop_training = 1
    
    #Confution Matrix
    #--------------------------------------------------------------------------
    y_pred = model.predict_classes(X_test)
    cm = confusion_matrix(np.argmax(y_test,axis=1), y_pred)
    print(cm)
    
    # plot train and validation loss
    #--------------------------------------------------------------------------
#    pyplot.plot(history.history['loss'])
#    pyplot.plot(history.history['val_loss'])
#    pyplot.title('model train vs validation loss')
#    pyplot.ylabel('loss')
#    pyplot.xlabel('epoch')
#    pyplot.legend(['train', 'validation'], loc='upper right')
#    pyplot.show()
    
    # plot train and validation accuracy
    #--------------------------------------------------------------------------
#    pyplot.plot(history.history['acc'])
#    pyplot.plot(history.history['val_acc'])
#    pyplot.title('model train vs validation accuracy')
#    pyplot.ylabel('loss')
#    pyplot.xlabel('epoch')
#    pyplot.legend(['train_acc', 'validation_acc'], loc='lower right')
#    pyplot.show()

# ----------------------------------------------------------------------------------------------------------------------------------------- #    
#####################################################  training with user parameters  #######################################################
# ----------------------------------------------------------------------------------------------------------------------------------------- #   

def user_do_training(user_ratio, user_dropout, user_epoches, user_batch_size):
        
    D = []
    number_of_class = 0
    
    # uploading the dummy data to the model.
    #--------------------------------------------------------------------------
    with open('audio/dummy_class.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        
        for row in reader:
            
            try:
                # selecting name and id
                #--------------------------------------------------------------
                name = row[1]
                classID = row[0]
                print (classID,'\t',colored(name,'red'))

                # generating the data for model.  
                #--------------------------------------------------------------
                originalData(name, classID, D)
                #slowData(name, classID, D)
                #speedData(name, classID, D)
                #semitonesHigh(name, classID, D)
                #semitonesLow(name, classID, D)
                
                # global class for counting number of classes available.
                #--------------------------------------------------------------
                number_of_class += 1
            
            except:
                print('header detected so passing it.\n')
                pass
        
    with open('audio/classes.csv', 'r') as f:
        reader = csv.reader(f)
        
        # skip the headers or the first row of the csv if 
        # we add it multiple times then it will remove multiple rows.
        #----------------------------------------------------------------------
        next(reader, None)    
        
        for row in reader:
            
            try:
                # selecting name and id
                #--------------------------------------------------------------
                name = row[1]
                classID = row[0]
                print (classID,'\t',colored(name,'cyan'))
                
                # generating the data for model.
                #--------------------------------------------------------------
                originalData(name, classID, D)
                #originalData_with_threshold(name, classID, D)
                #slowData(name, classID, D)
                #speedData(name, classID, D)
                #semitonesHigh(name, classID, D)
                #semitonesLow(name, classID, D)
                
                # global class for counting number of classes available.
                #--------------------------------------------------------------
                number_of_class += 1
            
            except:
                print('header detected so passing it.\n')
                pass
      
    k.clear_session()
          
    dataset = D
    random.shuffle(dataset)
    random.shuffle(dataset)
    random.shuffle(dataset)
    
    D_len = len(D)
    data_split = int(D_len * (user_ratio))
    
    train = dataset[: data_split]
    test = dataset[data_split :]
    
    X_train, y_train = zip(*train)
    X_test, y_test = zip(*test)
    
    # Reshape for CNN input.
    #--------------------------------------------------------------------------
    X_train = np.array([x.reshape( (128, 128, 1) ) for x in X_train])
    X_test = np.array([x.reshape( (128, 128, 1) ) for x in X_test])
    
    # One-Hot encoding for classes
    #--------------------------------------------------------------------------
    y_train = np.array(keras.utils.to_categorical(y_train, number_of_class))
    y_test = np.array(keras.utils.to_categorical(y_test, number_of_class))
    
    k.clear_session()
    
    model = Sequential()
    input_shape=(128, 128, 1)
    
    model.add(Conv2D(36, (5, 5), strides=(1, 1), input_shape=input_shape))
    model.add(MaxPooling2D((4, 2), strides=(4, 2)))
    model.add(Activation('relu'))
    
    model.add(Conv2D(48, (5, 5), padding="valid"))
    model.add(MaxPooling2D((4, 2), strides=(4, 2)))
    model.add(Activation('relu'))
    
    model.add(Conv2D(48, (5, 5), padding="valid"))
    model.add(Activation('relu'))
    
    model.add(Flatten())
    model.add(Dropout(rate = user_dropout))
    
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(rate = user_dropout))
    
    model.add(Dense(number_of_class))
    model.add(Activation('softmax'))
    
    model.compile(optimizer="Adam",	loss="categorical_crossentropy", metrics=['accuracy'])
    
    # defining the batch size and epochs.
    # num_b_size = len(test)*
    # num_epochs = int((len(D)-part)/num_b_size)
    
    set_epochs = user_epoches
    set_batch = user_batch_size
    
    history = model.fit(X_train, y_train, epochs = set_epochs, batch_size= set_batch, validation_data= (X_test, y_test))
    
    score = model.evaluate( X_test, y_test)
    
    print('\n\nTest loss:', colored(score[0]*100, 'red'))
    print('Test accuracy:', colored(score[1]*100, 'green'))
    
    Totaldata =  D_len
    NoClass =    number_of_class
    BatchSize =  set_batch
    Epoches =    set_epochs
    TrainAcc =   round(history.history['acc'][-1]*100, 4)
    TestAcc =    round(history.history['val_acc'][-1]*100, 4)
    TrainLoss =  round(history.history['loss'][-1]*100, 4)
    TestLoss =   round(history.history['val_loss'][-1]*100, 4)
    DateTrain =  QDateTime.currentDateTime().toString()
    
    
    # inserting the details into the CSV.
    #--------------------------------------------------------------------------
    update_training_CSV(Totaldata, NoClass, BatchSize, Epoches, TrainAcc, TestAcc, TrainLoss, TestLoss, DateTrain)
            
    # saving thr trained model data.
    #--------------------------------------------------------------------------
    model.save('models/gunshot_prediction.h5')
    
    # this variable is going to be used to get back from the training progress bar window
    # to the training window.
    #------------------------------------------------------------------------------------
    global stop_training
    stop_training = 1
    
    #Confution Matrix
    #--------------------------------------------------------------------------
    y_pred = model.predict_classes(X_test)
    cm = confusion_matrix(np.argmax(y_test,axis=1), y_pred)
    print(cm)
    
    # plot train and validation loss
    #--------------------------------------------------------------------------
#    pyplot.plot(history.history['loss'])
#    pyplot.plot(history.history['val_loss'])
#    pyplot.title('model train vs validation loss')
#    pyplot.ylabel('loss')
#    pyplot.xlabel('epoch')
#    pyplot.legend(['train', 'validation'], loc='upper right')
#    pyplot.show()
    
    # plot train and validation accuracy
    #--------------------------------------------------------------------------
#    pyplot.plot(history.history['acc'])
#    pyplot.plot(history.history['val_acc'])
#    pyplot.title('model train vs validation accuracy')
#    pyplot.ylabel('loss')
#    pyplot.xlabel('epoch')
#    pyplot.legend(['train_acc', 'validation_acc'], loc='lower right')
#    pyplot.show()    
    