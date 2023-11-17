#!/usr/bin/env python3
from pyrogram import Client
from pyrogram import filters
import logging
import time
import os

file_name = "MsgLog" + time.strftime("%d%m%y") + ".log"
folder = "Logs/"
file_path = folder + file_name
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)

full_file_name = os.path.join(directory, file_name)
logger= logging.getLogger()
logger.setLevel(logging.INFO) # or whatever
handler = logging.FileHandler(file_path, 'a', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(name)s %(message)s', '%m/%d/%Y %I:%M:%S %p')) # or whatever
logger.addHandler(handler)

# logging.basicConfig(filename='file_path', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger.info("Forwarding Message")
# ~~~~~~ CONFIG ~~~~~~~~ #
ACCOUNT = "@YOUR_ID"
PHONE_NR = '+(CountryCode)(PhoneNumber)'

# https://my.telegram.org/auth?to=apps
API_ID = 0  # create api from https://my.telegram.org/auth?to=apps to enable this script
API_HASH = "123abc"  # get hash from created API

# CHAT ID
SOURCE_CHAT = -1  # Get the Chat ID of your Chat group using telegram web
TARGET_CHAT = -1  # Get the Chat ID of the Chat group that you want to forward the message to using telegram web

# SIGN OFF
SIGN = " °"  # message check to differentiate being sent by user or script
# ~~~~~~~~~~~~~~~~~~~~~~ #

app = Client(
    ACCOUNT,
    phone_number=PHONE_NR,
    api_id=API_ID,
    api_hash=API_HASH
)

# filters.chat(SOURCE_CHAT)
@app.on_message(filters.chat(SOURCE_CHAT))
def my_handler(client, message):
    reply = ""
    if message.reply_to_message:
        info = ""
        if message.reply_to_message.text:
            info = message.reply_to_message.text
        if message.reply_to_message.photo:
            info = "PHOTO"
        if message.reply_to_message.video:
            info = "VIDEO"
        if message.reply_to_message.caption:
            info += (": " + message.reply_to_message.caption)

        reply = "\n[Replying to \"{}\"]".format(info)

    if message.text:
        app.send_message(TARGET_CHAT, message.text + SIGN + str(len(message.text)) + reply)
        logger.info("[TEXT] {}".format(message))

    caption = ""
    if message.caption:
        caption = message.caption + SIGN + str(len(message.caption)) + reply

    if message.photo:
        imgFile = app.download_media(message.photo.file_id, in_memory=True)
        app.send_photo(TARGET_CHAT, imgFile, caption)
        logger.info("[PHOTO] {}".format(message))
    if message.video:
        vidFile = app.download_media(message.video.file_id, in_memory=True)
        app.send_video(TARGET_CHAT, vidFile, caption)
        logger.info("[VIDEO] {}".format(message))

app.run()