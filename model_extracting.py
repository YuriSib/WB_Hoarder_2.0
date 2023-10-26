import re


def get_model(product, brand):
    product = product.replace(brand, '')
    product = re.sub(r'\bПОДАРОК\b', '', product)
    product = re.sub(r'\bодарок\b', '', product)
    match_list = re.findall(r"\b[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я][\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{2,7}"
                            r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]"
                            r"{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}"
                            r"[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}[-,\s]?[\da-zA-ZА-Я]{,7}", product)
    if match_list:
        return max(match_list, key=len)
    else:
        return 'Неизвестная модель'


if __name__ == "__main__":
    product_list = [
        "Обогреватель для дома тепловентилятор Denzel",

        "Газовая пушка тепловая +ПОДАРОК Denzel",

        "95421 Бетономешалка B-125 550вт 130л Denzel",

        "Пылесос строительный RVC30, 1400 Вт, бак 30 л Denzel",

        "Всасывающий шланг для моек высокого давления 58307 Denzel",

        "Строительный пылесос с насадками LVC15 +ПОДАРОК! Denzel"
                    ]

    for product in product_list:
        match = get_model(product, 'Denzel')
        print(match)
