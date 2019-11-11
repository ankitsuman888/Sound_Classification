# -*- coding: utf-8 -*-

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


y, sr = librosa.load('D:/Python/PROJECT/NCTC_Project/GunshotRecognition/audio_record/output4.wav', duration= 2.97)


# librosa.feature.melspectrogram
ps = librosa.feature.melspectrogram(y=y, sr=sr)
print(ps.shape)
librosa.display.specshow(ps, y_axis='mel', x_axis='time')


# librosa.feature.mfcc
ps1 = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=128)
print(ps1.shape)
librosa.display.specshow(ps1, y_axis='mel', x_axis='time')


# librosa.feature.chroma_stft
ps2 = librosa.feature.chroma_stft(y=y, sr=sr)
print(ps2.shape)
librosa.display.specshow(ps2, y_axis='mel', x_axis='time')


# librosa.feature.spectral_contrast
ps3 = librosa.feature.spectral_contrast(y=y, sr=sr)
print(ps3.shape)
librosa.display.specshow(ps3, y_axis='mel', x_axis='time')


# librosa.feature.tonnetz
ps4 = librosa.feature.tonnetz(y=y, sr=sr)
print(ps4.shape)
librosa.display.specshow(ps4, y_axis='mel', x_axis='time')

