import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"database url"
    
    
})

ref=db.reference("Students Attendace")

data= {
    
    "21410857":
        {
         "name":"Pill Gates",
         "major":"Data Science",
         "Starting_Year":2020,
         "Total Attendance":0,  
         "Standing":"E",
         "Year":2,
         "Last_Attendance_Time":"2023-3-2 00:23:33 AM"
            
        },
    "21610857":
        {
         "name":"Elon Mask",
         "major":"Space X",
         "Starting_Year":2020,
         "Total Attendance":0,  
         "Standing":"E",
         "Year":2,
         "Last_Attendance_Time":"2023-3-2 00:23:33 AM"
            
        },
    "21210857":
        {
         "name":"Emily",
         "major":"Actor",
         "Starting_Year":2020,
         "Total Attendance":0,  
         "Standing":"E",
         "Year":2,
         "Last_Attendance_Time":"2023-3-2 00:23:33 AM"
            
        }
}    
   









for key , value in data.items():
     ref.child(key).set(value)
