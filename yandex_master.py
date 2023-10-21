from bs4 import BeautifulSoup
from urllib.parse import quote
from sql_master import sql_row_counter

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth


def url_master(qwery):
    response = quote(qwery)
    url_ = f'https://yandex.ru/search/?text={response}'

    return url_


def html_obj(url):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(url=url)
    wait = WebDriverWait(driver, 25)
    try:
        wait.until(EC.presence_of_element_located(("xpath", "/html/body/main/div[2]/div[2]/div/div[1]/nav/div/div[6]/a")))
    except Exception:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    html = driver.page_source

    return html


def scrapper(url_):
    html = html_obj(url_)
    print('Объект класса Driver создан, html изъят со станицы поиска!')
    soup = BeautifulSoup(html, 'lxml')
    options_list = soup.find_all('div', {'class': 'Organic Organic_withThumb Organic_thumbFloat_right Organic_thumbPo'
                                                  'sition_full organic Typo Typo_text_m Typo_line_s i-bem'})
    if options_list:
        product_list = []
        for option in options_list:
            price_html = option.find('span', {'class': 'PriceValue'})
            if price_html:
                dirty_price = price_html.find('span', {'class': 'A11yHidden'})
                price = dirty_price.get_text(strip=True) if dirty_price else price_html.get_text(strip=True)

                desc = option.find('div', {'class': 'TextContainer OrganicText organic__text text-container '
                                   'Typo Typo_text_m Typo_line_m'}).get_text().replace('<b>', ' ').replace('</b>', ' ')

                link = option.find('div', {'class': 'Path Organic-Path path organic__path'}).a['href']

                product_list.append({'price': price, 'desc': desc, 'link': link})

        price = 999999
        min_price_product = 0
        for product in product_list:
            price_int = int(''.join(filter(str.isdigit, product['price'])))

            if 3000 < int(price_int) < price and 'erries' not in product['link']:
                min_price_product = product
            price = int(product['price'])

            quantity_rows = sql_row_counter('search_table')
            try:
                quantity_rows_int = int(''.join(filter(str.isdigit, quantity_rows)))
            except TypeError:
                quantity_rows_int = int(''.join(filter(str.isdigit, str(quantity_rows[0]))))
        if (quantity_rows_int % 10) == 0:
            print(f'Количество строк в БД - {quantity_rows_int} штук.')
        return min_price_product
    else:
        print('Подходящего товара в поисковой выдаче не найдено!')
        return 0


if __name__ == "__main__":
    url = 'https://yandex.ru/search/?text=%D0%AD%D0%BA%D1%81%D1%86%D0%B5%D0%BD%D1%82%D1%80%D0%B8%D0%BA%D0%BE%D0%B2%D' \
          '0%B0%D1%8F+%D1%88%D0%BB%D0%B8%D1%84%D0%BE%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%88%D0' \
          '%B8%D0%BD%D0%B0+%D0%AD%D0%A8%D0%9C-125%D0%9A&lr=10649'
    product_list = scrapper(url)

    print(product_list)
