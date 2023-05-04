import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
from firebase_admin import storage
import time

# connect with the database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://face-attendance-real-tim-a6b68-default-rtdb.firebaseio.com/",
    'storageBucket':"face-attendance-real-tim-a6b68.appspot.com"
    
    
})
# connect with the database

bucket=storage.bucket




cap=cv2.VideoCapture(0) # read from camera 
cap.set(3,480)# width dimintions
cap.set(4,640) # hight dimintions


background_image=cv2.imread("Resources/back_image.png") # read background image

folder_of_pathe_modes="Resources/modes" # to read all modes from the folder

list_of_modes=os.listdir(folder_of_pathe_modes) # to read all names of photos

modes_list=[] # empty list

for mode in list_of_modes: # loop in our folder path
    modes_list.append(cv2.imread(os.path.join(folder_of_pathe_modes,mode)))# we append all items in modes list andadding the path to name.. # print(len(modes_list))
    
    
    
    
    
    
#load the encoding file

file=open("EncodeFile.p","rb") # open the file has stored the id and faces
get_all_encodinig_of_faces_with_id=pickle.load(file) # load ids and images
file.close() # close the file
get_all_encodinig_of_faces , student_id_list=get_all_encodinig_of_faces_with_id # to seprate them print(student_id_list) 

mode_type=0
counter=0
ids=-1
# student_image=[]

while True: 
    reading,img=cap.read()# read capture from cam
    
    Simage=cv2.resize(img,(0,0),None,0.25,0.25) # resize the main image
    Simage=cv2.cvtColor(Simage,cv2.COLOR_BGR2RGB) # convert image to RGB
    
    face_cur_frame=face_recognition.face_locations(Simage) # to find the location of the image
    encode_cur_frame=face_recognition.face_encodings(Simage,face_cur_frame) # to compare the current image with there location..
    
    background_image[162:162+480,55:55+640]=img # the dimintions of background image in our frame..
    
    background_image[44:44+633,808:808+414]=modes_list[mode_type] # active
    
    if encode_cur_frame:
         for encode_face , face_location in zip(encode_cur_frame,face_cur_frame):
                   matches_encoding=face_recognition.compare_faces(get_all_encodinig_of_faces,encode_face)
                   matches_distance=face_recognition.face_distance(get_all_encodinig_of_faces,encode_face)# lower distance is much accuracy..
                   # print("distance",matches_distance)
                   print("encoding",matches_encoding)
                   match_index=np.argmin(matches_distance) # print(match_index)
        
                   if matches_encoding[match_index]:# # print("unknown") # print(student_id_list[match_index])
                    y1,x2,y2,x1=face_location
                    y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                    bbox= 55+x1, 156+y1, x2-x1, y2-y1
                    background_image=cvzone.cornerRect(background_image,bbox,rt=0)
                    ids=student_id_list[match_index]
                    if counter== 0:
                     counter=1
                     mode_type=1
                 
         if counter !=0:
        
           if counter== 1:
             student_info=db.reference(f"Students Attendace/{ids}").get()
              # get image from storage
             
            #  blob = bucket.get_blob(f'Images/{ids}.png')
            #  array = np.frombuffer(blob.download_as_string(), np.uint8)
            #  student_image = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
            
             # ubdate data of attendance
             datetimeopject=datetime.strptime(student_info['Last_Attendance_Time'],"%Y-%m-%d %H:%M:%S %p")
             second_elaps=(datetime.now()-datetimeopject).total_seconds()
             if second_elaps>3600:
              ref=db.reference(f"Students Attendace/{ids}")
              student_info['Total Attendance']+=1
              ref.child("Total Attendance").set(student_info['Total Attendance'])
              ref.child("Last_Attendance_Time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S %p"))
             else:
              time.sleep(1)
              mode_type=3
              counter=0
              background_image[44:44+633,808:808+414]=modes_list[mode_type]  
             
           if mode_type !=3:
         
             if 10<counter<20:
              mode_type=2
              background_image[44:44+633,808:808+414]=modes_list[mode_type]   
            
             if counter<=10:
               cv2.putText(background_image,str(student_info['Total Attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
               cv2.putText(background_image,str(student_info['major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
               cv2.putText(background_image,str(ids),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
               cv2.putText(background_image,str(student_info['Standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
               cv2.putText(background_image,str(student_info['Year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
               cv2.putText(background_image,str(student_info['Starting_Year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
               (w , h), _ = cv2.getTextSize(student_info['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
               offset=(414-w)//2
               cv2.putText(background_image,str(student_info['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
              #  background_image[175:175+216,909:909+216]=student_image
        
        
        
             counter+=1
             if counter>=20:
               counter=0
               mode_type=0
               student_info=[]
               background_image[44:44+633,808:808+414]=modes_list[mode_type]
    else:
        mode_type=4
        background_image[44:44+633,808:808+414]=modes_list[mode_type]
        time.sleep(2)
        mode_type=0
        counter=0
         # cv2.imshow("Wepcam",img) # to show your caoture in the frame
    cv2.imshow("Taken Attendance",background_image) #  to read the background image in cam frame
    cv2.waitKey(1)# delay 1ms
    
        