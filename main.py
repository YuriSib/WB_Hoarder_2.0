

from wb_master import get_product, get_category
from sql_master import check_id, save_price_wb_table, load_row_for_id, qwery_in_sql, save_in_wb_table, save_in_search_table
from yandex_master import scrapper, url_master


def compare(price_wb, price_search):
    difference = (price_search - price_wb) / price_search * 100
    if difference > 30:
        check_difference = True
    else:
        check_difference = False

    return check_difference


def main(url):
    category_list = get_category(url)

    for product in category_list:
        # Делаем API запрос к категории по URL, на выходе получаем {'id': 'id', 'name': 'name', 'price': 'price'}
        name, price, id_ = product['Наименование'], product['Цена со скидкой'], product['Артикул, id']
        
        if check_id(id_, 'wb_table'):
            save_price_wb_table(price, id_)
            product_from_search = load_row_for_id(id_, 'search_table')

            if product_from_search:
                check_difference = compare(price, product_from_search[2])
                if check_difference:
                    # Выводим сообщение в ТГ
                    pass
            else:
                qwery = qwery_in_sql(id_)
                url = url_master(qwery)

                # Ищем этот товар в поиске
                product = scrapper(url)
                name, search_price = product['desc'], int(product['desc'])
                different = compare(price, search_price)
                # Добавляем его в таблицу search_table БД
                save_in_search_table(id_, name, price, different)
        else:
            product_list = get_product(id_, name, price)
            save_in_wb_table(product_list[0], product_list[1], product_list[2], product_list[3])

            # Ищем этот товар в поиске
            pass
        
    
        
    