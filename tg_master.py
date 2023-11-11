import telebot


bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message_):
    chat_id = message_.chat.id
    bot.reply_to(message_, f"Your chat ID is: {chat_id}")


def message(photo, name, id_, new_price, search_price, link):
    bot.send_photo(-1002049731505, f'{photo}',
                   f'{name}, \n id: {id_} \n'
                   f'===========================\n'
                   f' Цена - {new_price} руб.\n '
                   f'===========================\n'
                   f'Алгоритмом найдена \nминимальная рыночная цена: {str(search_price)} руб. \n{link}'
                   f'\n===========================\n'
                   f'Ссылка на карточку: \nhttps://www.wildberries.ru/catalog/{id_}/detail.aspx'
                   )


def monitoring_massage(photo, link, id_, name, price_curr, price_last, search_price):
    bot.send_photo(-1002049731505, f'{photo}', f'===================================\n'
                                f'{name} изменился в цене. \n Id : {id_}\n Был {price_last} руб., '
                                f'стал {price_curr} руб.\n В Яндекс найден похожий товар: \n{link}\n '
                                f'его цена - {search_price} руб.\n https://www.wildberries.ru/catalog/{id_}/detail.aspx'
                                f'\n===================================')


def error_message(text):
    bot.send_message(674796107, f'Итерация была прервана из-за ошибки: {text}')


bot.send_message(674796107, 'бот запущен!')


# bot.infinity_polling()
