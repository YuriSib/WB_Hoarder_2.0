import requests
from pattern_extracting import get_power


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


def get_property(grouped_options, parameter):
    product = False
    if grouped_options:
        if type(grouped_options[0]) is not int:
            property_list = grouped_options[0].get('options', None)
            for property_ in property_list:
                if parameter in property_['name'] and 'оминальн' not in property_['name']:
                    product = property_['value']
                    return product
            if product is False:
                product = 0
        else:
            product = 0
    else:
        product = 0
    return product


def price_counter(grouped_options, description, average_price, average_power):
    power = float(str(get_property(grouped_options, 'кВт')).replace(' ', '').replace('кВт', '').replace('Вт', '')\
        .replace('квт', ''))
    if power:
        shortening = str(power).replace('.', '')
        if len(shortening) >= 3:
            power = float(power) / 1000
    else:
        power = get_power(description)

    if not power:
        return 'Не удалось определить мощность!'

    different = ((float(power) - average_power) / average_power) * 100
    min_price = average_price + (average_price * different / 100)

    return min_price


def get_price(category, description, grouped_options):
    if grouped_options and 'компрессор' in category:
        volume = get_property(grouped_options, 'есивер')
        if not volume:
            return 'Не удалось определить объем ресивера!'

        if '24' in volume:
            min_price = price_counter(grouped_options, description, 8000, 1.6)
        elif '50' in volume:
            min_price = price_counter(grouped_options, description, 12000, 1.8)
        elif '100' in volume:
            min_price = price_counter(grouped_options, description, 22000, 2.2)

    elif grouped_options and 'тепловая пушка' in category:
        fuel = get_property(grouped_options, 'опливо')
        if not fuel:
            if 'лектр' in description or 'сеть' in description or 'Cеть' in description:
                fuel = 'сеть'
            elif 'азов' in description or 'ропан' in description or 'етан' in description:
                fuel = 'газ'
            elif 'изель' in description:
                fuel = 'дизель'
            else:
                return 'Не удалось определить тип топлива!'
        else:
            if 'лектр' in description or 'сеть' in description or 'Cеть' in description:
                fuel = 'сеть'
            elif 'газ' in fuel or 'Газ' in fuel or 'ропан' in fuel or 'етан' in fuel:
                fuel = 'газ'
            elif 'изель' in fuel:
                fuel = 'дизель'
            else:
                return 'Не удалось определить тип топлива!'

        if 'сеть' in fuel:
            min_price = price_counter(grouped_options, description, 2000, 2)
        elif 'газ' in fuel:
            min_price = price_counter(grouped_options, description, 7000, 2.3)
        elif 'дизель' in fuel:
            min_price = price_counter(grouped_options, description, 15000, 20)

    elif grouped_options and 'пила' in category:
        type_ = get_property(grouped_options, 'ип пилы')
        if not type_:
            if 'исковая' in description or 'иркулярн' in description:
                type_ = 'циркулярная'
            elif 'абельн' in description:
                type_ = 'сабельная'
            elif 'епная' in description:
                type_ = 'цепная'
            elif 'орцовочн' in description:
                type_ = 'торцовочная'
            else:
                return 'Не удалось определить тип пилы!'
        else:
            if 'исковая' in type_ or 'иркулярн' in type_:
                type_ = 'циркулярная'
            elif 'абельн' in type_:
                type_ = 'сабельная'
            elif 'епная' in type_:
                type_ = 'цепная'
            elif 'орцовочн' in type_:
                type_ = 'торцовочная'
            else:
                return 'Не удалось определить тип пилы!'

        if 'циркулярная' in type_:
            min_price = price_counter(grouped_options, description, 4000, 1)
        elif 'сабельная' in type_:
            min_price = price_counter(grouped_options, description, 4000, 1)
        elif 'цепная' in type_:
            min_price = price_counter(grouped_options, description, 3000, 1)
        elif 'торцовочная' in type_:
            min_price = price_counter(grouped_options, description, 10000, 1.5)

    elif grouped_options and 'пылесос' in category:
        min_price = price_counter(grouped_options, description, 4000, 1.4)

    elif grouped_options and 'сверлильный станок' in category:
        min_price = price_counter(grouped_options, description, 9000, 0.55)

    elif grouped_options and 'лобзик' in category:
        min_price = price_counter(grouped_options, description, 3500, 1.3)

    elif grouped_options and 'генератор' in category:
        min_price = price_counter(grouped_options, description, 19000, 3.3)

    elif grouped_options and 'фрезер' in category:
        min_price = price_counter(grouped_options, description, 4000, 0.8)

    elif grouped_options and 'штроборез' in category:
        min_price = price_counter(grouped_options, description, 7000, 1.4)

    elif grouped_options and 'электрорубанок' in category:
        min_price = price_counter(grouped_options, description, 4000, 1.1)

    elif grouped_options and 'миксер строительный' in category:
        min_price = price_counter(grouped_options, description, 4000, 2)

    elif grouped_options and 'полировальная машина' in category:
        min_price = price_counter(grouped_options, description, 3500, 1.4)

    elif grouped_options and 'шлифовальная машина' in category:
        min_price = price_counter(grouped_options, description, 2600, 0.8)

    return min_price


def get_product(id_, category):
    response, url_ = curl_creator(id_)
    if response == 0:
        response, url_ = curl_creator(id_, 3, 5)
        if response == 0:
            response, url_ = curl_creator(id_, 2, 4)

    photo_link = url_.replace('info/ru/card.json', 'images/big/1.webp')

    if response == 0:
        return 0

    description = response.get('description', None)
    grouped_options = response.get('grouped_options', None)

    product = get_property(grouped_options, 'Модель')
    if not product:
        product = description

    average_price = get_price(category, description, grouped_options)

    description = description[:200] + '...'

    return product, description, photo_link, average_price


if __name__ == "__main__":
    url = f'https://catalog.wb.ru/catalog/repair10/catalog?appType=1&limit=100&cat=128968&curr=rub&dest=-1257786&' \
          f'regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&uclusters=0&page='
    a = get_category(url)
    print(a)
    # a = get_product('164614093', 'name', 100500)
    # print(a)