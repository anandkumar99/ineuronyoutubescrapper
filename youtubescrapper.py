import requests
from gdrive import *
from youtubefunction import *
from snowflakefunction import *
from videotest import *
from loadcomment import *
from mongodbfunction import *
import shutil
import base64

def YoutubeChannelScrapping(channel_url):
    api_key = "AIzaSyCvf13tx3l84ProkErs-KAePMIy3LVNZlE"
    channel = requests.get(channel_url)
    channel.encoding='utf-8'
    content = channel.text
    startIndex = content.index('https://www.youtube.com/feeds/videos.xml?')
    endIndex = content.index('"', startIndex)
    channelid = content[startIndex+52:endIndex]
    # print("channel id", channelid)
    conn = GetConnection()
    #EmptyChannelVideos(conn)
    channelvideos = get_all_video_in_channel(channelid, api_key)
    # print(channelvideos)

    currdir = os.getcwd()
    SAVE_PATH = os.path.join(currdir, "video")
    if os.path.exists(SAVE_PATH):
        shutil.rmtree(SAVE_PATH)

    upload_max = 50
    uploaded_count = 1
    # print(channelvideos)
    for video in channelvideos:
        if 'LIVE' in video[1].upper():
            continue
        if GetChannelVideosCount(conn, video[4], video[0]) == 0: #check if video is already in backend then skip
            if uploaded_count < upload_max: #check if already reached max upload video
                uploaded_count += 1
                channel_name = video[0]
                youtube_link = video[4]
                likes, comments = GetYoutubeVideoComments(youtube_link, 100)
                comment_count = len(comments)
                thumbnail_base64 = GetWebImageBase64(video[5])
                AddCommentsToMongoDB(channel_name, channel_url, youtube_link, comments, thumbnail_base64)
                print(comments)
                filepath = SaveYouTubeVideo(video[4], video[0], SAVE_PATH)
                if filepath != "Some Error!":
                    filepath = uploadFileToGDrive(filepath)
                InsertChannelVideoInSnowflake(conn, RemoveQuotes(video[0]), channel_url, RemoveQuotes(video[1]), RemoveQuotes(video[2]), video[4], filepath, comment_count, likes, video[5])
                
            else:
                return

def RemoveQuotes(content):
    return content.replace("'", "`").replace('"', "`")

def GetWebImageBase64(url):
    return base64.b64encode(requests.get(url).content)

YoutubeChannelScrapping('https://www.youtube.com/user/javaboynavin')
#Krish nail : https://www.youtube.com/user/krishnaik06
#My SirG : https://www.youtube.com/user/saurabhexponent1
#Hitesh : https://www.youtube.com/c/HiteshChoudharydotcom
#Telusko : https://www.youtube.com/user/javaboynavin
