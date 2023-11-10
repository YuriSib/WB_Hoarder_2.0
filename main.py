import time

from wb_master import get_category, get_product
from sql_master import check_id, save_price_wb_table, load_row_for_id, save_in_wb_table, \
    save_in_search_table, save_price_suitable_products_table, load_rows_from_suitable_products_table
from yandex_master import scrapper, url_master
from tg_master import message, error_message, monitoring_massage
from pattern_extracting import get_model
from url_master import category_url


def compare(price_wb, price_search, percent=35):
    try:
        price_wb, price_search = float(price_wb), float(price_search)
    except ValueError:
        return False
    difference = (price_search - price_wb) / price_search * 100
    if difference > percent and price_search > 4000:
        check_difference = True
    else:
        check_difference = False

    return check_difference


def product_monitoring():
    product_list = load_rows_from_suitable_products_table()
    for product in product_list:
        id_, name, price_curr, price_last, average_price = product[0], product[1], product[2], product[3], product[4]
        current_price = load_row_for_id(id_, 'wb_table')[2]
        if price_curr != price_last and price_last is not None:
            name_in_search = load_row_for_id(id_, 'search_table')[1]
            monitoring_massage(id_, name, current_price, price_last, average_price, name_in_search)
        save_price_suitable_products_table(current_price, price_curr, id_)


def main(url, category):
    category_list = get_category(url)

    error_counter = 0

    for product in category_list:
        # try:
            name, brand = product['Наименование'], product['Бренд'],
            price, id_ = product['Цена со скидкой'], product['Артикул, id']

            if 'akita' in brand or 'AKITA' in brand or 'osch' in brand or 'OSCH' in brand or 'ewalt' in brand or \
                'EWALT' in brand or 'eWalt' in brand or 'eWalt' in brand:
                continue

            if check_id(id_, 'wb_table'):
                wb_name = load_row_for_id(id_, 'wb_table')[1]
                if 'Неизвестная модель' in load_row_for_id(id_, 'wb_table')[1]:
                    continue
                else:
                    save_price_wb_table(price, id_)

                product_from_search = load_row_for_id(id_, 'search_table')
                if product_from_search is None:
                    url = url_master(wb_name)
                    try:
                        yandex_product = scrapper(url)
                    except AttributeError:
                        yandex_product = None

                    if yandex_product:
                        search_name = get_model(yandex_product['desc'], brand, '')
                        search_price = int(yandex_product['price'])
                        save_in_search_table(id_, category + ' ' + brand + ' ' + search_name, search_price)
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
                        message(dirty_name=name, name=wb_name, id_=id_, new_price=price,
                                search_price=product_from_search[2], name_in_search=product_from_search[1])
                        continue
            else:
                model_from_name = get_model(name, brand, '')
                if 'Неизвестная модель' in model_from_name:
                    model_from_name = ''

                dirty_name, curl = get_product(id_)
                model_name = get_model(dirty_name, brand, name) if dirty_name else get_model(name, brand, '')
                try:
                    save_in_wb_table(id_, category + ' ' + brand + ' ' + model_name, curl, price)
                except Exception:
                    continue

                if 'Неизвестная модель' in model_name:
                    save_in_search_table(id_, 'Не найдено!', 1)
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
                    save_in_search_table(id_, category + ' ' + brand + ' ' + search_name, search_price)
                    if 'Неизвестная модель' in search_name:
                        continue

                    check_difference_and_price = compare(price, search_price)
                    if check_difference_and_price:
                        message(dirty_name=name, name=category + ' ' + brand + ' ' + model_name, id_=id_,
                                new_price=price, search_price=search_price, name_in_search=brand + ' ' + search_name)
                else:
                    save_in_search_table(id_, 'Не найдено!', 1)
                    continue
        # except Exception as e:
        #     error_message(e)
        #     continue


category_dict = category_url()

if __name__ == '__main__':
    while True:
        for key, value in category_dict.items():
            print(key)
            main(value, key)
            product_monitoring()
        print('Iteration is complete. Wait to new iteration for 2 min!')
        time.sleep(120)


