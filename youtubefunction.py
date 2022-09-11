from urllib.request import Request, urlopen
import json
from time import sleep

def get_all_video_in_channel(channel_id, api_key):
    MAX_LINK = 50 #THIS WILL DECIDE HOW MANY VIDEOS TO BE DOWNLOADED
    page_size = 25
    if page_size > MAX_LINK:
        page_size = MAX_LINK
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    loop_count = 0
    for_count = 0
    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults={}'.format(api_key, channel_id, page_size)
    WAIT_PERIOD = 5
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
        #print(channel_url)
        inp = urlopen(req)
        resp = json.load(inp)
        #print(resp)
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
                    youtuber = i['snippet']['channelTitle']
                    title = i['snippet']['title']
                    description = i['snippet']['description']
                    thumbnailurl = i['snippet']['thumbnails']['high']['url']
                    video_url = base_video_url + i['id']['videoId']
                    data = [youtuber, title, description, thumbnailurl, video_url, thumbnailurl]
                    # print(data)
                    video_data.append(data)

        try:
            next_page_token = resp['nextPageToken']
            channel_url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_data


#api_key = "AIzaSyCvf13tx3l84ProkErs-KAePMIy3LVNZlE"
#print(get_all_video_in_channel('UCvVZ19DRSLIC2-RUOeWx8ug', api_key))

