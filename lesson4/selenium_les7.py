from selenium import webdriver
from selenium.webdriver.common.keys import Keys


if __name__ == "__main__":
    browser = webdriver.Chrome()
    url = 'https://habr.com/'
    browser.get(url)
    print(1)