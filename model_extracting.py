import re


def get_model(product_, brand, name):
    product_ = name + ' ' + product_
    product_ = re.sub(r'\bПОДАРОК\b', '', product_)
    product_ = re.sub(r'\bодарок\b', '', product_)
    # match_list = re.findall(r"\b[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я][\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{2,7}"
    #                         r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]"
    #                         r"{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}"
    #                         r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}", product_)
    match_list = re.findall(r"\b[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я][\da-zA-ZА-Я]{,7}[-,\s]?[a-zA-ZА-Я]{2,7}"
                            r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]"
                            r"{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}"
                            r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}", product_)
    # match_list = re.findall(r"\b[\da-zA-ZА-Я]{2,7}", product_)
    if match_list:
        product_model = max(match_list, key=len)
    else:
        return 'Неизвестная модель'
    brand_clear = product_model.replace(brand, '').replace(re.sub('(.)', lambda m: m.group(1).upper(), brand), '')
    if match_list and len(brand_clear) > 4:
        return brand_clear
    else:
        return 'Неизвестная модель'
    # if match_list:
    #     return match_list
    # else:
    #     return 'Неизвестная модель'


if __name__ == "__main__":
    product_list = [
        """Тепловая пушка, керамический нагреватель DHC 2-100, 2кВт Осенью и зимой мы особенно нуждаемся в 
        тепле и комфорте."""
        
        "Обогреватель для дома тепловентилятор Denzel",

        "Газовая пушка тепловая +ПОДАРОК Denzel",

        "95421 Бетономешалка B-125 550вт 130л Denzel",

        "Пылесос строительный RVC30, 1400 Вт, бак 30 л Denzel",

        "Всасывающий шланг для моек высокого давления 58307 Denzel",

        "Строительный пылесос с насадками LVC15 +ПОДАРОК! Denzel"
                    ]

    for product in product_list:
        match = get_model(product, 'Denzel', 'Обогреватель для дома')
        print(match)
