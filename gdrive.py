from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import requests
import json

def getFolderId():
    return '1quDuPyGoHPmWLJiUwWabpDHiyAb6bx8c'

def getAuth():
    gauth = GoogleAuth()           
    drive = GoogleDrive(gauth)  
    return gauth, drive      

def uploadFile(filepath):

    gauth, drive = getAuth()
    file1 = drive.CreateFile(metadata={"title": "myfile.jpg", "parents": [{"kind": 'drive#fileLink', "id": getFolderId()}]})
    file1.SetContentFile(filepath)  # Set content of the file from given string.
    file1.Upload(param={'supportsTeamDrives': True})

    access_token = gauth.credentials.access_token # gauth is from drive = GoogleDrive(gauth) Please modify this for your actual script.
    file_id = file1['id']
    url = 'https://www.googleapis.com/drive/v3/files/' + file_id + '/permissions?supportsAllDrives=true'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {'type': 'anyone', 'value': 'anyone', 'role': 'reader'}
    res = requests.post(url, data=json.dumps(payload), headers=headers)

    # SHARABLE LINK
    return file1['alternateLink']




def getFileList():   
    fileList = []
    gauth, drive = getAuth()     
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(getFolderId())}).GetList()
    for file in file_list:
        #print(file)
        fileList.append('title: %s, id: %s shared:%s link: %s' % (file['title'], file['id'], file['shared'], file['alternateLink']))
    return fileList

        
        
#upload_filename = os.path.join(os.getcwd(), 'test\\thumbnail\\r3pMQ8-Ad5s.jpg')
#fileLink = uploadFile(upload_filename)
#print(fileLink)
#filelist = getFileList()
#print(filelist)