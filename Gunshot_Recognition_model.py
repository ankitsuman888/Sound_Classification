from keras.models import load_model
import tensorflow as tf
import numpy as np
import librosa
import librosa.display
from keras import backend as K
from termcolor import colored
#import joblib
import csv

freq_val = 0

def frequency_value():   
    return(freq_val)

def do_recognition(data, freq_thres) :

    global freq_val
    K.clear_session()
       
    #data ='D:\\Python\\PROJECT\\NCTC_Project\\GunshotRecognition\\audio\\cracker\\cracker\\original_7.wav'
    
    y, sr = librosa.load(data, duration = 2.97)
    
    size_mel = librosa.feature.melspectrogram(y = y, sr = sr)
    
    size_mel = np.array([size_mel.reshape( (128, 128, 1) )])
    
    '''
    # generating tempo of the file.
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    print(tempo ,':', beats)
    '''      
    # generating the average frequency of the audio file 'data'
    # and finding the summation of all the value. We are taking avg_freq[0]
    # because all the elements are in avg_freq[0][elements].
    '''
    avg_freq = librosa.feature.spectral_centroid(y=y, sr=sr)
    summation = int(sum(avg_freq[0])/ len(avg_freq[0])) 
    print('average frequency: ',summation)
    
    avg_freq = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    summation = int(sum(avg_freq[0])/ len(avg_freq[0])) 
    print('average frequency: ',summation)
    '''
    # spectral_rolloff essentially the maximum: finds the frequency f such that almost all 
    # of the energy (by default, 85%) in the frame is at frequencies below f. If you set 
    # the roll-off to a small fraction (say, 10%), this would give you an estimate of the 
    # effective minimum frequency.
    
    '''
    # Approximate maximum frequencies with roll_percent=0.85 (default)
    
    avg_freq = librosa.feature.spectral_rolloff(y=y, sr=sr)
    freq_val = int(sum(avg_freq[0])/ len(avg_freq[0]))
    
    
    '''
    # Approximate minimum frequencies with roll_percent=0.1
    
    avg_freq = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.1)
    freq_val = int(sum(avg_freq[0])/ len(avg_freq[0])) 
    print(freq_thres)

    # setting up the threshold value.    
    freq_thres = int(freq_thres)
    
    if(freq_val < freq_thres):
        x = np.array([['Nothing Found', 0],
                      ['Nothing Found', 0],
                      ['Nothing Found', 0],
                      ['Nothing Found', 0],
                      ['Nothing Found', 0],
                      ['Nothing Found', 0]])
    
    else:
#        joblib_model = joblib.load('models/gunshot_prediction.pkl')
#        get_data = joblib_model.predict(size_mel)
        
        model = load_model('models/gunshot_prediction.h5')
        get_data = model.predict(size_mel)
        
        # here taking all the classes from the classes.csv and adding their Id along with 
        # their probability.
        # value[][0] = class label
        # value[][1] = class name
        # value[][2] = probability
        
        i = 0 
        class_list = []
        
        with open('audio/classes.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            
            for row in reader:
                class_list = class_list + [[int(row[0]), row[1], round(get_data[0][i]*100, 2)]]
                i = i+1
                
        # print(class_list)
        
        # sorting element using the third element i.e, is x[2].             
        class_list.sort(reverse = True, key=lambda x: x[2])
        # print (class_list)
        
        
        # Now class_list[0] will have the element with the highest probability
        # Here returning the outputr as number of classes wise.
        # If the number of class is one then first will be executed and so on.
        # Here we are returning the maximum class as 5.
        
        # If there is only 1 class
        if(len(class_list) == 1):
            x = np.array([[class_list[0][1], class_list[0][2]],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty']])
        
        # If there is only 2 class       
        if(len(class_list) == 2):
            x = np.array([[class_list[0][1], class_list[0][2]],
                          [class_list[1][1], class_list[1][2]],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty']])
        
        # If there is only 3 class            
        if(len(class_list) == 3):
            x = np.array([[class_list[0][1], class_list[0][2]],
                          [class_list[1][1], class_list[1][2]],
                          [class_list[2][1], class_list[2][2]],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty']])
        
        # If there is only 4 class            
        if(len(class_list) == 4):
            x = np.array([[class_list[0][1], class_list[0][2]],
                          [class_list[1][1], class_list[1][2]],
                          [class_list[2][1], class_list[2][2]],
                          [class_list[3][1], class_list[3][2]],
                          ['Empty', 'Empty'],
                          ['Empty', 'Empty']])
        
        # If there is only 5 class      
        if(len(class_list) == 5):
            x = np.array([[class_list[0][1], class_list[0][2]],
                          [class_list[1][1], class_list[1][2]],
                          [class_list[2][1], class_list[2][2]],
                          [class_list[3][1], class_list[3][2]],
                          [class_list[4][1], class_list[4][2]],
                          ['Empty', 'Empty']])
    
        # If there is only 6 class      
        if(len(class_list) == 6):
            x = np.array([[class_list[0][1], class_list[0][2]],
                          [class_list[1][1], class_list[1][2]],
                          [class_list[2][1], class_list[2][2]],
                          [class_list[3][1], class_list[3][2]],
                          [class_list[4][1], class_list[4][2]],
                          [class_list[5][1], class_list[5][2]]])
            
    return(x)
    