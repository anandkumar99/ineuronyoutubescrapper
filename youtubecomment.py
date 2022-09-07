from googleapiclient.discovery import build
  
def video_comments(video_id, api_key):
    final_comments = []
  
    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)
    comment_count = 0
    # retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id
    ).execute()
  
    # iterate video response
    while video_response:
        
        # extracting required info
        # from each result object 
        for item in video_response['items']:
            comment_count = comment_count + 1
            if comment_count > 10:
                return final_comments
            # print(item)
            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            commentor = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            commentorThumbnail = item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
            final_comments.append([comment, commentor, commentorThumbnail])
            
  
        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id
                ).execute()
        else:
            break
  

# video_id = "-ePdbG39wqI"
# api_key = 'AIzaSyCvf13tx3l84ProkErs-KAePMIy3LVNZlE'
# Call function
# comments = video_comments(video_id, api_key)
# print(comments)