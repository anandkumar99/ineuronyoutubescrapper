import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scroll_to_end(wd):
    wd.find_element("xpath", '//body').send_keys(Keys.HOME)
    time.sleep(1)
    wd.find_element("xpath", '//body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    wd.find_element("xpath", '//body').send_keys(Keys.END)
    time.sleep(1)
    #time.sleep(sleep_between_interactions)

def fetch_comments(max_comments_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    notchangeattempt = 0
    number_results = 0
    comments_results = []
    time.sleep(3)
    scroll_to_end(wd)

    comments_count_element = wd.find_elements(By.XPATH, "(//*/yt-formatted-string[@class='count-text style-scope ytd-comments-header-renderer']/span)[1]")
    like_count_element = wd.find_elements(By.XPATH, "//*/*[contains(@aria-label, 'likes') and @class='style-scope ytd-toggle-button-renderer style-text']")

    comment_count = 0
    if len(comments_count_element) > 0: 
        comment_count = int(comments_count_element[0].text.replace(',', ''))
    like_count = 0
    if len(like_count_element) > 0:
        like_count = like_count_element[0].text
    print(comment_count)
    if comment_count > max_comments_to_fetch:
        comment_count = max_comments_to_fetch

    while number_results < comment_count:
        time.sleep(sleep_between_interactions)
        scroll_to_end(wd)

        # get all image thumbnail results
        #thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        comments_results = wd.find_elements(By.XPATH, "//*/yt-formatted-string[@class='style-scope ytd-comment-renderer']")
        if number_results == len(comments_results):
            notchangeattempt+=1
        else:
            notchangeattempt = 0            
        number_results = len(comments_results)
        if notchangeattempt > 2:
            break
        print(number_results)
    return like_count, extract_comment(comments_results)

def extract_comment(comments_results):
    comment_info = []
    #commentor_results = wd.find_elements(By.XPATH, "//*/span[@class=' style-scope ytd-comment-renderer']")
    for comment in comments_results:
        # try to click every thumbnail such that we can get the real image behind it
        #try:
        commentor_results = comment.find_elements(By.XPATH, "./../../../..//*/span[@class=' style-scope ytd-comment-renderer' or @class='style-scope ytd-comment-renderer']")

        commenter = commentor_results[0]
        comment_info.append({'comment':RemoveQuotes(comment.text), 'commentor':RemoveQuotes(commenter.text)})
    return comment_info

def RemoveQuotes(content):
    return content.replace("'", "`").replace('"', "`")

def GetYoutubeVideoComments(url, max_comment):
    DRIVER_PATH = r'chromedriver.exe'
    # load the page
    with webdriver.Chrome(executable_path=DRIVER_PATH) as wd:
        wd.get(url)
        wd.maximize_window()
        res = fetch_comments(max_comment, wd, 0.5)  
        return res


#search_url = "https://www.youtube.com/watch?v=2CRY5BYf-js"
#likes, comments = GetYoutubeVideoComments(search_url, 100)
#print(likes)
#print(comments)
