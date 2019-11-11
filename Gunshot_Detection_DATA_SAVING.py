# -*- coding: utf-8 -*-
import csv
import datetime
import os
from pydub import AudioSegment

# ------------------------------------------------------------------------------------------------------------------------------------------#    
#####################################################  This is for Saving Evidence   ########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

# Function for writing into the csv file.
def update_sound_CSV(Id, Class, Probability, Time, Date):
    with open('Data_Record/sound_evidence.csv', 'a') as IdData:
        IdData.write('\n{},{},{},{},{}'.format(Id, Class, Probability, Time, Date))


# Main function for saving the data file with the respective ID.
def saving_data_file(maxpos, prob):

    # Generating the Date and Time.
    now = datetime.datetime.now()
    Ctime = now.strftime("%I:%M:%S  %p")
    Cdate = str(datetime.datetime.now().date())    
        
    # Generating Id.
    with open('Data_Record/sound_evidence.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row
        Id = row[0]
    
    if(Id == 'Id'):
        Id = 1
    else:
        Id = int(Id)
        Id = Id + 1
    
    # combining id with the class.
    maxpos = str(Id)+'_'+maxpos
     
    # adding the information into the csv file by calling the function.
    update_sound_CSV(Id, maxpos, prob, Ctime, Cdate)
    
    # if the folder is not available then it will create the folder.
    newpath = r'audio_record\sound_data_saved' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
    # Saving the wave file in the name of maxpos under the location newpath.
    audio = AudioSegment.from_wav('audio_record/output.wav')
    audio.export('audio_record/sound_data_saved/'+ maxpos +'.wav', format='wav')   
    
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#####################################################  Saving Data for Notification   #######################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

# Function for writing into the csv file.
#------------------------------------------------------------------------------
def update_notification_CSV(Class, Email, Phone):
    with open('Data_Record/notification_data.csv', 'a') as IdData:
        IdData.write('\n{},{},{}'.format(Class, Email, Phone))


# writing new data into CSV for notification.
#------------------------------------------------------------------------------
def saving_data_notification(Class, Email, Phone):
    
    try :
        val = os.path.isfile('Data_Record/notification_data.csv')
        print(val)
        
        # if the CSV is not available then creating the new one.
        #----------------------------------------------------------------------
        if (val == False):
            with open('Data_Record/notification_data.csv', 'w') as IdData:
                IdData.write('{},{},{}'.format('Class', 'Email', 'Phone'))
                
            update_notification_CSV(Class, Email, Phone)
        
        # If CSV is there then writing data directly into the csv.
        #----------------------------------------------------------------------
        elif(val == True):
            update_notification_CSV(Class, Email, Phone)
    
    except:
        pass


# Here finding and selecting the class, email_Id and Phone_number from CSV for sending the notification since.
# Here we are taking the lastest/ last class name from the CSV as user input is latest.
#--------------------------------------------------------------------------------------------------------------
def DisplayDataNotification():
    
    try :
        val = os.path.isfile('Data_Record/notification_data.csv')
        print(val)
    
        if (val == False):
            dataList = ['NULL', 'NULL', 'NULL']
            return (dataList)
        
        elif(val == True):
            with open('Data_Record/notification_data.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    dataList = row
                
                print(dataList)       
                return(dataList)
    except:
        print('Except Condition Executed.')
        dataList = ['NULL', 'NULL', 'NULL']
        return (dataList)
           
  
# ------------------------------------------------------------------------------------------------------------------------------------------#    
#####################################################  ????????????????????????????   #######################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
