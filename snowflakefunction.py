import snowflake.connector as sf
#import pandas as pd

def GetConnection():
    username = "anandkumar99"
    password = "India@123"
    account = "oi03177.central-india.azure"
    #warehouse = "computer_wh"
    database = "INEURON_DB"

    conn = sf.connect(user=username, password=password, account=account)

    cursor = conn.cursor()
    cursor.execute("USE DATABASE {}".format(database))

    return conn

def MakeTableStructure(conn):
    sql = "create or replace TABLE INEURON_DB.YOUTUBE_DATA.YOUTUBERS (" +\
        "id int identity(1, 1), youtuber_name VARCHAR(250), youtube_channel_url VARCHAR(250), video_link VARCHAR(250), video_comment VARCHAR(250), gdrive_video_link VARCHAR(250), " +\
        "video_likes VARCHAR(250), video_comment_count NUMBER(38,0), video_title VARCHAR(250), video_desc VARCHAR(500), video_thumbnail VARCHAR(250));"

    cursor = conn.cursor()        
    cursor.execute(sql)

def InsertChannelVideoInSnowflake(conn, channel, channel_url, video_title, video_desc, video_youtube_link, video_gdrive_link, video_comment_count, video_like_count, video_thumbnail_url):

    try:    

        sql = "INSERT INTO YOUTUBE_DATA.YOUTUBERS("+\
        "youtuber_name, youtube_channel_url, video_link, gdrive_video_link, video_likes, video_comment_count, video_title, video_desc, video_thumbnail) "+\
        " VALUES('{}','{}','{}', '{}', '{}', {}, '{}', '{}','{}');"
        sql = sql.format(channel, channel_url, video_youtube_link, video_gdrive_link, 
        video_like_count, video_comment_count, video_title, video_desc, video_thumbnail_url)
        #print(sql)
        cursor = conn.cursor()        
        cursor.execute(sql)

    except Exception as e:
        print(e)

def EmptyChannelVideos(conn):
    try:    
        sql = "Delete FROM YOUTUBE_DATA.YOUTUBERS;"
        cursor = conn.cursor()        
        cursor.execute(sql)
    except Exception as e:
        print(e)

def GetChannelVideosCount(conn, video, channel):
    try:    
        sql = "SELECT * FROM YOUTUBE_DATA.YOUTUBERS where youtuber_name='" + channel + "' and video_link='" + video + "';"
        cursor = conn.cursor()        
        cursor.execute(sql)

        videosObj = []
        for c in cursor:
            videoObj = {'id':c[0], 'youtuber_name':c[1], 'video_link':c[2]}
            videosObj.append(videoObj)

    except Exception as e:
        print(e)
    return len(videosObj)

def GetChannelVideos(conn, channel_url):
    videosObj = []
    try:    
        sql = "SELECT youtuber_name, youtube_channel_url, video_link, gdrive_video_link, video_likes, video_comment_count, video_title, video_desc, video_thumbnail FROM YOUTUBE_DATA.YOUTUBERS where youtube_channel_url='" + channel_url + "';"
        cursor = conn.cursor()    
        print(sql)    
        cursor.execute(sql)


        for c in cursor:
            videoObj = {"youtuber_name":c[0], "youtube_channel_url":c[1], "video_link":c[2], 
            "gdrive_video_link":c[3], "video_likes":c[4], "video_comment_count":c[5], 
            "video_title":c[6], "video_desc":c[7], "video_thumbnail":c[8]}
            videosObj.append(videoObj)

    except Exception as e:
        print(e)
    return videosObj
#conn = GetConnection()
#MakeTableStructure(conn)
#InsertChannelVideoInSnowflake(conn, 'anand channel', 'this is video title', 'desc of video', 'www.youtube.com1', 'gdrive/video1', 128, 110,'thumbnail url')
#print(GetChannelVideosCount(conn, 'https://www.youtube.com/watch?v=Ub9lg4FWZBA', 'Jie Jenn'))
#data = GetChannelVideos(conn,'https://www.youtube.com/user/krishnaik06')
#print(data)
