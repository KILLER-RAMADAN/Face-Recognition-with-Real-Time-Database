import cv2
import face_recognition
import pickle
import os
import numpy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


# connect with the database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"database url",
    'storageBucket':"storage url"
    
    
})
# connect with the database






# importing the student images...

folder_of_pathe_S_images="images" # to read all modes from the folder

list_of_images=os.listdir(folder_of_pathe_S_images) # to read all names of photos

# print(list_of_images)

students_images_list=[]# empty list

student_id_list=[]# students id list

for image in list_of_images: # loop in our folder path
    students_images_list.append(cv2.imread(os.path.join(folder_of_pathe_S_images,image)))# we append all items in modes list andadding the path to name.. 
    remove_jpg=os.path.splitext(image)[0] # to take only the id number
    student_id_list.append(remove_jpg)# adding all id in student_id_list # print(student_id_list)
    
    
    
    # sending data to firebase
    file_name=f"{folder_of_pathe_S_images}/{image}"
    Bucket=storage.bucket()
    blob=Bucket.blob(file_name)
    blob.upload_from_filename(file_name)
    # sending data to firebase
    
    
    
    
    


def get_encoding_of_images(images_list): # we made a function to find encoding of all photos...
    encode_list=[]
    for img in images_list:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0] # get encoding of photos
        encode_list.append(encode)
    return encode_list
print("process encoding")
get_all_encodinig_of_faces=get_encoding_of_images(students_images_list) # print(get_all_encodinig_of_faces) 
print("done encoding")
get_all_encodinig_of_faces_with_id=[get_all_encodinig_of_faces,student_id_list]

file=open("EncodeFile.p","wb")
pickle.dump(get_all_encodinig_of_faces_with_id,file)
file.close()
print("file saved")
