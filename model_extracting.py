import re


def get_model(product_, brand, name):
    product_ = name + ' ' + product_
    product_ = re.sub(r'\bПОДАРОК\b', '', product_)
    product_ = re.sub(r'\bодарок\b', '', product_)
    # match_list = re.findall(r"\b[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я][\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{2,7}"
    #                         r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]"
    #                         r"{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}"
    #                         r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}", product_)
    match_list = re.findall(r"\b[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я][\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{2,7}"
                            r"[-,.\s]?[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{,7}[-,.\s]?"
                            r"[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{,7}"
                            r"[-,.\s]?[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{,7}[-,.\s]?[\da-zA-ZА-Я]{,7}", product_)
    if match_list:
        match_list = [re.sub(r"[А-ЯA-Za-z]{4,20}", '', item) for item in match_list]
        match_list = [s.replace('220 В', '').replace('220В', '') for s in match_list]
        match_list = [s.replace('SDS', '').replace('АКБ', '') for s in match_list]
        match_list = [s.replace('Li-ion', '').replace('LI-ION', '') for s in match_list]
        match_list = [i.replace(brand, '').replace(re.sub('(.)', lambda m: m.group(1).upper(), brand), '') for i in match_list]
        product_model = max(match_list, key=len)
    else:
        return 'Неизвестная модель'
    brand_clear = product_model.replace(brand, '').replace(re.sub('(.)', lambda m: m.group(1).upper(), brand), '')
    if match_list and len(brand_clear) > 4:
        return product_model
    else:
        return 'Неизвестная модель'
    # if match_list:
    #     return match_list
    # else:
    #     return 'Неизвестная модель'


if __name__ == "__main__":
    product_list = [
        """Тепловая пушка, керамический нагреватель DHC 2-100, 2кВт Осенью и зимой мы особенно нуждаемся в 
        тепле и комфорте.""",
        
        "Обогреватель для дома тепловентилятор Denzel",

        "Газовая пушка тепловая +ПОДАРОК Denzel",

        "95421 Бетономешалка B-125 550вт 130л Denzel",

        "Пылесос строительный RVC30, 1400 Вт, бак 30 л Denzel",

        "Всасывающий шланг для моек высокого давления 58307 Denzel",

        "Строительный пылесос с насадками LVC15 +ПОДАРОК! Denzel",

        "Устройство зарядное для аккумуляторов IBC-18-2.3, Li-ion, 18 В, 2.3 А Denzel (28453)",

        "ZKV1500, 220В",

        "ЗУБР  ПРЕМИУМ СЛЕДОПЫТ",

        "Газонокосилка бензиновая ГБ-400",

        "Гайковерт пневматический ударный МГ-320",
        
        'Гайковерт ударный сетевой 300 Нм, 1 2" ГС-300',

        'Перфоратор П-650к, 650 Вт',
    
                    ]

    for product in product_list:
        match = get_model(product, 'Denzel', 'Обогреватель для дома')
        print(match)
