from en_videos import get_channel_stats, get_videos_ids, \
    get_videos_details, get_comments, get_user_channel_stats
from googleapiclient.discovery import build
import pprint


api_key = ["AIzaSyAas7rC594WDvAwKaXpFgaTCv_-mbTJAUo",
           "AIzaSyCtzFyZRlwHUO6uiJlKeYEgH7ZSrJVZcPg"]
channel_ids = ["UCWDksMO8R0Mew4B89GhO9dA",
               "UCoSrY_IQQVpmIRZ9Xf-y93g",
               "UC3n5uGu18FoCy23ggWWp8tA",
               "UC5CwaMl1eIgY8h02uZw7u8A",
               "UCI7ktPB6toqucpkkCiolwLg",
               "UCaBTm46K3l59CIty88Q_jog",
               "UC1DCedRgGHBdm81E1llLhOQ",
               "UCgTOIiEgjm58xLjHvDjmgdA",
               "UCmDfpsIMjCw9bMrwa8dIsTw"
               ]
user_channel_ids = ["MissaSinfonia"]

youtube = build("youtube", "v3", developerKey=api_key[1])

#  main()
all_data = get_channel_stats(youtube, channel_ids)
all_user_data = get_user_channel_stats(youtube, user_channel_ids)
videos = []
videos_details = []
comentarios = []
for i in range(len(all_data)):
    pprint.pprint(all_data[i])
    videos = get_videos_ids(youtube, all_data[i]["playlist_id"])
    videos_details = get_videos_details(youtube, videos)
    #  pprint.pprint(videos_details)
    for j in range(len(videos)):
        #  print(f"Video {j}")
        comentarios.append(get_comments(youtube, videos[j]))
        #  pprint.pprint(comentarios[j])
    #  all_data[i], videos_details[i], comentarios[i]
    print("\n\n\n----")
#  para este punto ya deberían haberse guardado la info de los de arriba
videos = []
videos_details = []
comentarios = []
for i in range(len(all_user_data)):
    pprint.pprint(all_user_data[i])
    videos = get_videos_ids(youtube, all_user_data[i]["playlist_id"])
    videos_details = get_videos_details(youtube, videos)
    #  pprint.pprint(videos_details)
    for j in range(len(videos)):
        #  print(f"Video {j}")
        comentarios.append(get_comments(youtube, videos[j]))
        #  pprint.pprint(comentarios[j])
    print("\n\n\n----")
#  aquí arriba ando imprimiendo el diccionario de datos
