from selenium import webdriver
from bs4 import BeautifulSoup
from en_videos import get_channel_stats, get_videos_ids, get_videos_details, get_comments
from googleapiclient.discovery import build
import pprint


urls = [
    "UC3n5uGu18FoCy23ggWWp8tA"
]


api_key = "AIzaSyAas7rC594WDvAwKaXpFgaTCv_-mbTJAUo"
channel_ids = ["UC3n5uGu18FoCy23ggWWp8tA",
               "UCoSrY_IQQVpmIRZ9Xf-y93g"
               ]

youtube = build("youtube", "v3", developerKey=api_key)


#  Ya no se usa el main
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
all_data = get_channel_stats(youtube, channel_ids)
videos = []
comentarios = []
for i in range(len(all_data)):
    pprint.pprint(all_data[i])
    videos = get_videos_ids(youtube, all_data[i]["playlist_id"])
    print(videos)
    #  print(get_videos_details(youtube, videos))  #  -- Para el json
    pprint.pprint(get_videos_details(youtube, videos))
    for j in range(len(videos)):
        print(f"Video {j}")
        comentarios.append(get_comments(youtube, videos[j]))
        pprint.pprint(comentarios[j])
    print("\n\n\n----")
#  aquí arriba ando imprimiendo el diccionario de datos
