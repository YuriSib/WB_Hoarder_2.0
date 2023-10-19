import telebot
import os
import time


bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message_):
    chat_id = message_.chat.id
    bot.reply_to(message_, f"Your chat ID is: {chat_id}")


bot.send_message(674796107, "Бот запущен!")


def message(name, id_, new_price, search_price, name_in_search):
    bot.send_message(674796107, f'Товар: {name}, \n id: {id_} \n '
                                f'https://www.wildberries.ru/catalog/{id_}/detail.aspx'
                                f'упал в цене. \n В Яндекс найден похожий товар: \n'
                                f' {name_in_search} \n его цена - {search_price} рублей \n '
                                f'разница {(search_price - new_price) / new_price * 100}%')


bot.infinity_polling()
