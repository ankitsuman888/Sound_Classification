import numpy as np
import librosa
import time

# data formating for input
data ='D:\\Python\\PROJECT\\NCTC_Project\\GunshotRecognition\\audio_record\\output.wav'
y, sr = librosa.load(data, duration = 2.97)
size_mel = librosa.feature.melspectrogram(y = y, sr = sr)
size_mel = np.array([size_mel.reshape( (128, 128, 1) )])
print(size_mel)


#model = 'model that we have buit in CNN'



start_time = time.time()
# Using Joblib
import joblib

# joblib_file = "joblib_model.pkl"  
# joblib.dump(model, joblib_file)

joblib_file = "joblib_model.pkl"  
joblib_model = joblib.load(joblib_file)
predict = joblib_model.predict(size_mel)
print(predict)  
print("--- %s seconds ---" % (time.time() - start_time))





start_time = time.time()
# Using Pickle
import pickle

# pkl_filename = "pickle_model.pkl"  
# with open(pkl_filename, 'wb') as file:  
    # pickle.dump(model, file)

pkl_filename = "pickle_model.pkl" 
with open(pkl_filename, 'rb') as file:  
    pickle_model = pickle.load(file)
predict = pickle_model.predict(size_mel)
print(predict) 
print("--- %s seconds ---" % (time.time() - start_time))





start_time = time.time()
#using h5py
from keras.models import load_model

# model.save('models/gunshot_prediction.h5')

model = load_model('gunshot_prediction.h5')
get_data = model.predict(size_mel)
print(get_data)
print("--- %s seconds ---" % (time.time() - start_time))