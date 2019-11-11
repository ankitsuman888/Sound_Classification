import csv
import os
import shutil

# ------------------------------------------------------------------------------------------------------------------------------------------#    
###################################################  cleaning class name data   #############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

def clean_classData():
    
    try :
                
        # Clean the class sound file.
        #----------------------------------------------------------------------
        with open('audio/classes.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader, None) 
            
            for row in reader:
                
                try:
                    # reading each folder name from the csv file and deleting the folder according to it.
                    #-------------------------------------------------------------------------------------
                    className = row[1]   
                    folderName = className
                    shutil.rmtree('audio/'+ folderName +'/'+ folderName)
                    shutil.rmtree('audio/'+ folderName)

                except:
                    pass
        
        # Replace the CSV file with new empty one. 
        #----------------------------------------------------------------------
        with open('audio/classes.csv', 'w') as IdData:
            IdData.write('{},{}'.format('class_id','class_name'))
            
    except:
        pass

# ------------------------------------------------------------------------------------------------------------------------------------------#    
###################################################  cleaning the record data   #############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

def clean_evidence():
    
    try:
        # Repalce the CSV file with new empty one.
        #----------------------------------------------------------------------
        with open('Data_Record/sound_evidence.csv', 'w') as IdData:
            IdData.write('{},{},{},{},{}'.format('Id','Class','Probability','Time','Date'))
            
        # Clean the evidence sound data of the model by deleting the evidence folder & recreating it.
        #--------------------------------------------------------------------------------------------
        folderName = 'sound_data_saved'   
        shutil.rmtree('audio_record/'+ folderName)
        os.makedirs('audio_record/'+ folderName)
     
    except:
        pass

# ------------------------------------------------------------------------------------------------------------------------------------------#    
#####################################################  cleaning notification data  ##########################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    

def clean_notification_data():
    
    try:
        from Gunshot_Detection_DATA_SAVING import update_notification_CSV
        
        val = os.path.isfile('Data_Record/notification_data.csv')
        print(val)
        
        # if the CSV is not available then creating the new one.
        #----------------------------------------------------------------------
        if (val == False):
            with open('Data_Record/notification_data.csv', 'w') as IdData:
                IdData.write('{},{},{}'.format('Class', 'Email', 'Phone'))
                
            update_notification_CSV('NULL', 'NULL', 'NULL')
        
        # If CSV is there then writing data directly into the csv.
        #----------------------------------------------------------------------
        elif(val == True):
            update_notification_CSV('NULL', 'NULL', 'NULL')
            
    except:
        pass

# ------------------------------------------------------------------------------------------------------------------------------------------#    
#########################################################  cleaning everthing   #############################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    
    
def clean_model():
    # cleaning the class data and the evidence both from the model.
    # resetting the whole model.
    try:
        clean_classData()
        clean_evidence()
        clean_notification_data()
        
    except:
        pass
    
