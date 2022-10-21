import configparser
import time

from whatsapp_scrapper import WhatsappScrapper


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
    driver_path = config_parser.get('config', 'DRIVER_PATH')

    settings = {
        'browser': browser,
        'browser_path': browser_path,
        'name': name,
        'page': page,
        'driver_path': driver_path
    }
    return settings


def main():
    """
    Loading all the configuration and opening the website
    (Browser profile where whatsapp web is already scanned)
    """
    settings = load_settings()
    scrapper = WhatsappScrapper(
        settings['page'], settings['browser'], settings['browser_path'], settings['driver_path'])

    if scrapper.open_conversation(settings['name']):
        # scrapper.send_message("hola")
        previous_in_message = None
        while True:
            last_in_message, message_emojis, quote, quote_emojis, quote_by = scrapper.read_last_in_message()

            if previous_in_message != last_in_message:
                print(last_in_message, message_emojis,
                      quote, quote_emojis, quote_by)
                previous_in_message = last_in_message

            time.sleep(1)


if __name__ == '__main__':
    main()
