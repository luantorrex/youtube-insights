from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.youtube.com/c/TheBeatles/videos?view=0&sort=dd&shelf_id=0')

for _ in range(10):
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(3)

htmlContent = driver.page_source

soup = BeautifulSoup(htmlContent, 'html.parser')

videos = soup.find_all('div',{"id":"dismissable"})

master_list = []

for video in videos:
    video_info = {}
    video_info['title'] = video.find('a', {'id':'video-title'}).text
    
    views = video.find('span', {'class' : 'ytd-grid-video-renderer'}).text.split(" ")[0]
    if 'K' in views:
        views = views.replace('K', '')
        video_info['views'] = float(views) * 1000
    elif 'M' in views:
        views = views.replace('M', '')
        video_info['views'] = float(views) * 1000000
    master_list.append(video_info)

driver.close()

import pandas as pd
df = pd.DataFrame(master_list)
df.to_csv("beatles.csv", index=False)