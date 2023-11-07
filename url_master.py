def category_url():
    category_dict_ = {
        # 'перфоратор': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
        #                'cat=128961&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=1166&page=',
        #
        # 'шуруповерт': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
        #               'cat=128961&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=2197&page=',

        'генератор': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
                     'cat=128968&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=3863&page=',

        'компрессор': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
                      'cat=128968&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=926&page=',

        'пылесос': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
                   'cat=128968&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=2995&page=',

        'сверлильный станок': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&'
                              'appType=1&cat=128968&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=4160&page=',

        'тепловая пушка': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
                          'cat=128968&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=2550&page=',

        # 'бензорез': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat='
        #             '128963&curr=rub&dest=-1257786&priceU=600000%3B28911300&sort=popular&spp=29&xsubject=4017&page=',

        'лобзик': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
                  'cat=128963&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=8279&page=',

        'пила': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&cat=128963&'
                'curr=rub&dest=-1257786&priceU=100000%3B26640200&sort=popular&spp=29&xsubject=1169%3B8102%3B8103&page=',

        'фрезер': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1&'
                  'cat=128963&curr=rub&dest=-1257786&priceU=150000%3B26640200&sort=popular&spp=29&xsubject=1167&page=',

        'штроборез': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1'
                     '&cat=128963&curr=rub&dest=-1257786&page=1&sort=popular&spp=29&xsubject=1337&page=',

        'электрорубанок': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1'
                          '&cat=128963&curr=rub&dest=-1257786&&sort=popular&spp=29&xsubject=1171page=',

        'миксер строительный': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test'
                               '&appType=1&cat=128966&curr=rub&dest=-1257786&priceU=160000%3B5031300'
                               '&sort=popular&spp=29&xsubject=2297&page=',

        # 'сварочный аппарат': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test&appType=1'
        #                      '&cat=128962&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=1318&page=',

        'полировальная машина': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test'
                                '&appType=1&cat=128964&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=2668&page=',

        'шлифовальная машина': 'https://catalog.wb.ru/catalog/repair10/catalog?TestGroup=no_test&TestID=no_test'
                               '&appType=1&cat=128964&curr=rub&dest=-1257786&sort=popular&spp=29&xsubject=1168&page=',
    }
    return category_dict_


if __name__ == "__main__":
    category_dict = category_url()
    for key, value in category_dict.items():
        print(key, value)
