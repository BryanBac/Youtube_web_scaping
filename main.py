from en_videos import get_channel_stats, get_videos_ids, \
    get_videos_details, get_comments, get_user_channel_stats
from googleapiclient.discovery import build
import pprint


urls = [
    "UC3n5uGu18FoCy23ggWWp8tA"
]


api_key = "AIzaSyAas7rC594WDvAwKaXpFgaTCv_-mbTJAUo"
channel_ids = ["UCoSrY_IQQVpmIRZ9Xf-y93g",
               "UC3n5uGu18FoCy23ggWWp8tA"
               ]
user_channel_ids = ["MissaSinfonia"]

youtube = build("youtube", "v3", developerKey=api_key)

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
    pprint.pprint(videos_details)
    for j in range(len(videos)):
        print(f"Video {j}")
        comentarios.append(get_comments(youtube, videos[j]))
        pprint.pprint(comentarios[j])
    print("\n\n\n----")
#  para este punto ya deberían haberse guardado la info de los de arriba
videos = []
videos_details = []
comentarios = []
for i in range(len(all_user_data)):
    pprint.pprint(all_user_data[i])
    videos = get_videos_ids(youtube, all_user_data[i]["playlist_id"])
    videos_details = get_videos_details(youtube, videos)
    pprint.pprint(videos_details)
    for j in range(len(videos)):
        print(f"Video {j}")
        comentarios.append(get_comments(youtube, videos[j]))
        pprint.pprint(comentarios[j])
    print("\n\n\n----")
#  aquí arriba ando imprimiendo el diccionario de datos
