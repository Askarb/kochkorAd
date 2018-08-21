from time import time

import telepot
# from InstagramAPI import InstagramAPI
from django.conf import settings
from slugify import slugify, CYRILLIC


def send_notification_to_telegram(request, form):
    if not request.user.is_authenticated:
        telegram_bot = telepot.Bot(settings.TELEGRAM_TOKEN)
        telegram_bot.sendMessage(chat_id='@kochkor',
                                text='Title - {0}\r\nText - {1}'.
                                format(form.title,
                                       form.text)
                                )


def generate_slug(title):
    if not title:
        title = 'jarnama'
    return slugify((title + '-' + str(int(round(time()*1000)))), pretranslate=CYRILLIC)


# def upload_photo(photo_path, caption=''):
#     api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
#     api.login()  # login
#     api.uploadPhoto(photo_path, caption=caption)
#
#
# def upload_album(photo_path_list, caption=''):
#     media = [  # Albums can contain between 2 and 10 photos/videos.
#         {
#             'type': 'photo',
#             'file': '/home/askar/Desktop/painstall/gallery_files/gallery1.jpg',  # Path to the photo file.
#             # 'usertags': [
#             #     {  # Optional, lets you tag one or more users in a PHOTO.
#             #         'position': [0.5, 0.5],
#             #         WARNING: THE USER ID MUST BE VALID. INSTAGRAM WILL VERIFY IT
#             #         AND IF IT'S WRONG THEY WILL SAY "media configure error".
#                     # 'user_id': '123456789',  # Must be a numerical UserPK ID.
#                 # },
#             # ]
#         },
#         {
#             'type': 'photo',
#             'file': '/home/askar/Desktop/painstall/gallery_files/gallery2.jpg',  # Path to the photo file.
#         },
#         # {
#         #    'type'     : 'video',
#         #    'file'     : '/path/to/your/video.mp4', # Path to the video file.
#         #    'thumbnail': '/path/to/your/thumbnail.jpg'
#         # }
#     ]
#     captionText = 'caption 3'  # Caption to use for the album.
#     ig = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
#     ig.login()
#     ig.uploadAlbum(media, caption=captionText)
