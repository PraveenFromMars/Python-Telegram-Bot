from telegram.ext import *
from telegram import *
import os
from os.path import *
import requests
import shutil
from apiclient.discovery import build
import string

key = "$YOUR_API_KEY"

resource = build("customsearch", 'v1', developerKey=key).cse()


key = "$YOUR_API_KEY"

bot = Bot("$YOUR_API_KEY")

# print("bot has started")
updater = Updater("$YOUR_API_KEY", use_context=True)

dispatcher = updater.dispatcher

def reply(update:Update, context:CallbackContext):
    bot.send_message(chat_id=update.effective_chat.id, text="hello bro how are you")

def start(update:Update, context:CallbackContext):
    bot.send_message(chat_id=update.effective_chat.id,
        text = "Helle there, Welcome to the Image Bot. Here you can get every images with simple query. For more information fire /help"
        )
def Help(update:Update, context:CallbackContext):
    bot.send_message(chat_id=update.effective_chat.id,
        text="Hello (From search asssitant), There are 2 parameters that you can use to get the best image as possible\ncount : Number of images that you want to get 1 - 10\nsite : specific site name to get image \nIMPORTANT: All tags should be described after the search query. Example 'Dog count:3 site:pixelbay,unplash'"
        )
def reply(update, contet):
    text = str(update.message.text).lower()
    countnum = ""
    site = []
    sites = ""
    query = text.split();
    querys = ""
    if int(text.find("count")) != -1:
        contentintext = text.split()
        for i in contentintext:
            if int(i.find("count")) != -1:
                query.remove(i)
                contentsini = i.split(":")
                for j in contentsini:
                    if j != "count":
                        countnum = int(j);
        if countnum > 10:
            bot.send_message(chat_id=update.effective_chat.id, text="Count limit overflowed")
            return 
    if int(text.find("site")) != -1:
        contentintext = text.split()
        for i in contentintext:
            if int(i.find("site")) != -1:
                query.remove(i)
                contentsini = i.split(":")
                for j in contentsini:
                    if j == "site":
                        contentsini.remove(j)
                site = contentsini[0].split(",")
                for k in site:
                    if sites == "":
                        sites = sites + k
                    else:
                        sites = sites + ',' + k
    
    for j in query:
        querys = querys + ' ' + j
    if int(text.find("site")) != -1:
        querys = querys + ' ' + "inurl:" + sites;
    result = resource.list(q=querys, cx="4d2a535d6bf66b50a", searchType='image').execute()
    image = "hello"
    typeOfImage = "type"
    for item in result['items']:
        if int(text.find("count")) != -1:
            countnum = countnum - 1;
        image = item['link']
        typeOfImage = image.split()
        bot.send_photo(chat_id=update.effective_chat.id, photo=image)
        if int(text.find("count")) == -1:
            break
        else:
            if countnum == 0:
                break
        
def error(update, context):
   logger.warning("Some internal error occured!!, please try a new key word")
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', Help))
dispatcher.add_handler(MessageHandler(Filters.text, reply))
# print("Bot has started!!")

dispatcher.add_error_handler(error)


updater.start_polling()
