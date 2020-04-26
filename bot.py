# coding=utf-8
import config
import os
import telebot
from flask import Flask, request
from telebot import types


bot = telebot.TeleBot(config.TOKEN)


"""KEYBOARDS"""
starting_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
starting_keyboard.add(types.KeyboardButton(text='Да'))
starting_keyboard.add(types.KeyboardButton(text='Нет'))
starting_keyboard.add(types.KeyboardButton(text='...'))

timetable_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
timetable_keyboard.add(types.KeyboardButton(text='Сегодня'))
timetable_keyboard.add(types.KeyboardButton(text='Завтра'))
timetable_keyboard.add(types.KeyboardButton(text='Текущая неделя'))
timetable_keyboard.add(types.KeyboardButton(text='Следующая неделя'))
timetable_keyboard.add(types.KeyboardButton(text='Назад'))


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, 'Салам алейкум ! Вы Анзор ?', reply_markup=starting_keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, "Ищу расписание...", parse_mode='markdown')
        bot.send_photo(message.chat.id, photo=open('media/sueta.jpg', 'rb'))
        bot.send_message(message.chat.id, 'Чё хочешь уцы', reply_markup=timetable_keyboard)
        #bot.register_next_step_handler(message, process_message)
    elif message.text.lower() == 'нет':
        bot.send_photo(message.chat.id, photo=open('media/bruh.jpg', 'rb'))
        bot.send_message(message.chat.id, "Че ты здесь забыл тогда ТШОРТ !?")
    elif message.text.lower() == '...':
        #bot.send_audio(message.chat.id, audio=open('media/ya.mp3', 'rb'))
        bot.send_message(message.chat.id, "Да кто такой это ваше многоточие...")



    elif message.text.lower() == 'сегодня':
        bot.send_message(message.chat.id, "А хер его !")
    elif message.text.lower() == 'завтра':
        bot.send_message(message.chat.id, "Без понятия...")
    elif message.text.lower() == 'текущая неделя':
        bot.send_message(message.chat.id, "Ты идиот ?")
    elif message.text.lower() == 'следующая неделя':
        bot.send_message(message.chat.id, "Безумно можно быть пееервыыымм...")
    elif message.text.lower() == 'назад':
        bot.send_message(message.chat.id, "Отправляю назад !")
        bot.send_message(message.chat.id, 'Анзор ?', reply_markup=starting_keyboard)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def process_message(message):
    pass




if "HEROKU" in list(os.environ.keys()):
    server = Flask(__name__)

    @server.route('/' + config.TOKEN, methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=config.HEROKU_URL + config.TOKEN)
        return "!", 200

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
