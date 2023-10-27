import time

from wb_master import get_category, get_product
from sql_master import check_id, save_price_wb_table, load_row_for_id, save_in_wb_table, \
    save_in_search_table, save_price_suitable_products_table, load_rows_from_suitable_products_table
from yandex_master import scrapper, url_master
from tg_master import message, error_message, monitoring_massage
from model_extracting import get_model


def compare(price_wb, price_search, percent=20):
    price_wb, price_search = float(price_wb), float(price_search)
    difference = (price_search - price_wb) / price_search * 100
    if difference > percent and price_search > 4000:
        check_difference = True
    else:
        check_difference = False

    return check_difference


def product_monitoring():
    product_list = load_rows_from_suitable_products_table()
    for product in product_list:
        id_, name, price_curr, price_last, search_price = product[0], product[1], product[2], product[3], product[4]
        current_price = load_row_for_id(id_, 'wb_table')[2]
        if price_curr != price_last:
            monitoring_massage(id_, name, current_price, price_last, search_price)
        save_price_suitable_products_table(current_price, price_curr, id_)


def main(url):
    category_list = get_category(url)

    error_counter = 0

    for product in category_list:
        # try:
            name, brand = product['Наименование'], product['Бренд'],
            price, id_ = product['Цена со скидкой'], product['Артикул, id']

            if check_id(id_, 'wb_table'):
                wb_name = load_row_for_id(id_, 'wb_table')[1]
                if 'Неизвестная модель' in load_row_for_id(id_, 'wb_table')[1]:
                    continue
                else:
                    save_price_wb_table(price, id_)
                    product_from_search = load_row_for_id(id_, 'search_table')

                    search_name, search_price = load_row_for_id(id_, 'wb_table')[1], load_row_for_id(id_, 'wb_table')[2]

                    check_difference_and_price = compare(price, product_from_search[2])
                    if check_difference_and_price:
                        message(name=wb_name, id_=id_, new_price=price,
                                search_price=search_price, name_in_search=search_name)
                        continue
            else:
                dirty_desk_name = get_product(id_)
                desk_name = get_model(dirty_desk_name, brand, name) if dirty_desk_name else get_model(name, brand, '')
                save_in_wb_table(id_, brand + ' ' + desk_name, price)

                if 'Неизвестная модель' in desk_name:
                    save_in_search_table(id_, 'Не найдено!', 1)
                    continue

                url = url_master(brand + ' ' + desk_name)
                yandex_product = scrapper(url)

                if yandex_product:
                    search_name = get_model(yandex_product['desc'], brand, '')
                    search_price = int(yandex_product['price'])
                    save_in_search_table(id_, brand + ' ' + search_name, search_price)
                    check_difference_and_price = compare(price, search_price)
                    if check_difference_and_price:
                        message(name=brand + ' ' + desk_name, id_=id_, new_price=price,
                                search_price=search_price, name_in_search=brand + ' ' + search_name)
                else:
                    save_in_search_table(id_, 'Не найдено!', 1)
                    continue
        # except Exception as e:
        #     error_message(e)
        #     error_counter += 1
        #     if error_counter >= 10:
        #         break


url_list = [
    ('denzel', 'https://catalog.wb.ru/brands/d/catalog?appType=1&brand=46232&curr=rub&dest=-1257786&regions='
                  '80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page='),
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
    # ('resanta', 'https://catalog.wb.ru/brands/%D1%80/catalog?appType=1&brand=15488&curr=rub&dest=-1257786&regions='
    #            '80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page'),
]

# bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')
# bot.send_message(674796107, "Бот запущен!")


if __name__ == '__main__':
    while True:
        for url in url_list:
            print(url[0])
            main(url[1])
        product_monitoring()
        print('Iteration is complete. Wait to new iteration for 5 min!')
        time.sleep(300)


