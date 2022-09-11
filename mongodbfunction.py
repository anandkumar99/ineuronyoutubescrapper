import pymongo

def AddCommentsToMongoDB(channel, channel_url, youtube_link, comments, thumbnail_base64):
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.vojhzqn.mongodb.net/?retryWrites=true&w=majority")

    database = client['myDB']
    col1 = database['youtuber_comments']

    data = {"channel":channel, "channel_url":channel_url, "youtube_link":youtube_link, "comments":comments, "thumbnail_base64":thumbnail_base64}

    col1.insert_one(data)

def GetCommentsFromMongoDB(youtube_link):
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.vojhzqn.mongodb.net/?retryWrites=true&w=majority")

    database = client['myDB']
    col1 = database['youtuber_comments']

    record = col1.find({"youtube_link" : youtube_link})

    for data in record:
        return data["comments"], data["thumbnail_base64"]
 
# comments, thumbnail = GetCommentsFromMongoDB('https://www.youtube.com/watch?v=4VVhwfVf1k8')
# print(comments)


