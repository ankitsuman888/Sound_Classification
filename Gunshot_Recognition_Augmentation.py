import librosa
import librosa.display
import numpy as np
from termcolor import colored
import os
from pydub import AudioSegment

import warnings
warnings.filterwarnings('ignore')

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  original data split   #############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      

def originalData(name, classID, D):
       
    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+ name +'/'+ name +'.wav')
            audio = audio[t1:t2]           
            audio.export('audio/'+ name +'/'+ name +'/original_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/original_{}.wav'. format(i))
            
            # Melspectrogram feature extracion. 
            #------------------------------------------------------------------
            print( i , 'of size', audio_size, 'added to folder '+ colored(name,'red'))                  
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/original_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)     
            if ps.shape != (128, 128): 
                break
            D.append((ps, classID))
                        
            i = i + 1
            j = j + 2.97
            k = k + 2.97
       
        except:
            print('data corrupted')

def originalData_with_threshold(name, classID, D):
    
    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+ name +'/'+ name +'.wav')
            audio = audio[t1:t2]           
            audio.export('audio/'+ name +'/'+ name +'/original_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/original_{}.wav'. format(i))
            
            # Melspectrogram feature extracion. 
            #------------------------------------------------------------------
            print( i , 'of size', audio_size, 'added to folder '+ colored(name,'green'))                  
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/original_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)     
            
  
            # librosa.effects.trim
            # if the sample length is less than 1.5 second after the trimming 
            # then we are rejecting the sample.
            #------------------------------------------------------------------            
            yt, index = librosa.effects.trim(y, top_db = 5)
            print(librosa.get_duration(yt))
            if(librosa.get_duration(yt) >= 0.5):
                if ps.shape != (128, 128): 
                    break
                D.append((ps, classID))
                print(colored("Sample Passed.",'green'))
            else:
                print(colored("Smaple Rejected.",'red'))
                pass
            
#            avg_freq = librosa.feature.spectral_rolloff(y = y, sr = sr, roll_percent = 0.1)
#            freq_val = int(sum(avg_freq[0]) / len(avg_freq[0]))          
#            if(freq_val >= 300):
#                if ps.shape != (128, 128): 
#                    break
#                D.append((ps, classID))          
#            else:
#                pass
#            print("The average frequency of sample : ",freq_val)
                                      
            i = i + 1
            j = j + 2.97
            k = k + 2.97
       
        except:
            print('data corrupted')

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  HPSS ------     ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      


def hpssData(name, classID, D):
    
    y, sr = librosa.load('audio/'+ name +'/'+ name +'.wav' )
    # margin lies between 1.0 to 10.0
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    librosa.output.write_wav('audio/'+ name +'/harmonic.wav', y_harmonic, sr)
    librosa.output.write_wav('audio/'+ name +'/percusive.wav', y_percussive, sr)

    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+name+'/hpss.wav')
            audio = audio[t1:t2]           
            audio.export('audio/'+ name +'/'+ name +'/hpss_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/hpss_{}.wav'. format(i))
                
            print( i , 'of size', audio_size, 'added to folder '+ name)
            
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/hpss_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)      
            if ps.shape != (128, 128): 
                break
            D.append((ps, classID)) 
            
            i = i + 1
            j = j + 2.97
            k = k + 2.97
        
        except:
            print('data corrupted')
    
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  SLOW  ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      


def slowData(name, classID, D):
    
    # sr=None means that we are taking default sample rate of the audio.
    # if you want to change the sample rate put sr=48000 or something else.

    y, sr = librosa.load('audio/'+ name +'/'+ name +'.wav')
    y_changed_slow = librosa.effects.time_stretch(y, rate = 0.96)
    librosa.output.write_wav('audio/'+ name +'/slow.wav', y_changed_slow, sr)
    
    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+name+'/slow.wav')
            audio = audio[t1:t2]           
            audio.export('audio/'+ name +'/'+ name +'/slow_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/slow_{}.wav'. format(i))
                
            print( i , 'of size', audio_size, 'added to folder '+ name)
            
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/slow_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)      
            if ps.shape != (128, 128): 
                break
            D.append((ps, classID)) 
            
            i = i + 1
            j = j + 2.97
            k = k + 2.97
        
        except:
            print('data corrupted')
    
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  FAST   ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      

def speedData(name, classID, D):
         
    y, sr = librosa.load('audio/'+ name +'/'+ name +'.wav' )
    y_changed_speed = librosa.effects.time_stretch(y, rate = 1.15)
    librosa.output.write_wav('audio/'+ name +'/speed.wav', y_changed_speed, sr)
    
    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+name+'/speed.wav')
            audio = audio[t1:t2]
            
            audio.export('audio/'+ name +'/'+ name +'/speed_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/speed_{}.wav'. format(i))
                
            print( i , 'of size', audio_size, 'added to folder '+ name)
            
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/speed_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)       
            if ps.shape != (128, 128): 
                break
            D.append((ps, classID)) 
            
            i = i + 1
            j = j + 2.97
            k = k + 2.97
            
        except:
            print('data corrupted')
            
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  HIGH TONE  ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      

def semitonesHigh(name, classID, D):
         
    y, sr = librosa.load('audio/'+ name +'/'+ name +'.wav')
    y_changed_st = librosa.effects.pitch_shift(y, sr, n_steps = 0.1)
    librosa.output.write_wav('audio/'+ name +'/pitch_a.wav', y_changed_st, sr)
        
    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+name+'/pitch_a.wav')
            audio = audio[t1:t2]
            
            audio.export('audio/'+ name +'/'+ name +'/pitch_a_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/pitch_a_{}.wav'. format(i))
                
            print( i , 'of size', audio_size, 'added to folder '+ name)
            
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/pitch_a_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)       
            if ps.shape != (128, 128): 
                break
            D.append((ps, classID)) 
            
            i = i + 1
            j = j + 2.97
            k = k + 2.97
            
        except:
            print('data corrupted')

# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  LOW TONE  ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      
            
def semitonesLow(name, classID, D):
         
    y, sr = librosa.load('audio/'+ name +'/'+ name +'.wav' )   
    y_changed_st = librosa.effects.pitch_shift(y, sr, n_steps = -0.1)
    librosa.output.write_wav('audio/'+ name +'/pitch_b.wav', y_changed_st, sr)
    
    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+name+'/pitch_b.wav')
            audio = audio[t1:t2]
            
            audio.export('audio/'+ name +'/'+ name +'/pitch_b_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/pitch_b_{}.wav'. format(i))
                
            print( i , 'of size', audio_size, 'added to folder '+ name)
            
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/pitch_b_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)       
            if ps.shape != (128, 128): 
                break
            D.append((ps, classID)) 
            
            i = i + 1
            j = j + 2.97
            k = k + 2.97
            
        except:
            print('data corrupted')
  
# ------------------------------------------------------------------------------------------------------------------------------------------#    
########################################################  NOISE   ###################################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#      
         
def noiseData(name, classID, D):
         
    y, sr = librosa.load('audio/'+ name +'/'+ name +'.wav')      
    y_noise = y.copy()
    noise_amp = 0.005*np.random.uniform()*np.amax(y_noise)
    y_noise = y_noise.astype('float64') + noise_amp * np.random.normal(size = y_noise.shape[0])

    librosa.output.write_wav('audio/'+ name +'/noise.wav', y_noise, sr)

    
    i = 1
    j = 0
    k = 2.97
    
    audio_size = 0
    
    while (audio_size != 44):
        
        try:
            t1 = j * 1000   # thousand for millisecond.
            t2 = k * 1000
            
            audio = AudioSegment.from_wav('audio/'+name+'/noise.wav')
            audio = audio[t1:t2]
            
            audio.export('audio/'+ name +'/'+ name +'/noise_{}.wav'. format(i), format='wav')    
            audio_size = os.path.getsize('audio/'+ name +'/'+ name +'/noise_{}.wav'. format(i))
                
            print( i , 'of size', audio_size, 'added to folder '+ name)
            
            y, sr = librosa.load('audio/'+ name +'/'+ name +'/noise_{}.wav'. format(i) , duration = 2.97)
            ps = librosa.feature.melspectrogram(y = y, sr = sr)       
            if ps.shape != (128, 128): 
                break
            D.append((ps, classID)) 
            
            i = i + 1
            j = j + 2.97
            k = k + 2.97
            
        except:
            print('data corrupted')         
            
            