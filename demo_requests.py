from twocaptcha import TwoCaptcha
import logging

import requests
from bs4 import BeautifulSoup

from config import API_KEY
# NOTE: Enabling logging will print the API KEY to the console
logging.basicConfig(level=logging.DEBUG)


solver = TwoCaptcha(API_KEY)
sitekey = '6LfGNEoeAAAAALUsU1OWRJnNsF1xUvoai0tV090n'
url = 'https://www.scrapebay.com/spam'


def solve(sitekey, url):
    try:
        result = solver.recaptcha(sitekey=sitekey, url=url)
    except Exception as e:
        exit(e)

    return result.get('code')


def get_csrf_token(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    csrf_el = soup.select_one('[name="csrfmiddlewaretoken"]')
    csrf_token = csrf_el.get('value')
    return csrf_token


def main():
    csrf_token = get_csrf_token(url)
    print('Received CSRF token', csrf_token)
    captcha = solve(sitekey, url)
    print('Solved Captcha', captcha)

    payload = 'csrfmiddlewaretoken={}&g-recaptcha-response={}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.scrapebay.com/spam',
        'Cookie': f'csrftoken={csrf_token}'
    }

    response = requests.post(url,
                             headers=headers,
                             data=payload.format(csrf_token, captcha)
                             )
    soup = BeautifulSoup(response.text, 'lxml')
    print('~' * 20)
    print(soup.select_one('td:last-child').get_text())


if __name__ == '__main__':
    main()
