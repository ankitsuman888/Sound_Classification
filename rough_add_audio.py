


from pydub import AudioSegment
for i in range(1,540):
    sound1 = AudioSegment.from_file('D:/Python/DATASET/Recog_sound/SIREN/siren_'+str(i)+".wav")
    sound2 = AudioSegment.from_file('D:\\Python\\DATASET\\Recog_sound\\SIREN\\siren_'+str(i + 1)+".wav")
    
    combined = sound1.overlay(sound2)

combined.export("siren.wav", format='wav')

import statistics 
x = [172, 174, 176, 172, 172, 173, 176, 172, 177, 174, 176, 175, 176, 169, 175, 174, 174, 174, 175, 173, 171, 171, 175, 175, 173, 175, 175]

xx = statistics.mean(x) 
print("Mean is :", xx)

xx= statistics.median(x)
print("Median is :", xx)


xx= statistics.mode(x)
print("Mode is :", xx)

y = (172+ 174+ 176+ 172+ 172+ 173+ 176+ 172+ 177+ 174+ 176+ 175+ 176+ 169+ 175+ 174+ 174+ 174+ 175+ 173+ 171+ 171+ 175+ 175+ 173+ 175+ 175)/27
print(y)

z = [184, 180, 181, 184, 182, 181, 182, 182, 183, 182, 181, 182, 182, 180, 183, 181, 184, 183, 182, 182, 183, 182, 183, 181, 180, 181, 183]
zz = statistics.stdev(z)

print(zz)