from time import time

import telepot
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
    return slugify((title + '-' + str(int(round(time()*1000)))), pretranslate=CYRILLIC)
