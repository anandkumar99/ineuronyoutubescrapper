from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from gdrive import *
from youtubefunction import *
from snowflakefunction import *
from mongodbfunction import *

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
            channel = request.form['content'].replace(" ","")
            conn = GetConnection()
            data = GetChannelVideos(conn, channel)

            return render_template('results.html', videos=data[0:(len(data)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    else:
        return render_template('index.html')

@app.route('/comments',methods=['GET']) # route to show the review comments in a web UI
@cross_origin()
def comments():
    print("got request")
    try:
        print("get url")
        data = request.args
        video_url = data['video']
        comments, thumbnail = GetCommentsFromMongoDB(video_url)
        return render_template('comments.html', comments=comments[0:(len(comments)-1)], thumbnail=thumbnail)
    except Exception as e:
        print('The Exception message is: ',e)
        return 'something is wrong'

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run( port=8001)
