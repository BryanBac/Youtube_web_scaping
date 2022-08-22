from selenium import webdriver
from bs4 import BeautifulSoup
import requests


urls = [
    "UC3n5uGu18FoCy23ggWWp8tA"
]
links = [
    "https://www.youtube.com/watch?v=DYed5whEf4g"
]


def main():
    driver = webdriver.Chrome("chromedriver_win32\\chromedriver.exe")
    driver.get("https://www.youtube.com/channel/{}/videos".format(urls[0]))
    content = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(content, 'lxml')
    titles = soup.findAll("a", id="video-title")
    for title in titles:
        link = "https://www.youtube.com" + title.get("href")
        links.append(link)
        print(title.text, "---", link)


def en_videos():
    print("me faltan los likes")


main()
en_videos()
