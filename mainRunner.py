from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from GazeTracking.gaze_tracking import GazeTracking
import xlsxwriter     
import time  
import graph as graph
import circumplex as circumplex    
import math 
import Attention as attention


def empty_excel_file(file_path):
    try:
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()
        workbook.close()
        
        print("Excel file emptied successfully.")
    except Exception as e:
        print(f"Error: {e}")

webcam = cv2.VideoCapture(0) #open the camera
print("opened camera")

gaze = GazeTracking() #gaze tracking object
print("gaze tracking object created")
cascade_classifier=cv2.CascadeClassifier(r'/Users/rohansaikondle/Downloads/Main-project/EmotionRecognitionmodels/frontalface.xml') #model to search for face in an image
model=load_model(r'/Users/rohansaikondle/Downloads/Main-project/EmotionRecognitionmodels/face.hdf5') #emotion detection modelprint("emotion detection model loaded")
class_labels=['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise'] #classes of the emotions
file_path = "/Users/rohansaikondle/Downloads/Main-project/Data/sheets/data.xlsx"  # Provide the path to your Excel file
empty_excel_file(file_path)
#create an excel sheet to write write data
book = xlsxwriter.Workbook(file_path)  
sheet = book.add_worksheet('data')
print("excel sheet open now")
row = 0    
column = 0   

#Time information variables
# TT = 40 #runs for TT frames , 1 minute = 120 frames
# sleep_time = 0.49 #sleeps for 0.499 ~ 0.5 secs, so runs at 2fps

TT = 2 #runs for TT frames , 1 minute = 120 frames
sleep_time = 29.98 #sleeps for 0.499 ~ 0.5 secs, so runs at 2fps
t=0

i=0
while (TT > 0):
    _, frame = webcam.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # gray scale the image
    faces = cascade_classifier.detectMultiScale(gray,1.3,5) #detect the faces

    #for each face detected in the image
    for (x,y,w,h) in faces:

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),2) #put a rectagle on the face
        roi_gray = gray[y:y+h,x:x+w] #cut out the face in gray
        roi_gray = cv2.resize(roi_gray,(48,48),fx=100,fy=100,interpolation=cv2.INTER_CUBIC) #resize the face
        crop = frame[y:y+h,x:x+w] #save the face in color formate
        
        if np.sum([roi_gray])!=0: #is face is present, and the image is not all dark
            
            #EMotion Detection part
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            preds = model.predict(roi)[0]#do the prediction
            prob,angle_1, sector_n0_1, per_1 = circumplex.circumplex(preds)
            label=class_labels[preds.argmax()] #get the label
            label_position = (x,y)  #make a tuple of the coordinates where the face begins
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),3) #print stuff on the frame

            #Gaze Tracking part
            gaze.refresh(frame) #give the source image to the gaze tracking object
            frame = gaze.annotated_frame() #set the markings on the pupils
            hr=gaze.horizontal_ratio()
            vr=gaze.vertical_ratio()
            val,angle_2, sector_n0_2, per_2 = attention.attention_percentage(hr, vr)
            label_position = (x-2,y-50)
            l = [prob, sector_n0_1, per_1, val, sector_n0_2, per_2]
            for p in l:
                if isinstance(p, list):
                    for j in p:
                        sheet.write(row, column, j)
                        column += 1
                elif isinstance(p, np.ndarray):
                    for j in p:
                        sheet.write(row, column, j)
                        column += 1
                else:
                    sheet.write(row, column, p)
                    column += 1
            row += 1
            column = 0
            cv2.imshow("Demo", frame)
            cv2.imwrite(r'/Users/rohansaikondle/Downloads/Main-project/Data/Images/kang'+str(i)+'.jpg',crop)
            sheet.insert_image(row-1,11,r'/Users/rohansaikondle/Downloads/Main-project/Data/Images/kang'+str(i)+'.jpg')
            if angle_1 ==None or angle_2== None:
                continue 
            else:
                q = graph.plot_circle_with_sectors(angle_1, angle_2,per_1, per_2, row-1 ) 
                sheet.insert_image(row-1,16, r'/Users/rohansaikondle/Downloads/Main-project/circle_with_sectors'+str(row-1)+'.png')          
            i+=1
    if cv2.waitKey(1) == 27:
        break
    time.sleep(sleep_time) #sleeps till the amount of time specified in 'sleep_time' variable
    TT = TT -1 #reduce the number of frames captured
book.close()