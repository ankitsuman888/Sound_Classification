import csv
#import soundfile as sf
#import librosa
import wave
import contextlib 

def calculateTrainingTime():
    
    # finding the length of the dummydata file {i.e, silence.wav}
    #--------------------------------------------------------------------------
    
#    y, sr = librosa.load('audio/silence/silence.wav') 
#    dummy_class_length = librosa.get_duration(y)
#    total_dummy_samples = int(dummy_class_length/2.97)  
#    print('Dummy Sample: ', total_dummy_samples)
    
    fname = 'audio/silence/silence.wav'
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        total_dummy_samples = int(duration/2.97)
        print(total_dummy_samples)
 
    
    # finding the length of the all the classes that we have uploaded.
    #--------------------------------------------------------------------------
    
    total_user_class_samples = 0
        
    with open('audio/classes.csv', 'r') as file:  
        reader = csv.reader(file)
        next(reader, None)
        
        for row in reader:
            
#            f = sf.SoundFile('audio/'+row[1]+'/'+row[1]+'.wav')
#            user_class_length = int(len(f) / f.samplerate)
#            user_class_samples = int(user_class_length/2.97)
            
#            y, sr = librosa.load('audio/'+row[1]+'/'+row[1]+'.wav')
#            user_class_length = librosa.get_duration(y)
#            user_class_samples = int(user_class_length/2.97)
            
            fname = 'audio/'+row[1]+'/'+row[1]+'.wav'
            with contextlib.closing(wave.open(fname,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                user_class_samples = int(duration/2.97)
                print(user_class_samples)
            
            total_user_class_samples += user_class_samples
            
    print('User Class Sample: ',total_user_class_samples)
    
    # finding training epoches time.
    # currently not defined.
    #--------------------------------------------------------------------------
    epoches_train_time = 0
    
    # fining total sample and adding them then finding total time in minutes.
    #--------------------------------------------------------------------------
    
    total_sample_size = total_dummy_samples + total_user_class_samples + epoches_train_time
    
    timeLength = int((total_sample_size / 60) / 3)  ## in minutes.   ( 3 sample per second split)  
    
    print(total_sample_size)
    print(timeLength)

    return(timeLength)



     