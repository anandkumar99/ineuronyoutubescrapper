from pytube import YouTube 
import os
 
def createFolder(folderpath):
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)    

def SaveYouTubeVideo(youtubeLink, channel, SAVE_PATH):
    #where to save 
    print(SAVE_PATH)
    createFolder(SAVE_PATH)

    SAVE_PATH = os.path.join(SAVE_PATH, channel)
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
        print("error to download : " , youtubeLink)
        return "Some Error!"
    
    #filters out all the files with "mp4" extension 
    mp4files = yt.streams.filter(progressive = True, file_extension = "mp4").get_lowest_resolution()
   
    try: 
        video_size = mp4files.filesize
        print("video size ", video_size)
        # download video from the YouTube 
        if video_size < 50000000:   #file must be smaller than 50mb
            return mp4files.download(output_path = SAVE_PATH) 
        else:
            return "Some Error!"
    except: 
        return "Some Error!"
        
#file = SaveYouTubeVideo('https://www.youtube.com/watch?v=Ub9lg4FWZBA','test channel', r'C:\Users\EI07949\Desktop\AI Training\Python\Project\YoutubeScrapper\video\test')
#print(file)