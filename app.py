from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from gdrive import *
from youtubefunction import *
from snowflakefunction import *
from videotest import *
import uuid
import shutil

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    #filelist = getFileList()
    #return '<br>'.join(filelist)
    return render_template("index.html")


@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    api_key = "AIzaSyCvf13tx3l84ProkErs-KAePMIy3LVNZlE"
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            channel = requests.get(searchString)
            channel.encoding='utf-8'
            content = channel.text
            startIndex = content.index('https://www.youtube.com/feeds/videos.xml?')
            endIndex = content.index('"', startIndex)
            channelid = content[startIndex+52:endIndex]
            print("channel id", channelid)
            conn = GetConnection()
            channelvideos = get_all_video_in_channel(channelid, api_key)
            print(channelvideos)

            deleteAllFilesInGDriveFolder()
            currdir = os.getcwd()
            SAVE_PATH = os.path.join(currdir, "video")
            if os.path.exists(SAVE_PATH):
                shutil.rmtree(SAVE_PATH)

            print(channelvideos)
            request_id = uuid.uuid4().hex
            for video in channelvideos:
                filepath = SaveYouTubeVideo(video[3], request_id, SAVE_PATH)
                if filepath != "Some Error!":
                    filepath = uploadFile(filepath)
                InsertChannelVideoInSnowflake(conn, request_id, video[0], video[1], '', video[3], filepath, video[4], video[5], video[6])

       
            #     mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
            #               "Comment": custComment}

            videos = GetChannelVideos(conn)
            print(videos)
            return render_template('results.html', videos=videos[0:(len(videos)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'


    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run( port=8001)
