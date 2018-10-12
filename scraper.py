"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""
import ConfigParser
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def load_settings():
    """
    Loading and assigning global variables from our settings.txt file
    """
    config_parser = ConfigParser.RawConfigParser()
    config_file_path = 'mysettings.txt'
    config_parser.read(config_file_path)

    browser = config_parser.get('your-config', 'BROWSER')
    browser_path = config_parser.get('your-config', 'BROWSER_PATH')
    name = config_parser.get('your-config', 'NAME')
    page = config_parser.get('your-config', 'PAGE')

    settings = {
        'browser': browser,
        'browser_path': browser_path,
        'name': name,
        'page': page
    }
    return settings


def load_driver(settings):
    """
    Load the Selenium driver depending on the browser
    (Edge and Safari are not running yet)
    """
    driver = ''
    if settings['browser'] == 'firefox':
        firefox_profile = webdriver.FirefoxProfile(settings['browser_path'])
        driver = webdriver.Firefox(firefox_profile)
    elif settings['browser'] == 'edge':
        pass
    elif settings['browser'] == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "user-data-dir=" + settings['browser_path'])
        driver = webdriver.Chrome(chrome_options=chrome_options)
    elif settings['browser'] == 'safari':
        pass

    return driver


def search_chatter(driver, settings):
    """
    Function that search the specified user and activates his chat
    """

    while True:
        for chatter in driver.find_elements_by_xpath("//div[@class='_2wP_Y']"):
            chatter_name = chatter.find_element_by_xpath(
                ".//span[@class='_1wjpf']").text
            if chatter_name == settings['name']:
                chatter.find_element_by_xpath(
                    ".//div[@tabindex='-1']").click()
                return


def read_last_in_message(driver):
    """
    Reading the last message that you got in from the chatter
    """
    message = ''
    for messages in driver.find_elements_by_xpath("//div[@class='_3_7SH _3DFk6 message-in']"):
        try:
            message_container = messages.find_element_by_xpath(
                ".//div[@class='copyable-text']"
            )
            message = message_container.find_element_by_xpath(
                ".//span[@class='selectable-text invisible-space copyable-text']"
            ).text
        except NoSuchElementException:
            try:
                message_container = messages.find_element_by_xpath(
                    ".//div[@class='message message-chat message-in tail message-chat']"
                )
                message = message_container.find_element_by_xpath(
                    ".//span[@class='emojitext selectable-text invisible-space copyable-text']"
                ).text
            except NoSuchElementException:
                pass

    return message


def main():
    """
    Loading all the configuration and opening the website
    (Browser profile where whatsapp web is already scanned)
    """
    settings = load_settings()
    driver = load_driver(settings)
    driver.get(settings['page'])

    search_chatter(driver, settings)

    previous_in_message = ''
    while True:
        last_in_message = read_last_in_message(driver)

        if previous_in_message != last_in_message:
            print last_in_message
            previous_in_message = last_in_message

        time.sleep(1)


if __name__ == '__main__':
    main()
