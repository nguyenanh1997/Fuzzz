import string
import random
import re
from urllib.parse import urljoin

import requests_html
from bs4 import BeautifulSoup
from math import log
#from w3af.core.controllers.misc.fuzzy_string_cmp import fuzzy_equal
from colorama import Fore, init

init(autoreset=True)

COMMON_CSRF_NAMES = (
    'csrf_token',
    'CSRFName',  # OWASP CSRF_Guard
    'CSRFToken',  # OWASP CSRF_Guard
    'anticsrf',  # AntiCsrfParam.java
    '__RequestVerificationToken',  # AntiCsrfParam.java
    'token',
    'csrf',
    'YII_CSRF_TOKEN',  # http://www.yiiframework.com/
    'yii_anticsrf'  # http://www.yiiframework.com/
    '[_token]',  # Symfony 2.x
    '_csrf_token',  # Symfony 1.4
    'csrfmiddlewaretoken',  # Django 1.5
)


class Csrf_Scanner:
    def __init__(self, session, password, logger):
        self.session = requests_html.HTMLSession()
        self.password = password
        self.logger = logger
        self.count_csrf = 0


    # Lay form trong  source page tuong ung voi url
    def extract_forms(self, url, cookie):

        response = self.session.get(url, cookies=cookie)
       
        parsed_html = BeautifulSoup(response.content, 'html.parser')
        return parsed_html.findAll("form")

    def shannon_entropy(self, data):
        if not data:
            return 0

        entropy = 0

        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += - p_x * log(p_x, 2)

        return entropy

    # kiem tra xem co phai csrf_token hay khong
    def is_csrf_token(self, key, value):
        min_length = 5      # ngan nhat la 5 
        max_length = 512    # max length 512
        #min_entropy = 2.4   # ??? biet chet lien

        # Check length
        if len(value) <= min_length:
            return False

        if len(value) > max_length:
            return False

        if not re.match('^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$', value):
            return False

        # Check for common CSRF token names
        for common_csrf_name in COMMON_CSRF_NAMES:
            if common_csrf_name.lower() in key.lower():
                return True
        '''
        # Calculate entropy
        entropy = self.shannon_entropy(value)
        if entropy >= min_entropy:
            return True
        '''
        return False

    def rand_str_generator(self, size=4, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    def is_resp_equal(self, resp1, resp2):
        if resp1.status_code != resp2.status_code:
            return False
        if str(resp1.content) != str(resp2.content):    
            return False
        return True
    

    
    def is_token_checked(self, post_url, method, post_data, csrf_token_key, csrf_token, cookie):
        modified_data = post_data
        modified_data[csrf_token_key] = csrf_token.replace(csrf_token[0:4], self.rand_str_generator())

        if method == "post" or method == "POST":
            original_response = self.session.post(post_url, data=post_data, cookies = cookie)
            modified_response = self.session.post(post_url, data=modified_data, cookies = cookie)
            result = self.is_resp_equal(original_response, modified_response)
            return not result
        else:
            original_response = self.session.get(post_url, params=post_data, cookies = cookie)
            modified_response = self.session.get(post_url, params=modified_data, cookies = cookie)
            #result = self.is_resp_equal(original_response, modified_response)
        return not result
    

    def scan(self, link, cookie):
        forms = self.extract_forms(link, cookie)
        count = 0
        for form in forms:
            csrf_token_key = ""
            csrf_token = ""
            action = form.get("action")
            post_url = urljoin(link, action)
            method = form.get("method")
            post_data = {}
            inputs_list = form.findAll('input') # lay tat ca input tag
            for inputs in inputs_list:
                name = inputs.get('name') #lay input name
                value = inputs.get('value') # lay input value
                input_type = inputs.get('type') # lay input type
                if input_type == 'password': # kiem tra xem co phai feild password hay khong
                    value = self.password # dien password cua minh vao
                post_data[name] = value # hop nhat du lieu post $x=yy
                if name is not None and value is not None and input_type != 'submit' and self.is_csrf_token(name,
                                                                                                            value):
                # kiem tra xem co phai csrf token hay khong
                    csrf_token_key = name # lay ten token
                    csrf_token = value # lay gia tri tonken
            if csrf_token_key != "":
                #self.logger.info("\n[+] CSRF token found; Checking if token is verified")
                if not self.is_token_checked(post_url, method, post_data, csrf_token_key, csrf_token, cookie):
                    count += 1
                    print(Fore.RED + "\nCSRF " + link)
                    #self.logger.info("\n[***] The following form in the link " + link + " is vulnerable to CSRF "
                    #                                                                    "because token is not "
                    #                                                                    "verified. Security "
                    #                                                                    " Risk: High")
                    print(form)
                    #self.logger.info(form)
            else:
                count += 1
                print(
                    Fore.RED + "\nCSRF " + link )
                #self.logger.info("\n[***] The following form in the Link " + link + "is vulnerable to CSRF; Lack of "
                #                                                                    "csrf_token. "
                #                                                                    "Security Risk: High")
                print(form)
                #self.logger.info(form)
            if method == 'GET':
                count += 1
                print(
                    Fore.RED + "\nCSRF " + link )
                #self.logger.info("\n[***] The following form in the link " + link + "is vulnerable to CSRF due to GET "
                #                                                                    "Request "
                #                                                                    "method. Security Risk: Low")
                print(form)
                #self.logger.info(form)
        if count == 0:
            print('\n[+] The '+link+' is not vulnerable to CSRF.\n')
            #self.logger.info('\n[+] The link is not vulnerable to CSRF.\n')
        else:
            self.count_csrf += count
    
'''
cookie = {"PHPSESSID" : "ffb679932bb7620c0209b773e6916a1c", "security": "low"} 
x = Csrf_Scanner('asd','asd','asd')
x.run_csrf_test("http://localhost/dvwa/vulnerabilities/csrf/" , cookie)
'''