from selenium import webdriver
import time

# Assigning global variables
FIREFOX_PATH = "/home/gama/.mozilla/firefox/kpnk7t0r.default"
NAME = 'Gian'
PAGE = "https://web.whatsapp.com/"

# Function that search the specified user and activates his chat
def search_chatter(driver):
    while True:
        for chatter in driver.find_elements_by_xpath("//div[@class='_2wP_Y']"):
            chatter_name = chatter.find_element_by_xpath(".//span[@class='emojitext ellipsify']").text
            if chatter_name == NAME:
                chatter.find_element_by_xpath(".//div[@class='chat-drag-cover']").click()
                return

# Loading all the configuration and opening the website (Firefox profile where whatsapp web is already scanned)

firefox_profile = webdriver.FirefoxProfile(FIREFOX_PATH)
driver = webdriver.Firefox(firefox_profile)
driver.get(PAGE)

search_chatter(driver)

# Waiting 10sec before closing the navigator
time.sleep(10)

driver.close()
