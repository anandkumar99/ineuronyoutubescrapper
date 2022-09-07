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
    sql = "create or replace TABLE INEURON_DB.YOUTUBE_DATA.VIDEO_DETAIL (" +\
        "REQUESTID VARCHAR(100), VIDEO_TITLE VARCHAR(250), VIDEO_DESC VARCHAR(1000), VIDEO_YOUTUBER VARCHAR(250)," +\
        "VIDEO_LINK_YOUTUBE VARCHAR(250), VIDEO_LINK_GDRIVE VARCHAR(250), VIDEO_LIKES NUMBER(38,0)," +\
        "VIDEO_COMMENT_COUNT NUMBER(38,0), VIDEO_THUMBNAIL_URL VARCHAR(250));"

    cursor = conn.cursor()        
    cursor.execute(sql)

def InsertChannelVideoInSnowflake(conn, request_id, video_title, video_desc, video_youtuber, video_youtube_link, video_link, video_comment_count, video_like_count, video_thumbnail_url):

    try:    

        sql = "INSERT INTO YOUTUBE_DATA.VIDEO_DETAIL(REQUESTID, "+\
        "VIDEO_COMMENT_COUNT, VIDEO_LIKES, VIDEO_LINK_GDRIVE, VIDEO_LINK_YOUTUBE, "+\
        "VIDEO_YOUTUBER, VIDEO_TITLE, VIDEO_DESC, VIDEO_THUMBNAIL_URL) VALUES('{}', {}, "+\
        "{}, '{}', '{}', '{}', '{}', '{}','{}');"
        sql = sql.format(request_id, video_comment_count,
        video_like_count, video_link, video_youtube_link, 
        video_youtuber, video_title, video_desc, video_thumbnail_url)
        #print(sql)
        cursor = conn.cursor()        
        cursor.execute(sql)

        sql = "SELECT * FROM YOUTUBE_DATA.VIDEO_DETAIL;"
        cursor = conn.cursor()        
        cursor.execute(sql)
        for c in cursor:
            print(c)

    except Exception as e:
        print(e)

def GetChannelVideos(conn):
    try:    
        sql = "SELECT * FROM YOUTUBE_DATA.VIDEO_DETAIL;"
        cursor = conn.cursor()        
        cursor.execute(sql)

        videosObj = []
        for c in cursor:
            videoObj = {'requestid':c[0], 'title':c[1], 'desc':c[2], 'youtuber':c[3], 
            'youtubelink':c[4], 'gdrivelink':c[5], 'like':c[6], 'comments':c[7], 'thumbnail':c[8]}
            videosObj.append(videoObj)

    except Exception as e:
        print(e)
    return videosObj
conn = GetConnection()
MakeTableStructure(conn)
#InsertChannelVideo(conn, '17173647384', 'title of video1',
#        'anand', 'www.youtube.com1', 'gdrive/video1', 128, 110)
#GetChannelVideos(conn)
