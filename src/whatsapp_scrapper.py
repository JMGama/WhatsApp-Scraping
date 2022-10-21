"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WhatsappScrapper():
    def __init__(self, page, browser, browser_path, driver_path):
        self.page = page
        self.browser = browser
        self.browser_path = browser_path
        self.driver_path = driver_path
        self.driver = self.load_driver()

        # Open the web page with the given browser
        self.driver.get(self.page)

    def load_driver(self):
        """
        Load the Selenium driver depending on the browser
        (Edge and Safari are not running yet)
        """
        driver = None
        if self.browser == 'firefox':
            firefox_profile = webdriver.FirefoxProfile(
                self.browser_path)
            driver = webdriver.Firefox(firefox_profile)
        elif self.browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            if self.browser_path:
                chrome_options.add_argument('user-data-dir=' +
                                            self.browser_path)
            driver = webdriver.Chrome(self.driver_path, options=chrome_options)
        elif self.browser == 'safari':
            pass
        elif self.browser == 'edge':
            pass

        return driver

    def open_conversation(self, name):
        """
        Function that search the specified user by the 'name' and opens the conversation.
        """

        while True:
            for chatter in self.driver.find_elements_by_xpath("//div[@id='pane-side']/div/div/div/div"):
                chatter_path = ".//span[@title='{}']".format(
                    name)

                # Wait until the chatter box is loaded in DOM
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[contains(@title,'{}')]".format(
                                name)))
                    )
                except StaleElementReferenceException:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[contains(@title,'{}')]".format(
                                name)))
                    )

                try:
                    chatter_name = chatter.find_element_by_xpath(
                        chatter_path).text
                    if chatter_name == name:
                        chatter.find_element_by_xpath(
                            ".//div/div").click()
                        return True
                except Exception as e:
                    pass

    def read_last_in_message(self):
        """
        Reading the last message that you got in from the chatter
        """
        message = ""
        message_emojis = []
        quote = ""
        quote_emojis = []
        quote_by = ""

        for messages in self.driver.find_elements_by_xpath(
                "//div[contains(@class,'message-in')]"):
            try:

                # Get message
                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")

                message = message_container.find_element_by_xpath(
                    ".//span[contains(@class,'copyable-text')]"
                ).text

                # Get emojis
                for emoji in message_container.find_elements_by_xpath(
                        ".//img[contains(@class,'copyable-text')]"
                ):
                    message_emojis.append(
                        emoji.get_attribute("data-plain-text"))

               # Get quoted message
                quote_container = message_container.find_element_by_xpath(
                    ".//span[contains(@class,'quoted-mention')]")

                quote = quote_container.text

                quote_by = message_container.find_element_by_xpath(
                    ".//span[contains(@class,'i0jNr')]").text

                # Get quoted emojis
                for emoji in quote_container.find_elements_by_xpath(
                        ".//img[contains(@class,'emoji')]"
                ):
                    quote_emojis.append(emoji.get_attribute("alt"))

            except NoSuchElementException as e:  # In case there are only emojis in the message
                try:
                    message_container = messages.find_element_by_xpath(
                        ".//div[contains(@class,'copyable-text')]")

                    for emoji in message_container.find_elements_by_xpath(
                            ".//img[contains(@class,'copyable-text')]"
                    ):
                        message_emojis.append(
                            emoji.get_attribute("data-plain-text"))
                except NoSuchElementException:
                    pass

        return message, message_emojis, quote, quote_emojis, quote_by

    def send_message(self, text):
        """
        Send a message to the chatter.
        You need to open a conversation with open_conversation()
        before you can use this function.
        """

        input_text = self.driver.find_element_by_xpath(
            "//div[@id='main']/footer/div/div[2]/div/div[@contenteditable='true']")

        input_text.click()
        input_text.send_keys(text)

        send_button = self.driver.find_element_by_xpath(
            "//div[@id='main']/footer/div/div[3]/button")
        send_button.click()

        return True
