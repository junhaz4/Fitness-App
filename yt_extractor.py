import youtube_dl
from youtube_dl.utils import DownloadError

yt = youtube_dl.YoutubeDL()

def get_info(url):
    """
    :param url:
    :return:
    """
    with yt:
        try: # get info from url
            result = yt.extract_info(url, download=False)
        except DownloadError:
            return None
    # this means the url contains a playlist
    if "entries" in result:
        video = result["entries"][0]
    else:
        video = result

    infos = ['id', 'title', 'channel', 'view_count', 'like_count',
             'channel_id', 'duration', 'categories', 'tags']
    def rename_key(key):
        if key == 'id':
            return 'video_id'
        return key

    return {rename_key(key): video[key] for key in infos}