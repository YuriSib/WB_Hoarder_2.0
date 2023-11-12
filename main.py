import time

from wb_master import get_category, get_product
from sql_master import check_id, save_price_wb_table, load_row_for_id, save_in_wb_table,save_in_search_table, \
    save_price_suitable_products_table, load_rows_from_suitable_products_table, save_in_suitable_products_table
from yandex_master import scrapper, url_master
from tg_master import message, error_message, monitoring_massage
from model_extracting import get_model
from url_master import category_url


def compare(price_wb, price_search, percent=35):
    price_wb, price_search = float(price_wb), float(price_search)
    difference = (price_search - price_wb) / price_search * 100
    if 100 > difference > percent and price_search > 4000:
        check_difference = True
    else:
        check_difference = False

    return check_difference


def product_monitoring():
    product_list = load_rows_from_suitable_products_table()
    for product in product_list:
        id_, name, price_curr, price_last, search_price = product[0], product[1], product[2], product[3], product[4]
        current_price, photo = load_row_for_id(id_, 'wb_table')[2], load_row_for_id(id_, 'wb_table')[3]
        name_in_search, link = load_row_for_id(id_, 'search_table')[1], load_row_for_id(id_, 'search_table')[3]
        if 'Не найдено!' not in name_in_search:
            if price_curr != price_last and price_last is not None:
                monitoring_massage(photo, link, id_, name, price_curr, price_last, search_price)
            if not price_last:
                message(photo=photo, name=name, id_=id_, new_price=current_price, search_price=search_price, link=link)
        save_price_suitable_products_table(current_price, price_curr, id_)


def main(url, category):
    category_list = get_category(url)

    for product in category_list:
        try:
            name, brand = product['Наименование'], product['Бренд'],
            price, id_ = product['Цена со скидкой'], product['Артикул, id']

            if 'akita' in brand or 'AKITA' in brand or 'osch' in brand or 'OSCH' in brand or 'ewalt' in brand or \
                'EWALT' in brand or 'eWalt' in brand or 'eWalt' in brand or 'бош' in brand or 'БОШ' in brand or \
                    'Бош' in brand or 'макита' in brand or 'Макита' in brand or 'МАКИТА' in brand:
                continue

            try:
                check_link = load_row_for_id(id_, 'search_table')[3]
            except TypeError:
                continue

            if check_id(id_, 'wb_table') and check_link:
                wb_name = load_row_for_id(id_, 'wb_table')[1]
                if 'Неизвестная модель' in load_row_for_id(id_, 'wb_table')[1]:
                    continue
                else:
                    save_price_wb_table(price, id_)

                wb_table_row = load_row_for_id(id_, 'wb_table')
                photo = wb_table_row[3]
                if not photo:
                    photo = get_product(id_)[1]
                    save_in_wb_table(id_, wb_table_row[1], price, photo)

                product_from_search = load_row_for_id(id_, 'search_table')
                if product_from_search is None:
                    url = url_master(wb_name)
                    try:
                        yandex_product = scrapper(url)
                    except AttributeError:
                        yandex_product = None

                    if yandex_product:
                        check_product = load_row_for_id(id_, 'suitable_products_table')
                        if check_product:
                            search_name = get_model(yandex_product['desc'], brand, '')
                            search_price = int(yandex_product['price'])
                            link = yandex_product['link']
                            save_in_search_table(id_, category + ' ' + brand + ' ' + search_name, search_price, link)
                            if 'Неизвестная модель' in search_name:
                                continue

                product_from_search = load_row_for_id(id_, 'search_table')

                if not product_from_search:
                    continue

                check_id_ = load_row_for_id(id_, 'suitable_products_table')
                if not check_id_:
                    try:
                        check_difference_and_price = compare(price, product_from_search[2])
                    except TypeError:
                        continue
                    if check_difference_and_price:
                        search_price = product_from_search[2]
                        link = product_from_search[3]
                        # message(photo=photo, name=wb_name, id_=id_, new_price=price,
                        #         search_price=search_price, link=link)
                        save_in_suitable_products_table(id_, wb_name, price, search_price)
                        continue
            else:
                model_from_name = get_model(name, brand, '')
                if 'Неизвестная модель' in model_from_name:
                    model_from_name = ''

                dirty_name, photo = get_product(id_)
                if 'модель' not in dirty_name:
                    model_name = get_model(dirty_name, brand, name) if dirty_name else get_model(name, brand, '')
                else:
                    model_name = dirty_name.replace('модель', '')
                try:
                    save_in_wb_table(id_, category + ' ' + brand + ' ' + model_name, price, photo)
                except Exception:
                    continue

                if 'Неизвестная модель' in model_name:
                    save_in_search_table(id_, 'Не найдено!', 1, photo)
                    continue

                if model_from_name:
                    url = url_master(category + ' ' + brand + ' ' + model_from_name)
                else:
                    url = url_master(category + ' ' + brand + ' ' + model_name)
                try:
                    yandex_product = scrapper(url)
                except AttributeError:
                    yandex_product = None

                if yandex_product:
                    search_name = get_model(yandex_product['desc'], brand, '')
                    search_price = int(yandex_product['price'])
                    link = yandex_product['link']
                    save_in_search_table(id_, category + ' ' + brand + ' ' + search_name, search_price, link)
                    if 'Неизвестная модель' in search_name:
                        continue

                    check_difference_and_price = compare(price, search_price)
                    if check_difference_and_price:
                        check_product = load_row_for_id(id_, 'suitable_products_table')
                        if check_product:
                            # message(photo=photo, name=category + ' ' + brand + ' ' + model_name, id_=id_,
                            #         new_price=price, search_price=search_price, link=link)
                            save_in_suitable_products_table(id_, category + ' ' + brand + ' ' + model_name,
                                                            price, search_price)
                else:
                    save_in_search_table(id_, 'Не найдено!', 1, 0)
                    continue
        except Exception as e:
            error_message(e)
            continue


category_dict = category_url()

if __name__ == '__main__':
    while True:
        for key, value in category_dict.items():
            print(key)
            main(value, key)
            product_monitoring()
        print('Iteration is complete. Wait to new iteration for 2 min!')
        time.sleep(120)


