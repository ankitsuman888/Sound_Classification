import csv

# ------------------------------------------------------------------------------------------------------------------------------------------#    
##########################################  here writing data into CLASSES csv file   #######################################################
# ------------------------------------------------------------------------------------------------------------------------------------------#    


# For adding the new classes into the CSV file.
def updateTrainClassCSV(class_id, class_name):
    with open('audio/classes.csv', 'a') as IdData:
        IdData.write('\n{},{}'.format(class_id, class_name))
        
        
def updateTrainClass(class_name):
        
    with open('audio/classes.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            row
        Id = row[0]
    
    if(Id == 'class_id'):
        Id = 1
    else:
        Id = int(Id) + 1
        
    updateTrainClassCSV(Id, class_name)

# Show total available classes.
    