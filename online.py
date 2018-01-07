"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""
import ConfigParser
import time

from selenium import webdriver


def assign_settings():
    """
    Loading and assigning global variables from our settings.txt file
    """
    config_parser = ConfigParser.RawConfigParser()
    config_file_path = 'settings.txt'
    config_parser.read(config_file_path)

    firefox_path = config_parser.get('your-config', 'FIREFOX_PATH')
    name = config_parser.get('your-config', 'NAME')
    page = config_parser.get('your-config', 'PAGE')

    settings = {'firefox_path': firefox_path, 'name': name, 'page': page}
    return settings


def search_chatter(driver, settings):
    """
    Function that search the specified user and activates his chat
    """

    while True:
        for chatter in driver.find_elements_by_xpath("//div[@class='_2wP_Y']"):
            chatter_name = chatter.find_element_by_xpath(
                ".//span[@class='emojitext ellipsify']").text
            if chatter_name == settings['name']:
                chatter.find_element_by_xpath(
                    ".//div[@class='chat-drag-cover']").click()
                return


def main():
    """
    Loading all the configuration and opening the website
    (Firefox profile where whatsapp web is already scanned)
    """
    settings = assign_settings()
    firefox_profile = webdriver.FirefoxProfile(settings['firefox_path'])
    driver = webdriver.Firefox(firefox_profile)
    driver.get(settings['page'])

    search_chatter(driver, settings)
    """
    Waiting 10 sec before closing the navigator
    """
    time.sleep(10)
    driver.close()


if __name__ == '__main__':
    main()
