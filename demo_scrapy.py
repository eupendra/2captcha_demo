import scrapy

from config import API_KEY

from twocaptcha import TwoCaptcha
from scrapy.exceptions import CloseSpider

solver = TwoCaptcha(API_KEY)
sitekey = '6LfGNEoeAAAAALUsU1OWRJnNsF1xUvoai0tV090n'
url = 'https://www.scrapebay.com/spam'


class CaptchaSpider(scrapy.Spider):
    name = 'captcha'
    start_urls = [url]

    def parse(self, response):
        try:
            result = solver.recaptcha(sitekey=sitekey, url=url)
        except Exception as e:
            raise CloseSpider('Could not solve captcha')

        captcha = result.get('code')
        payload = {
            'g-recaptcha-response': captcha
        }
        yield scrapy.FormRequest.from_response(response,
                                               formdata = payload,
                                               callback = self.parse_page)
    def parse_page(self, response):
        yield {
            'data': response.css('td:last-child ::text').get()
        }
