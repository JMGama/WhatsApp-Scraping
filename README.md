# :speech_balloon: WhatsApp-Scraping

Python script to get WhatsApp information from WhatsApp Web

# Requirements

All the libraries that we are going to use are in the [requirements.txt](requirements.txt) file.
You can install it with PIP in the terminal with:

```
sudo pip install -r requirements.txt
```

In order to make this project work you need to have a profile in your browser where you already scanned the QR with your account then we are going to use that account for launching the Selenium driver.

## Selenium

Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: Message: ‘geckodriver’ executable needs to be in PATH.

Other supported browsers will have their own drivers available. Links to some of the more popular browser drivers follow.

- [Chrome](https://chromedriver.chromium.org/downloads)
- [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- [Firefox](https://github.com/mozilla/geckodriver/releases)
- [Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)

> For more information you can go to the [Selenium Website](http://selenium-python.readthedocs.io/installation.html) at the installation section.

### Chrome driver

#### Windows

For Windows we recommend that you download the [Chrome driver](https://chromedriver.chromium.org/downloads) and save it in your chrome directory _(default path: C:\Program Files (x86)\Google\Chrome)_.

In the requirements.txt file you can set the path to the chrome driver <code>DRIVER_PATH = C:\Program Files (x86)\Google\Chrome\chromedriver</code>. With this configuration the script will know where to find the driver.

# Settings

**AT THIS MOMENT THE PROJECT ONLY WORKS WITH FIREFOX AND CHROME**

## Browser Profile `FIREFOX_PATH`

You need to setup your configuration in the [settings.txt](settings.txt) file.
In this file you need to specify the profile of your browser where you already scan the QR whit your WhatsaApp account

<p align="center">
  <img width="450" height="300" src="http://dl1.cbsistatic.com/i/2017/04/26/6431e906-7aa6-4bc7-bcc2-2f6fc8ec6935/68ef88d0940c3ac784e54869b0bdf1bc/imgingest-8720007773569767113.png">
</p>

For example we are using the default Firefox profile so we open Firefox and go to https://web.whatsapp.com/ then we scan our QR to login then we can close Firefox and go to search for our profile file that we have in `/home/user/.mozilla/firefox/xxxxxxxx.default`, now that we localized our file we add the direction to our [settings.txt](settings.txt) file in the FIREFOX_PATH

## Browser Profile `CHROME_PATH`

For Chrome you can open Chrome browser, in the navigation bar you can go to `chrome://version/` and copy the **Profile path** to set it in the [settings.txt](settings.txt) file in the BROWSER_PATH
