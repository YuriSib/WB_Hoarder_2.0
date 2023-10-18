from bs4 import BeautifulSoup
from urllib.parse import quote
import g4f

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth


def gpt_helper(text_):
    response_ = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{text_} Переработай этот текст таким образом, чтобы осталось только"
                                              f" название товара."}],
    )

    return response_


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
    driver = webdriver.Chrome(
        executable_path='/root/.cache/selenium/chromedriver/linux64/118.0.5993.70/chromedriver',
        options=options
    )

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(url=url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located(("xpath", "/html/body/main/div[2]/div[2]/div/div[1]/nav/div/div[6]/a")))
    html = driver.page_source

    return html


def scrapper(url_):
    html = html_obj(url_)
    soup = BeautifulSoup(html, 'lxml')
    options_list = soup.find_all('div', {'class': 'Organic Organic_withThumb Organic_thumbFloat_right Organic_thumbPosition_full organic Typo Typo_text_m Typo_line_s i-bem'})

    product_list = []
    for option in options_list:
        price_html = option.find('span', {'class': 'PriceValue'})
        if price_html:
            price = price_html.find('span', {'class': 'A11yHidden'}).get_text(strip=True)

            desc = option.find('div', {'class': 'TextContainer OrganicText organic__text text-container '
                               'Typo Typo_text_m Typo_line_m'}).get_text().replace('<b>', ' ').replace('</b>', ' ')

            product_list.append({'price': price, 'desc': desc})

    price = 999999
    min_price_product = []
    for product in product_list:
        if int(product['price']) < price:
            min_price_product = product
        price = int(product['price'])

    return min_price_product


if __name__ == "__main__":
    url = 'https://yandex.ru/search/?text=%D0%AD%D0%BA%D1%81%D1%86%D0%B5%D0%BD%D1%82%D1%80%D0%B8%D0%BA%D0%BE%D0%B2%D' \
          '0%B0%D1%8F+%D1%88%D0%BB%D0%B8%D1%84%D0%BE%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%88%D0' \
          '%B8%D0%BD%D0%B0+%D0%AD%D0%A8%D0%9C-125%D0%9A&lr=10649'
    product_list = scrapper(url)

    print(product_list)
