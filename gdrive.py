from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def getFolderId():
    return '1quDuPyGoHPmWLJiUwWabpDHiyAb6bx8c'

def getAuth():
    gauth = GoogleAuth()           
    drive = GoogleDrive(gauth)  
    return drive      

def uploadFile(filepath):

    drive = getAuth()
    gfile = drive.CreateFile({'parents': [{'id': getFolderId()}], 'title':'myfile.jpg'})
    # Read file and set it as the content of this instance.
    print(gfile)

    gfile.SetContentFile(filepath)
    gfile.Upload() # Upload the file.
        
def getFileList():   
    fileList = []
    drive = getAuth()     
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(getFolderId())}).GetList()
    for file in file_list:
        fileList.append('title: %s, id: %s' % (file['title'], file['id']))
    return fileList

        
        
#upload_filename = os.path.join(os.getcwd(), 'thumbnail\\r3pMQ8-Ad5s.jpg')
#uploadFile(upload_filename)
#filelist = getFileList()
#print(filelist)