from urllib.request import Request, urlopen
import json
from bs4 import BeautifulSoup as bs
from time import sleep
import requests

def get_all_video_in_channel(channel_id, api_key):
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    loop_count = 0
    for_count = 0
    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=10'.format(api_key, channel_id)
    WAIT_PERIOD = 5
    MAX_LINK = 2 #THIS WILL DECIDE HOW MANY VIDEOS TO BE DOWNLOADED
    video_count = 0
    video_data = []
    channel_url = first_url
    while True:
        loop_count = loop_count + 1
        #print("Loop count", loop_count)
        if loop_count > 10:
            break
        #page=urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
        #infile=urllib.request.urlopen(page).read()
        if loop_count > 1:
            sleep(WAIT_PERIOD) # sleep for a while until next retry

        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

        req = Request(
            url=channel_url, 
            headers=hdr
        )
        print(channel_url)
        inp = urlopen(req)
        resp = json.load(inp)

        for i in resp['items']:
            for_count = for_count + 1
            print("for count", for_count)
            #print(i)
            if i['id']['kind'] == "youtube#video":
                video_count = video_count + 1
                #print("video count", video_count)
                if video_count > MAX_LINK:
                    print("reached max link")
                    return video_data
                else:
                    title = i['snippet']['title']
                    description = i['snippet']['description']
                    thumbnailurl = i['snippet']['thumbnails']['high']['url']
                    video_url = base_video_url + i['id']['videoId']
                    video_like_data = scrape_info(video_url)
                    data = [title, description, thumbnailurl, video_url, video_like_data['views'], video_like_data['likes'], thumbnailurl]
                    print(data)
                    video_data.append(data)

        try:
            next_page_token = resp['nextPageToken']
            channel_url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_data

# creating function
def scrape_info(url):
      
    # getting the request from url
    r = requests.get(url)
      
    # converting the text
    s = bs(r.text, "html.parser")
    
    # finding meta info for title
    title = s.find("meta", itemprop="name")['content']
      
    # finding meta info for views
    views = s.find("meta", itemprop="interactionCount")['content']
      
    #duration = s.find("span", {"class": "ytp-time-duration"}).text

    # finding meta info for likes
    content = r.text
    startLike = content.index('likes"}},"simpleText":"')
    startLike = startLike + 23
    endLike = content.index('"', startLike)
    likes = content[startLike: endLike]
      
    # saving this data in dictionary
    data = {'views':views, 'likes':likes}
      
    # returning the dictionary
    return data

#api_key = "AIzaSyCvf13tx3l84ProkErs-KAePMIy3LVNZlE"
#print(get_all_video_in_channel('UCvVZ19DRSLIC2-RUOeWx8ug', api_key))

#print(scrape_info("https://www.youtube.com/watch?time_continue=17&v=2wEA8nuThj8"))
