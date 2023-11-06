from wb_master import curl_creator, get_property
from sql_master import load_property_and_price
from pattern_extracting import get_power


def price_counter(grouped_options, description, average_price, average_power):
    power = get_property(grouped_options, 'ощность').replace(' ', '').replace('кВт', '').replace('Вт', '')\
        .replace('квт', '')
    if power:
        shortening = power.replace('.', '')
        if len(shortening) >= 3:
            power = float(power) / 1000
    else:
        power = get_power(description)

    different = ((power - average_power) / average_power) * 100
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

    if grouped_options and 'генератор' in category:
        min_price = price_counter(grouped_options, description, 1900, 3.3)

    elif grouped_options and 'компрессор' in category:
        min_price = price_counter(grouped_options, description, 1900, 3.3)

