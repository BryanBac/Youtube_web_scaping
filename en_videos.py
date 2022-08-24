#  Función para estadisticas
def get_channel_stats(youtube, channel_ids):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids)
    )
    all_data = []
    response = request.execute()
    for i in range(len(response["items"])):
        data = dict(Channel_name=response["items"][i]["snippet"]["title"],
                    Subscribers=response["items"][i]["statistics"]["subscriberCount"],
                    Views=response["items"][i]["statistics"]["viewCount"],
                    Total_videos=response["items"][i]["statistics"]["videoCount"],
                    playlist_id=response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"]
                    )
        all_data.append(data)
    return all_data


def get_videos_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    netx_page_token = response.get("nextPageToken")
    more_pages = True
    videos_ides = []
    for i in range(len(response["items"])):
        videos_ides.append(response["items"][i]["contentDetails"]["videoId"])
    while more_pages:
        if netx_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=netx_page_token
            )
            response = request.execute()
            for i in range(len(response["items"])):
                videos_ides.append(response["items"][i]["contentDetails"]["videoId"])
            netx_page_token = response.get("nextPageToken")
    return videos_ides


def get_videos_details(youtube, video_ids):
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(video_ids[i:i+50]))
        response = request.execute()
        for video in response["items"]:
            video_stats = dict(
                Title=video["snippet"]["title"],
                Published_date=video["snippet"]["publishedAt"],
                Views=video["statistics"]["viewCount"],
                Likes=video["statistics"]["likeCount"],
                Total_fav=video["statistics"]["favoriteCount"],
                Duracion=video["contentDetails"]["duration"]
                #  Total_comentarios=video["statistics"]["commentCount"]
            )
            all_video_stats.append(video_stats)
    return all_video_stats


# Aquí va a ser para los comentarios
def get_comments(youtube, video_ids):
    all_comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_ids
    )
    try:
        response = request.execute()
        for comment in response["items"]:
            comment_detail = dict(
                autor=comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                likes=comment["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                texto=comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            )
            all_comments.append(comment_detail)
    except:
        print("El video tenía los comentarios deshabilitados")
    return all_comments
