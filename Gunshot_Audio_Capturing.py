import math
import wave
import pyaudio
import audioop
import os
import shutil

stop = 0

def Recording():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16    #sample size
    CHANNEL = 2                 #1= mono, 2= stereo(1411 kbps i.e bitrate)
    RATE = 441000               #sample rate 
    DURATION = 2.97
    OUTPUT = 'audio_record/output.wav'
    #THRESHOLD = 900
    #num_samples=50
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format = FORMAT,
                    channels = CHANNEL,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    
    print('Recording', end =" ")
    
    frames = []
    
    for i in range(0, int (RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    '''
    # setting up the threshold for the recording so that silence will not...... 
    # get predicted anyway.
    
    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
              for x in range(num_samples)] 
    
    values = sorted(values, reverse=True)
    
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print(" | Avg Intensity: ", r)
    #..........................................................................
    '''
    print('Completed')
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(OUTPUT, 'wb')
    wf.setnchannels(CHANNEL)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()



def dummyRecording(timeLength):
    
    # removing and creating new directory for recording for
    # handling abiguity of already existence.
    
    # converting into int.
    timeLength = int(timeLength)
    
    className = 'silence'

    if(os.path.isdir('audio/'+ className) == True):
      
        try:
            # remove folder an its contents
            shutil.rmtree('audio/'+ className +'/'+ className)
            shutil.rmtree('audio/'+ className)
            
            os.makedirs('audio/'+ className)
            os.makedirs('audio/'+ className +'/'+ className)
        
        except:
            os.makedirs('audio/'+ className)
            os.makedirs('audio/'+ className +'/'+ className)
            
    else:
        os.makedirs('audio/'+ className)
        os.makedirs('audio/'+ className +'/'+ className)
    
    # Recording part.
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16    #sample size
    CHANNEL = 2                 #1= mono, 2= stereo(1411 kbps i.e bitrate)
    RATE = 44100                #sample rate 
    DURATION = timeLength*60
    OUTPUT = 'audio/'+ className +'/'+ className +'.wav'
    
    print('started')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format = FORMAT,
                    channels = CHANNEL,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    
    frames = []
    
    for i in range(0, int (RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

        print('sound chunks: ',i )

    print('Completed')
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(OUTPUT, 'wb')
    wf.setnchannels(CHANNEL)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    
    
    
def liveRecording(className):
    
    # removing and creating new directory for recording for
    # handling abiguity of already existence.
    
    if(os.path.isdir('audio/'+ className) == True):
      
        # remove folder an its contents
        shutil.rmtree('audio/'+ className +'/'+ className)
        shutil.rmtree('audio/'+ className)
        
        os.makedirs('audio/'+ className)
        os.makedirs('audio/'+ className +'/'+ className)
    
    else:
        os.makedirs('audio/'+ className)
        os.makedirs('audio/'+ className +'/'+ className)
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16    # sample size
    CHANNEL = 2                 # 1= mono, 2= stereo(1411 kbps i.e bitrate)
    RATE = 44100                # sample rate 
    DURATION = 360000           # 100 hour recording 
    OUTPUT = 'audio/'+ className +'/'+ className +'.wav'
    
    print('started')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format = FORMAT,
                    channels = CHANNEL,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    
    frames = []
    
    for i in range(0, int (RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)
        
        # stopping when stop button is clicked.
        #----------------------------------------------------------------------
        global stop
        print('sound chunks: ',i ,stop)
                
        if(stop == 1):
            break
        
        if(stop == 1):
            break
        
    print('Completed')
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(OUTPUT, 'wb')
    wf.setnchannels(CHANNEL)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()