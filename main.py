from selenium import webdriver
from bs4 import BeautifulSoup
from en_videos import obtner


urls = [
    "UC3n5uGu18FoCy23ggWWp8tA"
]


def main():
    driver = webdriver.Chrome("chromedriver_win32\\chromedriver.exe")
    driver.get("https://www.youtube.com/channel/{}/videos".format(urls[0]))
    content = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(content, 'lxml')
    titles = soup.findAll("a", id="video-title")
    views = soup.findAll("span", class_="style-scope ytd-grid-video-renderer")
    suscripciones = soup.findAll("yt-formatted-string", id="subscriber-count")
    nombre_del_canal = soup.findAll("yt-formatted-string", class_="style-scope ytd-channel-name")
    i = 0
    for suscripcion in suscripciones:
        print(f"---{nombre_del_canal[0].text}---{suscripcion.text}---")
    for title in titles:
        link = "https://www.youtube.com" + title.get("href")
        #  links.append(link)
        print(title.text, "---", views[i].text, "---", link)
        i += 2


#  main()
obtner()
