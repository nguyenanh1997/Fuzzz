import string
import random
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from math import log
from w3af.core.controllers.misc.fuzzy_string_cmp import fuzzy_equal
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
        self.session = session
        self.password = password
        self.logger = logger
        self.count_csrf = 0

    def extract_csrf_token_meta(self, url):
        from requests_html import HTTPSession
        from bs4 import BeautifulSoup
        token = {}
        base_url = url
        requests = HTMLSession()
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text)

        # tim csrf token trong meta tag <meta>
        for meta_tag in soup.find_all("meta"):
            if meta_tag['name'] in COMMON_CSRF_NAMES or "csrf" in meta_tag["name"]:
                token[meta_tag['name']] = meta_tag['content']
        return token


    def extract_forms(self, url):
        from requests_html import HTTPSession
        try:
            self.session = HTMLSession()
            response = self.session.get(url)
        except requests.exceptions.ConnectionError:
            print(Fore.RED + '[***] Could not connect to the application. Check the Internet connection and'
                             ' Target Application status')
            self.logger.error('[***] Could not connect to the application. Check the Internet connection and'
                              ' Target Application status')
            exit()
        except requests.exceptions.InvalidSchema:
            print(Fore.RED + '[***] Error in the format of the provided URL')
            self.logger.error('[***] Error in the format of the provided URL')
            exit()
        parsed_html = BeautifulSoup(response.content, 'html.parser')
        return parsed_html.findAll("form")

'''
    def shannon_entropy(self, data):
        if not data:
            return 0

        entropy = 0

        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += - p_x * log(p_x, 2)

        return entropy

'''
    def is_csrf_token(self, key, value):
        min_length = 5
        max_length = 512
        min_entropy = 2.4

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

        # Calculate entropy
        '''
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
        if str(resp1.content) != str(resp2.content): #not fuzzy_equal(str(resp1.content), str(resp2.content), 1.0):
            return False
        return True

    #

    # kiem tra xem token co duoc check không.  Ham nay chi kiem tra xem csrf token nay co duoc verify hay khong
    def is_token_checked(self, post_url, method, post_data, csrf_token_key, csrf_token):
        modified_data = post_data
        modified_data[csrf_token_key] = csrf_token.replace(csrf_token[0:4], self.rand_str_generator()) #  random ra token moi
        try:
            if method == "post": # thuc hien post 
                original_response = self.session.post(post_url, data=post_data)    #response voi trust data
                modified_response = self.session.post(post_url, data=modified_data)# response voi fake data
                result = self.is_resp_equal(original_response, modified_response)  # kiem tra xem 2 request co giong nhau hay khong? 
                return not result
            else:
                original_response = self.session.get(post_url, params=post_data)   # Tuowng tu nhu tren 
                modified_response = self.session.get(post_url, params=modified_data)
                result = self.is_resp_equal(original_response, modified_response)
                return not result
        except requests.exceptions.ConnectionError:
            print(Fore.RED + '[***] Could not connect to the application. Check the Internet connection and'
                             ' Target Application status')
            self.logger.error('[***] Could not connect to the application. Check the Internet connection and'
                              ' Target Application status')
            exit()
        except requests.exceptions.InvalidSchema:
            print(Fore.RED + '[***] Error in the format of the provided URL')
            self.logger.error('[***] Error in the format of the provided URL')
            exit()

    def run_csrf_test(self, link):

        print('\n[+] Testing forms in the link ' + link + ' for CSRF\n')
        forms = self.extract_forms(link)
        count = 0
        for form in forms:
            csrf_token_key_in_form = ""
            csrf_token = ""
            action = form.get("action")
            post_url = urljoin(link, action)
            method = form.get("method")
            post_data = {}
            inputs_list = form.findAll('input')
            for inputs in inputs_list:
                name = inputs.get('name')
                value = inputs.get('value')
                input_type = inputs.get('type')
                if input_type == 'password':
                    value = self.password
                post_data[name] = value

'''
Chi thuc hien kiem tra xem csrf token co duoc verify chinh xac hay khong
Phai bo sung them chuc nang csrf token co duoc dung lai hay khong.
'''
                if name is not None and value is not None and input_type != 'submit' and self.is_csrf_token(name,
                                                                                                            value):
                    csrf_token_key_in_form = name
                    csrf_token = value

            if csrf_token_key_in_form != "": # kiem tra xem csrf token co ton tai hay khong
                print(Fore.RED + "\n[+] CSRF token found; Checking if token is verified")
                self.logger.info("\n[+] CSRF token found; Checking if token is verified")
                if not self.is_token_checked(post_url, method, post_data, csrf_token_key, csrf_token): # chi cgecj xem csrf token co verify hay khong
                    count += 1
                    print(Fore.RED + "\n[***] The following form in the link " + link + " is vulnerable to CSRF "
                                                                                        "because token is not "
                                                                                        "verified. Security "
                                                                                        " Risk: High")
                    self.logger.info("\n[***] The following form in the link " + link + " is vulnerable to CSRF "
                                                                                        "because token is not "
                                                                                        "verified. Security "
                                                                                        " Risk: High")
                    print(form)
                    self.logger.info(form)
            else:
                csrf_token_key_in_meta = self.extract_csrf_token_meta(url)
                if csrf_token_key_in_meta['name'] != "":
                    csrf_token = csrf_token_key_in_meta['content']
                    if not self.is_token_checked(post_url, method, post_data, csrf_token_key, csrf_token): # chi cgecj xem csrf token co verify hay khong
                    count += 1
                    print(Fore.RED + "\n[***] The following form in the link " + link + " is vulnerable to CSRF "
                                                                                        "because token is not "
                                                                                        "verified. Security "
                                                                                        " Risk: High")
                    self.logger.info("\n[***] The following form in the link " + link + " is vulnerable to CSRF "
                                                                                        "because token is not "
                                                                                        "verified. Security "
                                                                                        " Risk: High")
                    print(form)
                    self.logger.info(form)


                else: # truong hop csrf token khong ton tai
                    count += 1
                    print(
                        Fore.RED + "\n[***] The following form in the Link " + link + "is vulnerable to CSRF; Lack of "
                                                                                    "csrf_token. "
                                                                                    "Security Risk: High")
                    self.logger.info("\n[***] The following form in the Link " + link + "is vulnerable to CSRF; Lack of "
                                                                                        "csrf_token. "
                                                                                        "Security Risk: High")
                    print(form)
                    self.logger.info(form)
                if method == 'GET': # neu method la get thi 
                    count += 1
                    print(
                        Fore.RED + "\n[***] The following form in the link " + link + "is vulnerable to CSRF due to GET "
                                                                                    "Request "
                                                                                    "method. Security Risk: Low")
                    self.logger.info("\n[***] The following form in the link " + link + "is vulnerable to CSRF due to GET "
                                                                                        "Request "
                                                                                        "method. Security Risk: Low")
                    print(form)
                    self.logger.info(form)
        if count == 0:
            print('\n[+] The link is not vulnerable to CSRF.\n')
            self.logger.info('\n[+] The link is not vulnerable to CSRF.\n')
        else:
            self.count_csrf += count



'''
Bo sung them su dung lại token cũ
'''