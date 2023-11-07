import time

from main import compare
from avito_price import get_price
from wb_master import get_category, get_product
from sql_master import check_id, save_price_wb_table, load_row_for_id, save_in_wb_table, save_in_search_table,\
    save_average_price
from tg_master import avito_message
from pattern_extracting import get_model
from url_master import category_url


def main(url, category):
    category_list = get_category(url)

    for product in category_list:
        name, brand = product['Наименование'], product['Бренд'],
        price, id_ = product['Цена со скидкой'], product['Артикул, id']

        if 'akita' in brand or 'AKITA' in brand or 'osch' in brand or 'OSCH' in brand or 'ewalt' in brand or \
                'EWALT' in brand or 'eWalt' in brand or 'eWalt' in brand:
            continue

        if check_id(id_, 'wb_table'):
            wb_name, average_price = load_row_for_id(id_, 'wb_table')[1], load_row_for_id(id_, 'wb_table')[3]
            save_price_wb_table(price, id_)

            if not average_price:
                average_price = get_price(id_, category)

            check_difference = compare(price, average_price, 15)
            if check_difference:
                save_average_price(price)
                avito_message(wb_name, id_, price, average_price)

        else:
            model_from_name = get_model(name, brand, '')
            if 'Неизвестная модель' in model_from_name:
                model_from_name = ''

            dirty_name = get_product(id_)
            model_name = get_model(dirty_name, brand, name) if dirty_name else get_model(name, brand, '')
            try:
                save_in_wb_table(id_, category + ' ' + brand + ' ' + model_name, price)
            except Exception:
                continue

            if model_from_name:
                name = category + ' ' + brand + ' ' + model_from_name
            else:
                name = category + ' ' + brand + ' ' + model_name

            average_price = get_price(id_, category)
            check_difference = compare(price, average_price, 15)
            if check_difference:
                save_average_price(price)
                avito_message(name, id_, price, average_price)


category_dict = category_url()

if __name__ == "__main__":
    while True:
        for key, value in category_dict.items():
            print(key)
            main(value, key)
        print('Iteration is complete. Wait to new iteration for 2 min!')
        time.sleep(120)





