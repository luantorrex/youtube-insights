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

    driver.close()

    return channelName, views, countOfSubs

"""
def getCountofViews(channelLink):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    linkToAbout = channelLink + '/about'
    driver.get(linkToAbout)
    
    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')
    views = soup.find_all('yt-formatted-string', {'class', 'style-scope ytd-channel-about-metadata-renderer'})[-1].text
    driver.close()
    return views
"""