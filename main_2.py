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
            wb_name, average_price = load_row_for_id(id_, 'wb_table')[1], load_row_for_id(id_, 'wb_table')[4]
            photo_link = load_row_for_id(id_, 'wb_table')[2]
            save_price_wb_table(price, id_)

            if average_price == int or average_price == float:
                check_difference = compare(price, average_price, 15)
                if check_difference:
                    avito_message(wb_name, id_, price, average_price, photo_link)

        else:
            dirty_name, description, photo_link, average_price = get_product(id_, category)
            save_in_wb_table(id_, description, photo_link, price, average_price)

            if average_price == int or average_price == float:
                check_difference = compare(price, average_price, 15)
                save_average_price(id_, average_price)

                if check_difference:
                    avito_message(description, id_, price, average_price, photo_link)
            else:
                continue


category_dict = category_url()

if __name__ == "__main__":
    while True:
        for key, value in category_dict.items():
            print(key)
            main(value, key)
        print('Iteration is complete. Wait to new iteration for 2 min!')
        time.sleep(2700)





