import telebot

from sql_master import save_in_suitable_products_table


bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message_):
    chat_id = message_.chat.id
    bot.reply_to(message_, f"Your chat ID is: {chat_id}")


def message(dirty_name, name, id_, new_price, search_price, name_in_search):
    new_price, search_price = int(new_price), int(search_price)
    bot.send_message(674796107, f'Товар: {dirty_name} {name}, \n id: {id_} стоимостью - {new_price} руб. упал в цене.\n'
                             f'https://www.wildberries.ru/catalog/{id_}/detail.aspx'
                             f'\n В Яндекс найден похожий товар: \n'
                             f' {name_in_search} \n его цена - {search_price} руб. \n '
                             f'разница {(search_price - new_price) / new_price * 100}%')
    save_in_suitable_products_table(id_, name, new_price, search_price)


def monitoring_massage(id_, name, price_curr, price_last, search_price, name_in_search):
    bot.send_message(674796107, f'===================================\n'
                                f' Товар {name} изменился в цене. \n Id товара : {id_}\n Был {price_last}, '
                                f'стал {price_curr}.\n В Яндекс найден похожий товар: \n {name_in_search} \n '
                                f'его цена - {search_price} руб.\n https://www.wildberries.ru/catalog/{id_}/detail.aspx'
                                f'\n===================================')


def error_message(text):
    bot.send_message(674796107, f'Итерация была прервана из-за ошибки: {text}')


bot.send_message(674796107, 'бот запущен!')


# bot.infinity_polling()
