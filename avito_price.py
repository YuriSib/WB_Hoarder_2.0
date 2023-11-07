from wb_master import curl_creator, get_property
from sql_master import load_property_and_price
from pattern_extracting import get_power


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


def get_price(id_, category):
    response = curl_creator(id_)
    if response == 0:
        response = curl_creator(id_, 3, 5)
        if response == 0:
            response = curl_creator(id_, 2, 4)
    if response == 0:
        return 0

    description = response.get('description', None)
    grouped_options = response.get('grouped_options', None)

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


# different = ((2.2 - 3.3) / 3.3) * 100
# min_price = 19000 + (19000 * different / 100)
# print(min_price)
