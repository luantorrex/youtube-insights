from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def getChannelName(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.youtube.com/'+url)
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
    driver.close()
    return channelName