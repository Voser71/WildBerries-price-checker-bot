# import requests
import telebot
import re
from bs4 import BeautifulSoup as bs
from telebot import types
from pathlib import Path
import os.path
from time import sleep as pause
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
command = ["python3", "Bot.py"]
bot = telebot.TeleBot('6609874140:AAGmMLtp0KQMAJjzyWbLxqoxEv_5ksBRqrI')
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5 37.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
@bot.message_handler(commands=['start']) #стартовая команда#
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📌Добавить товар")
    markup.add(btn1,)
    bot.send_message(message.from_user.id, "Выберите, что вам нужно", reply_markup=markup)
@bot.message_handler(func=lambda message: True)
def get_text_messages(message):

    if message.text == "📌Добавить товар" or message.text == "📌Добавить":
        bot.send_message(message.from_user.id, "Пришли URL товара в Wildberries")
        global chat_id
        chat_id = message.chat.id
        bot.register_next_step_handler(message, URL_reader)
    elif message.text == "Пришли URL ➕":
        f = open(f'files/{message.chat.id}/URL/URL.txt','r')
        URL = f.readline()
        f.close()
        bot.send_message(message.from_user.id, URL)
        print(URL)
    elif message.text == 'Цена💲':
        f = open(f'files/{message.chat.id}/URL/URL.txt', 'r')
        URL = f.readline()
        f.close()
        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        pause(randint(4, 8))
        soup = bs(driver.page_source, 'lxml')
        p1 = soup.find('ins', class_='price-block__final-price').get_text(strip=True)
        price = int(re.sub("[^0-9]", "", p1))
        print(price)
        f = open(f'files/{message.chat.id}/URL/price.txt', 'r+')
        old_price = int(f.readline())
        f.close()
        if price < old_price:
            difference = old_price - price
            bot.send_message(message.from_user.id, f"Цена на товар упала на {difference}, сейчас цена равна {price}")
            f = open(f'files/{message.chat.id}/URL/price.txt', 'w+')
            f.write(str(price))
            f.close()
        elif price > old_price:
            bot.send_message(message.from_user.id, f"Цена выросла. Нынешняя цена: {price}")
            f = open(f'files/{message.chat.id}/URL/price.txt', 'w+')
            f.write(str(price))
            f.close()
        else:
            bot.send_message(message.from_user.id, f"Цена равна {price} ₽")
def URL_reader(message):
    x = re.search(r'^https:', message.text)
    if x!=None:
        Path(f'files/{message.chat.id}/URL').mkdir(parents=True, exist_ok=True)
        URL = message.text
        # URL = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton("📌Добавить")
        btn2 = types.KeyboardButton('Пришли URL ➕')
        btn3 = types.KeyboardButton('Цена💲')
        markup.add(btn1,btn2,btn3)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)
        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        # driver.get(URL)
        pause(randint(7, 11))
        soup = bs(driver.page_source, 'lxml')
        p = soup.find('ins', class_='price-block__final-price').get_text(strip=True)
        price = re.sub("[^0-9]","" , p)
        f = open(f'files/{message.chat.id}/URL/price.txt','w')
        f.write(price)
        f.close()
        f = open(f'files/{message.chat.id}/URL/URL.txt','w')
        f.write(message.text)
        f.close()
bot.polling(none_stop=True, interval=0)
