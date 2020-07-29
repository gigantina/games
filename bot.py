import requests, random
from bs4 import BeautifulSoup as bs
import telebot
from telebot import types

bot = telebot.TeleBot('1265229254:AAHJGt7bhCTc3SEN1_9LqvGtEVwIAeIFiy4')


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.from_user.id,
                     'Привет! Я ищу игры по категориям или могу прислать подборку игр разных жанров', reply_markup=menu())

def menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Аркады', 'RPG', 'Гонки', 'Драки', 'Квесты', 'Логические', 'Приключения', 'Симуляторы', 'Спорт', 'Стратегии',
       'Хоррор', 'Далее ->']])
    return keyboard

def next():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Назад <-', 'Шутер', 'Экшн', 'Подборка']])
    return keyboard


global cat, pages_cat
cat = ['Аркады', 'RPG', 'Гонки', 'Драки', 'Квесты', 'Логические', 'Приключения', 'Симуляторы', 'Спорт', 'Стратегии',
       'Хоррор', 'Шутер', 'Экшн']
pages_cat = ['arcade', 'rpg', 'racing', 'fight', 'quest', 'logic', 'adventure', 'simulator', 'sport', 'strategy',
             'horror', 'shooter', 'action']


@bot.message_handler(content_types=['text'])
def send_text(message):
    id = message.from_user.id
    if message.text in cat:
        category = cat.index(message.text)
        p = parse_cat(category)
        res = ''
        for i in p:
            res += f'{i[0]} - {i[1]}\n'
        bot.send_message(id, res)
    elif message.text == 'Подборка':
        p = parse_top()
        res = ''
        for i in p:
            res += f'{i[0]} - {i[1]}\n'
        bot.send_message(id, res)
    elif message.text == 'Далее ->':
        bot.send_message(id, 'Ok', reply_markup=next())
    elif message.text == 'Назад <-':
        bot.send_message(id, 'Ok', reply_markup=menu())


def parse_cat(category, n=5):
    r = requests.get(f'https://thelastgame.ru/category/{pages_cat[category - 1]}')
    html = bs(r.content, 'html.parser')
    max_page = int(str(html.select('a.last')[0]).split('/')[6])
    page = random.randint(1, max_page - 1)
    r = requests.get(f'https://thelastgame.ru/category/{pages_cat[category - 1]}/page/{page}')
    html = bs(r.content, 'html.parser')
    games = html.select('.post-thumbnail')
    res = []
    for i in range(n):
        el = str(games[i]).split('<')[2]
        title = el[el.find('title="') + 7:-3]
        link = el[el.find('href="') + 6:el.rfind('/') + 1]
        res.append((title, link))
    return res


def parse_top():
    res = []
    for i in range(13):
        res.append(parse_cat(i, 1)[0])
    return res

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)