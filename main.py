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
        try:
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
                    if 'Неизвестная модель' in search_name:
                        continue
                    check_difference_and_price = compare(price, search_price)
                    if check_difference_and_price:
                        message(name=brand + ' ' + desk_name, id_=id_, new_price=price,
                                search_price=search_price, name_in_search=brand + ' ' + search_name)
                else:
                    save_in_search_table(id_, 'Не найдено!', 1)
                    continue
        except Exception as e:
            error_message(e)
            error_counter += 1
            if error_counter == 5:
                break


url_list = [
    ('zitrek', 'https://catalog.wb.ru/brands/z/catalog?TestGroup=control&TestID=311&appType=1&brand=38311&curr=rub&'
               'dest=-1257786&priceU=190000;15062000&sort=sale&spp=29&xsubject=926;927;1164;1165;1166;1168;1169;'
               '1171;1233;1234;1318;2197;2221;2223;2224;2297;2550;2995;3717;3748;3913;4017;4084;4160;4204;4757;4810;'
               '6127;6273;8099;8102;8103;8279;8280&page='),

    ('zubr_1', 'https://catalog.wb.ru/brands/%D0%B7/catalog?TestGroup=control&TestID=311&appType=1&brand=54220&curr='
               'rub&dest=-1257786&priceU=150000;12736000&sort=rate&spp=29&xsubject=330;468;710;770;926;927;1163;'
               '1164;1165;1166;1167;1168;1169;1170;1171;1233;1234;1318;1337;1569;2030;2057;2070;2107;2194;2197;2221;'
               '2223;2224;2297;2540;2541;2550;2569;2586;2668;2955;2995;3126;3161;3659;3748;3796;3863;4068;4084;4160;'
               '4209;4472;4473;4756;4757;4810;6125;6127;6156;6286;6947;8090;8099;8102;8103;8109;8279;8280&page='),

    ('denzel', 'https://catalog.wb.ru/brands/d/catalog?TestGroup=control&TestID=311&appType=1&brand=46232&curr=rub&'
               'dest=-1257786&priceU=190000;52349000&sort=popular&spp=29&xsubject=770;926;927;939;1164;1165;'
               '1166;1169;1171;1233;1318;1362;1537;1717;2030;2098;2197;2221;2222;2224;2297;2540;2541;2550;2668;3668;'
               '3748;3749;3863;3913;4081;4084;4085;4202;4204;4472;4473;4474;4756;5480;6125;6156;6193;6273;6286;6947;'
               '7148;7798;8102&page='),

    ('interskol', 'https://catalog.wb.ru/brands/%D0%B8/catalog?TestGroup=control&TestID=311&appType=1&brand=9084&curr='
                  'rub&dest=-1257786&priceU=190000;5790000&sort=popular&spp=29&xsubject=710;927;1164;1166;1167;'
                  '1168;1169;1171;1234;1318;1337;1362;2197;2221;2223;2224;2297;2541;2550;2668;2955;2995;3717;3748;8102;'
                  '8103;8279&page='),

    ('sturm', 'https://catalog.wb.ru/brands/s/catalog?TestGroup=control&TestID=311&appType=1&brand=36933&curr=rub&dest'
              '=-1257786&priceU=190000;8903600&sort=popular&spp=29&xsubject=710;926;927;939;1164;1165;1166;1167;'
              '1168;1169;1225;1233;1234;1318;1569;2030;2033;2057;2070;2197;2221;2222;2341;2540;2541;2550;2668;2718;'
              '2955;2995;3527;3548;3717;3748;3796;3863;3970;4068;4084;4160;4204;4472;4473;4474;4756;4810;6273;6947;'
              '8102;8103;8279;8280&page='),

    ('resanta', 'https://catalog.wb.ru/brands/s/catalog?TestGroup=control&TestID=311&appType=1&brand=36933&curr=rub'
                '&dest=-1257786&priceU=190000;8903600&sort=popular&spp=29&xsubject=710;926;927;939;1164;1165;'
                '1166;1167;1168;1169;1225;1233;1234;1318;1569;2030;2033;2057;2070;2197;2221;2222;2341;2540;2541;2550;'
                '2668;2718;2955;2995;3527;3548;3717;3748;3796;3863;3970;4068;4084;4160;4204;4472;4473;4474;4756;4810;'
                '6273;6947;8102;8103;8279;8280&page='),

    ('kalibr', 'https://catalog.wb.ru/brands/%D0%BA/catalog?TestGroup=control&TestID=311&appType=1&brand=48492&curr='
               'rub&dest=-1257786&priceU=190000;5120000&sort=popular&spp=29&xsubject=926;927;1164;1166;1167;'
               '1168;1169;1170;1171;1318;1362;2197;2221;2224;2297;2668;2995;3717;3748;3863;4068;4084;4160;4202;4204;'
               '4472;4473;4474;4756;4810;6125;6127;6273;6275;6947;8102;8103;8279&page=')
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


