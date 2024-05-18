import telebot
from telebot import types
import requests
from urllib.parse import urlparse
import os
import time

API_TOKEN = '7013868761:AAGpTTknQpl7UOhqfLhMqNHI9BwxxcZFY5s'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا، أنا بوت التحميل الخاص بك. أرسل لي رابط الفيلم لأبدأ التحميل.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith("http"):
        url = message.text
        file_name = os.path.basename(urlparse(url).path)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            bot.reply_to(message, "جاري التحميل... ⏳")
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            bot.send_document(message.chat.id, open(file_name, 'rb'))
            os.remove(file_name)
            bot.reply_to(message, "تم التحميل بنجاح! 🎉")
        else:
            bot.reply_to(message, "لم أتمكن من تحميل الفيلم. تأكد من صحة الرابط.")

bot.polling()
