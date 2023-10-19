import g4f
import telebot

from wb_master import get_category, get_product
from sql_master import check_id, save_price_wb_table, load_row_for_id, qwery_in_sql, save_in_wb_table, save_in_search_table
from yandex_master import scrapper, url_master
# from tg_master import message


def gpt_helper(text_):
    response_ = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{text_} Переработай этот текст таким образом, чтобы осталось только"
                                              f" название товара."}],
    )

    return response_


def compare(price_wb, price_search, percent=20):
    difference = (price_search - price_wb) / price_search * 100
    if difference > percent:
        check_difference = True
    else:
        check_difference = False

    return check_difference


def check_and_sand_message(brand, search_product_name, id_, search_price, price):
    full_property = brand + get_product(id_)
    if 'Модель не указана' in full_property:
        save_in_wb_table(id_, full_property, price)
    else:
        if '(gpt)' in search_product_name:
            name_in_search = search_product_name
        else:
            name_in_search = '(gpt)' + gpt_helper(search_product_name)
            save_in_search_table(id_, name_in_search, search_price)

        message(name=full_property, id_=id_, new_price=price, search_price=search_price,
            name_in_search=name_in_search)


def main(url):
    category_list = get_category(url)

    for product in category_list:
        name, price, id_ = (product['Наименование'] + ' ' + product['Бренд']), product['Цена со скидкой'],\
            product['Артикул, id']
        
        if check_id(id_, 'wb_table'):
            if 'Модель не указана' in load_row_for_id(id_, 'wb_table')[1]:
                continue
            save_price_wb_table(price, id_)
            product_from_search = load_row_for_id(id_, 'search_table')

            if product_from_search:
                if product_from_search[2]:
                    check_difference = compare(price, product_from_search[2])
                    if check_difference:
                        check_and_sand_message(brand=product['Бренд'], search_product_name=product_from_search[1],
                                               id_=id_, search_price=product_from_search[2], price=price)
                        continue
                else:
                    continue
            else:
                qwery = qwery_in_sql(id_)
                url = url_master(qwery)
                yandex_product = scrapper(url)

                if yandex_product:
                    name, search_price = yandex_product['desc'], int(yandex_product['price'])
                    save_in_search_table(id_, name, int(yandex_product['price']))
                    if search_price:
                        check_difference = compare(price, search_price)
                        if check_difference:
                            check_and_sand_message(brand=product['Бренд'], search_product_name=yandex_product['desc'],
                                                   id_=id_, search_price=int(yandex_product['price']), price=price)
                    else:
                        continue
                else:
                    save_in_search_table(id_, name, 0)
                    continue
        else:
            save_in_wb_table(id_, name, price)

            qwery = qwery_in_sql(id_)
            url = url_master(qwery)
            yandex_product = scrapper(url)

            if yandex_product:
                search_product_name, search_price = yandex_product['desc'], int(yandex_product['price'])
                save_in_search_table(id_, search_product_name, int(yandex_product['price']))
                check_difference = compare(price, search_price)
                if check_difference:
                    check_and_sand_message(brand=product['Бренд'], search_product_name=yandex_product['desc'],
                                           id_=id_, search_price=int(yandex_product['price']), price=price)
            else:
                save_in_search_table(id_, name, 0)
                continue


url_list = [
    ('interskol', 'https://catalog.wb.ru/brands/%D0%B8/catalog?appType=1&brand=9084&curr=rub&dest=-1257786&regions=80,'
                 '38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&uclusters=0headers='
                 'headers&page='),
    ('zubr_1', 'https://catalog.wb.ru/brands/%D0%B7/catalog?appType=1&brand=54220&curr=rub&dest=-1257786&fsupplier=67861'
              ';218978&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=rate&sort=rate&spp=0'
              '&subject=2221;2224&page='),
    ('zubr_2', 'https://catalog.wb.ru/brands/%D0%B7/catalog?appType=1&brand=54220&curr=rub&dest=-1257786&fsupplier=67861'
              ';218978&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&sort=rate&'
              'spp=0&subject=1569;3748;2540;770;1164;4998;926;4080;2441;2297;3717;1165;1166;1169;2070;4084;2668;2995;'
              '2183;1318;2194;4160;3968;2550;986;2341;1362;1168;1337;2197;1170;1171&page='),
    ('sturm', 'https://catalog.wb.ru/brands/s/catalog?appType=1&brand=36933&curr=rub&dest=-1257786&regions=80,38,83,4,'
             '64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page='),
    ('resanta', 'https://catalog.wb.ru/brands/%D1%80/catalog?appType=1&brand=15488&curr=rub&dest=-1257786&regions='
               '80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page'),
    ('denzel', 'https://catalog.wb.ru/brands/d/catalog?appType=1&brand=46232&curr=rub&dest=-1257786&regions='
              '80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page=')
]

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')
# bot.send_message(674796107, "Бот запущен!")


def message(name, id_, new_price, search_price, name_in_search):
    bot.send_message(674796107, f'Товар: {name}, \n id: {id_} \n упал в цене. \n В Яндекс найден похожий товар: \n'
                                f' {name_in_search} \n его цена - {search_price} рублей \n '
                                f'разница {(search_price - new_price) / new_price * 100}%')


if __name__ == '__main__':
    # for url in url_list:
    #     print(url[0])
    #     main(url[1])
    main('https://catalog.wb.ru/brands/d/catalog?appType=1&brand=46232&curr=rub&dest=-1257786&regions='
              '80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page=')

