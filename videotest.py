from pytube import YouTube 
import os
 
def createFolder(folderpath):
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)    

def SaveYouTubeVideo(youtubeLink, folderid, SAVE_PATH):
    #where to save 

    createFolder(SAVE_PATH)

    SAVE_PATH = os.path.join(SAVE_PATH, folderid)
    createFolder(SAVE_PATH)
    #link of the video to be downloaded    
    # for file in os.scandir(SAVE_PATH):
    #    os.remove(file.path)

    try: 
        # object creation using YouTube
        # which was imported in the beginning 
        yt = YouTube(youtubeLink) 
    except: 
        
        #to handle exception 
        return "Some Error!"
    
    #filters out all the files with "mp4" extension 
    mp4files = yt.streams.filter(progressive = True, file_extension = "mp4").get_lowest_resolution()

    try: 
        # download video from the YouTube 
        return mp4files.download(output_path = SAVE_PATH) 
    except: 
        return "Some Error!"
        
# SaveYouTubeVideo('https://www.youtube.com/watch?v=VQ9dSqtlBBc', 'oifeoituposdfs')