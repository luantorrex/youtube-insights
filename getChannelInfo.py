from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

############# Futuramente, é aconselhável criar funções distintas, a fim de tornar o programa menos acoplado

def getChannelInfo(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    ##############                  getChannelName                  ################
    driver.get('https://www.youtube.com/'+ url)
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    user = soup.find('a', {'class','ytd-video-owner-renderer'})['href']
    channelLink = 'https://www.youtube.com' + user

    driver.get(channelLink)
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    channelName = soup.find('div', {'class', 'style-scope ytd-channel-name'}).text.strip().split('\n')[0]

    ##############                  getCountOfSubs                  ################
    countOfSubs = soup.find_all('yt-formatted-string', {'class', 'ytd-c4-tabbed-header-renderer'})[0].text.split(' ')[0]

    ##############                  getCountOfViews                  ################
    linkToAbout = channelLink + '/about'
    driver.get(linkToAbout)
    
    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')
    views = soup.find_all('yt-formatted-string', {'class', 'style-scope ytd-channel-about-metadata-renderer'})[-1].text

    ##############                  getAverageOfViews                  ################

    linkToVideos = channelLink + '/videos?view=0&sort=dd&shelf_id=0'
    driver.get(linkToVideos)

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
        
        viewsPerVideo = video.find('span', {'class' : 'ytd-grid-video-renderer'}).text.split(" ")[0]
        if 'K' in viewsPerVideo:
            viewsPerVideo = viewsPerVideo.replace('K', '')
            video_info['views'] = float(viewsPerVideo) * 1000
        elif 'M' in viewsPerVideo:
            viewsPerVideo = viewsPerVideo.replace('M', '')
            video_info['views'] = float(viewsPerVideo) * 1000000
        master_list.append(video_info)

    numberOfVideos = len(master_list)
    #intViews = int(views.split(' views')[0].replace(',', ''))

    #################################################################################
    driver.close()

    return channelName, views, countOfSubs, numberOfVideos