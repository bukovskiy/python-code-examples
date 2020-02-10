import telebot
import time
from telebot import types
from src import keys
from src import config
from src.parser import Parser
import requests
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
BOT_KEY = keys.TG_API_TOKEN
bot = telebot.TeleBot(BOT_KEY)
parser = Parser("kinopoisk")  # Default parser is Kinopoisk
user_parsers = {}  # to remember which user uses wich parser.
# Я понимаю, что доставать такую инфу каждый раз из глобальное переменной -
# не самое элегантное решение, но немного не хватило времени, чтобы разобраться,
# как хранить пользовательскую информацию в рамках одной сессии бота.
# Представленное решение работает


@bot.message_handler(commands=["start"])
def start(message):
    """
    Reacts to start message with START_MSG from config
    Also, greets the user by his or her first name
    """
    bot.send_message(message.chat.id, "Привет, {}!".format(message.chat.first_name))
    bot.send_message(message.chat.id, config.START_MSG)


@bot.message_handler(commands=["kinopoisk"])
def kinopoisk(message):
    """
    Switch parser search source to Kinopoisk
    """
    global user_parsers
    # parser = Parser("kinopoisk") # Switch parser to Kinopoisk
    user_parsers[message.chat.id] = "kinopoisk"
    bot.send_message(message.chat.id, "Отлично! Поищем на Кинопоиске!")


@bot.message_handler(commands=["imdb"])
def imdb(message):
    """
    Switch parser search source to IMDB
    """
    global user_parsers
    # parser = Parser("kinopoisk") # Switch parser to Kinopoisk
    user_parsers[message.chat.id] = "imdb"
    bot.send_message(message.chat.id, "Great! Let's search on IMDB!")


@bot.message_handler(commands=["help"])
def help(message):
    """
    Sends HELP_MSG!
    """
    bot.send_message(message.chat.id, config.HELP_MSG)


@bot.message_handler(regexp=r"\/id\d+")
def full_view(message):
    """
    Recognises string that starts with '/id' and call parser to search for
    full output and poster
    Sends these back
    :param message: idXXXXXX (id of the film (string)
    """
    keyboard = types.InlineKeyboardMarkup()
    watch_button = types.InlineKeyboardButton(text="Посмотреть", callback_data="watch")
    keyboard.add(watch_button)
    id = message.chat.id
    if user_parsers.get(id) is not None:
        parser.set_type(user_parsers.get(id))
    parser.parse_id(int(message.json['text'][3:]))
    response, photo_url = parser.output, parser.photo
    if photo_url is not None:
        photo = requests.get(photo_url)
        bot.send_photo(message.chat.id, photo.content)
        bot.send_message(message.chat.id, "[​​​​​​​​​​​]{}".format(response),
                         parse_mode='markdown', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, response, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """
    Reacts to the user's action in the previous message.
    Shows links to watch the movies instead of the full description message
    :param call: call_back data from one of the previous messages
    """
    if call.message:
        if call.data == "watch":
            okko = types.InlineKeyboardButton(text="OKKO", url=config.LINK_OKKO + parser.title)
            ivi = types.InlineKeyboardButton(text="IVI", url=config.LINK_IVI + parser.title)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(ivi, okko)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=config.WATCH_MSG, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def msg(message):
    """
    Calls parser to search for a brief list of movies that match the message text
    Sends the results back to the user
    :param message: user's message text

    """
    global user_parsers
    id = message.chat.id
    if user_parsers.get(id) is not None:
        parser.set_type(user_parsers.get(id))
    response = parser.parse_query(message.json['text'])

    # I spy on you! Behave!
    logger.debug('{} just searched for {}'.format(id, message.json['text']))
    bot.send_message(message.chat.id, response)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=False)
        except Exception as e:
            logger.error(e)
            bot.stop_polling()
            time.sleep(15)
