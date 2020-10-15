"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""
import configparser
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def load_settings():
    """
    Loading and assigning global variables from our settings.txt file
    """
    config_parser = configparser.RawConfigParser()
    config_file_path = 'settings.txt'
    config_parser.read(config_file_path)

    browser = config_parser.get('config', 'BROWSER')
    browser_path = config_parser.get('config', 'BROWSER_PATH')
    name = config_parser.get('config', 'NAME')
    page = config_parser.get('config', 'PAGE')

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
    driver = None
    if settings['browser'] == 'firefox':
        firefox_profile = webdriver.FirefoxProfile(settings['browser_path'])
        driver = webdriver.Firefox(firefox_profile)
    elif settings['browser'] == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        if settings['browser_path']:
            chrome_options.add_argument('user-data-dir=' +
                                        settings['browser_path'])
        driver = webdriver.Chrome(options=chrome_options)
    elif settings['browser'] == 'safari':
        pass
    elif settings['browser'] == 'edge':
        pass

    return driver


def search_chatter(driver, settings):
    """
    Function that search the specified user and activates his chat
    """

    while True:
        for chatter in driver.find_elements_by_xpath("//div[@id='pane-side']/div/div/div/div"):
            chatter_path = "//span[contains(@title,'{}')]".format(
                settings['name'])
            try:
                chatter_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, chatter_path))
                ).text
            except StaleElementReferenceException:
                chatter_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, chatter_path))
                ).text

            if chatter_name == settings['name']:
                chatter.find_element_by_xpath(
                    ".//div/div").click()
                return True


def read_last_in_message(driver):
    """
    Reading the last message that you got in from the chatter
    """
    for messages in driver.find_elements_by_xpath(
            "//div[contains(@class,'message-in')]"):
        try:
            message = ""
            emojis = []

            message_container = messages.find_element_by_xpath(
                ".//div[@class='copyable-text']")

            message = message_container.find_element_by_xpath(
                ".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
            ).text

            for emoji in message_container.find_elements_by_xpath(
                    ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
            ):
                emojis.append(emoji.get_attribute("data-plain-text"))

        except NoSuchElementException:  # In case there are only emojis in the message
            try:
                message = ""
                emojis = []
                message_container = messages.find_element_by_xpath(
                    ".//div[contains(@class,'copyable-text')]")

                for emoji in message_container.find_elements_by_xpath(
                        ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))
            except NoSuchElementException:
                pass

    return message, emojis


def main():
    """
    Loading all the configuration and opening the website
    (Browser profile where whatsapp web is already scanned)
    """
    settings = load_settings()
    driver = load_driver(settings)
    driver.get(settings['page'])

    if search_chatter(driver, settings):
        previous_in_message = None
        while True:
            last_in_message, emojis = read_last_in_message(driver)

            if previous_in_message != last_in_message:
                print(last_in_message, emojis)
                previous_in_message = last_in_message

            time.sleep(1)


if __name__ == '__main__':
    main()
