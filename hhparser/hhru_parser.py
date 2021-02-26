import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

PATH = 'C:\\Users\\Computer\\Desktop\\chromedriver.exe'
'''В данном файле все try except нацелены либо на получение данных с сайта hh.ru,
   не важно какая будет ошибка поэтому они не описаны внутри проверки
'''


class HhruParser:
    '''Скрапер для hh.ru'''
    def __init__(self, *args, **kwargs):
        '''Инициализируем драйвер браузера'''
        # copy используется обязательно, без этого метода драйвер не заработает
        caps = DesiredCapabilities.CHROME.copy()
        caps |= {'maxInstances': 4}
        print(caps)
        if 'no-javascript' in args:
            options = Options()
            options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
            self.driver = webdriver.Remote(
                command_executor='http://135.181.195.100:4444',
                desired_capabilities=caps,
                options=options
                )
            self.driver.maximize_window()
        else:
            self.driver = webdriver.Remote(
                command_executor='http://135.181.195.100:4444',
                desired_capabilities=caps,
                )
            self.driver.maximize_window()

    def get_page_blocks(self):
        '''Получаем блок со стрницами в футере сайта hh.ru'''
        page_blocks = self.driver.find_elements_by_class_name("pager-item-not-in-short-range")
        return page_blocks

    def get_num_of_pages(self, page_block):
        '''Получаем количество страниц с объявлениями'''
        page_block = page_block[-1]
        pages = page_block.find_elements_by_class_name("bloko-button")[0].text
        return pages

    def next_page(self):
        '''Переходит на следующую страницу'''
        next_page = self.driver.find_element_by_css_selector('[data-qa="pager-next"]')
        ActionChains(self.driver).click(next_page).perform()

    def get_current_url(self):
        try:
            return self.driver.current_url.split('?')[0]
        except:
            return self.driver.current_url

    def get_list_of_ads(self):
        '''Получаем список объявлений на одной странице'''
        ads = self.driver.find_elements_by_class_name("vacancy-serp-item")
        return ads

    def get_ad(self, list_of_ads, index_of_ad):
        '''Получаем одно объявление из списка страниц'''
        return list_of_ads[index_of_ad]

    def get_title(self):
        '''Получаем название объявления'''
        try:
            name = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-title"]'))
            ).text
        except:
            name = ''
        return name

    def get_address(self):
        try:
            city = self.driver.find_element_by_css_selector('[data-qa="vacancy-view-raw-address"]')
        except:
            city = self.driver.find_element_by_css_selector('[data-qa="vacancy-view-location"]')
        return city.text.split(', ')[0]

    def get_company_name(self):
        try:
            return self.driver.find_element_by_css_selector('[data-qa="vacancy-company-name"]').text
        except:
            return ''

    def get_detail_page(self, ad):
        detail = ad.find_element_by_css_selector('[data-qa="vacancy-serp__vacancy-title"]')
        ActionChains(self.driver).click(detail).perform()
        time.sleep(1)
        self.driver.switch_to_window(self.driver.window_handles[1])

    def close_detail_page(self):
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def get_details(self, selector):
        try:
            return self.driver.find_element_by_css_selector(selector).text
        except:
            return ""

    def get_experience(self):
        '''Работает только после получения детальной страницы'''
        try:
            experience = self.driver.find_element_by_css_selector('[data-qa="vacancy-experience"]').text
            return experience
        except:
            return ""

    def get_type_of_employment(self):
        '''Работает только после получения детальной страницы'''
        try:
            type_of_employment = self.driver.find_element_by_css_selector('[data-qa="vacancy-view-employment-mode"]').text
            return type_of_employment
        except:
            return ""

    def get_description(self):
        '''Работает только после получения детальной страницы'''
        try:
            description = self.driver.find_element_by_css_selector('[data-qa="vacancy-description"]').text
            return description
        except:
            return ""

    def get_phone(self):
        '''Получаем номер телефона'''
        try:
            phone = self.driver.find_element_by_css_selector('[data-qa="vacancy-contacts__phone"]').text
            phone = phone.split(',')[0]
            return phone
        except:
            return ""

    def get_email(self):
        try:
            return self.driver.find_element_by_css_selector('[data-qa="vacancy-contacts__email"]').text
        except:
            return ""

    def get_first_page(self, ad):
        '''Переходит на первую страницу'''
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-qa='first-page']")))
        except NoSuchElementException:
            print("Нет кнопки в начало")

    def show_contacts(self):
        try:
            contacts = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="show-employer-contacts"]')))
            ActionChains(self.driver).click(contacts).perform()
        except:
            print('Нет данных о контактах')
        time.sleep(0.2)

    def get_salary(self):
        '''Получаем зарплату на вакансии
        '''
        try:
            salary = self.driver.find_element_by_class_name("vacancy-salary").text
            if salary == 'з/п не указана':
                return None
            salary = int(''.join(salary.split(' ')[1:3]))
            return salary
        except:
            return None