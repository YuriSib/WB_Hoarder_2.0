import requests
from bs4 import BeautifulSoup


def settings(url, page=''):
    url = f'{url}{page}'

    headers = {
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'Referer': 'https://www.wildberries.ru/catalog/164614093/detail.aspx',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url=url, headers=headers, timeout=60)
    if response.status_code != 200:
        return 0

    return response.json()


def prepare_items(response):
    products = []

    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
                if float(product.get('salePriceU', None)) / 100 > 1000:
                    products.append({
                        'Наименование': product.get('name', None),
                        'Бренд': product.get('brand', None),
                    'Цена со скидкой': float(product.get('salePriceU', None)) / 100 if
                    product.get('salePriceU', None) != None else None,
                    'Артикул, id': product.get('id', None),
                })

    return products


def hoarder(url, page):
    response = settings(url, page)
    products = prepare_items(response) if response else []

    return products


def get_category(url):
    product_list = []
    control = True
    cnt = 1
    while True:
        products = hoarder(url, f'{cnt}')
        print(cnt)
        if products:
            product_list.extend(products)
            control = True
        else:
            if control:
                control = False
            else:
                break
        cnt += 1

    return product_list


def curl_creator(id_, vol=4, part=6):
    for number in range(0, 17):
        num = number if number >= 10 else '0' + str(number)
        url = f'https://basket-{num}.wb.ru/vol{str(id_)[:vol]}/part{str(id_)[:part]}/{str(id_)}/info/ru/card.json'
        try:
            response = settings(url)
            if response:
                break
        except Exception:
            continue
    return response, url


def get_product(id_):
    response, url_ = curl_creator(id_)
    if response == 0:
        response, url_ = curl_creator(id_, 3, 5)
        if response == 0:
            response, url_ = curl_creator(id_, 2, 4)
    if response == 0:
        return 0, 0

    photo_link = url_.replace('info/ru/card.json', 'images/big/1.webp')

    product = False
    description = response.get('description', None)
    grouped_options = response.get('grouped_options', None)
    if grouped_options:
        if type(grouped_options[0]) is not int:
            property_list = grouped_options[0].get('options', None)
            for property_ in property_list:
                if property_['name'] == 'Модель':
                    product = property_['value']
                    return product, photo_link
            if product is False:
                product = description
        else:
            product = description
    else:
        product = description
    return product, photo_link


if __name__ == "__main__":
    url = f'https://catalog.wb.ru/catalog/repair10/catalog?appType=1&limit=100&cat=128968&curr=rub&dest=-1257786&' \
          f'regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&uclusters=0&page='
    a = get_category(url)
    print(a)
    # a = get_product('164614093', 'name', 100500)
    # print(a)