'''
làm menu thôi nào ngưòi anh em thiện lành.
'''
from crawler import crawler
from LFI import lfi
from csrf_scanner import Csrf_Scanner
from sqlDectect import sqlDetect
from xssDetect import xssPayload
from OScmd import cmd
import json
import random
import time

def parseCookie():
    url = input("Enter url (http://domain.com)")
    params = list(input("enter params(x,y,z,...): ").split(","))
    method = input("method:(get or post): ")
    cookies = None
    #cookieJson = '{'
    cookiesInput     = list(input("Enter cookie cookie1:value1, cookie2:value2: ").split(","))
    cookieJson = {}
    for i in cookiesInput:
        name, value = i.split(":")
        cookieJson[name] = value
    '''
    for cookie in cookiesInput:
        cookie = list(cookie.split(':'))
        cookieJson += '"'+cookie[0]+'":"'+cookie[1]+'"'
    # cookiex:cookieValue
    cookieJson = cookieJson + '}'

    cookies = json.dumps(cookieJson)
    '''
    return url, cookieJson


def runScan():

    url, cookie = parseCookie()

    password = input("enter your password use in this site: ")



    crawl = crawler(url, [] ,cookie)
    listedCrawl = crawl.run_crawler()
    
    
    for link in listedCrawl:
        '''
        a = xssPayload()
        #url, params, cookie, method
        a.scan(link[0], link[2], cookie, link[1])
        '''
        a = xssPayload()
        a.scan(link[0], link[2], cookie, link[1])
        time.sleep(2)

        '''
        b = sqlDetect()                                  # sqli
        #url, method, params, cookie
        b.boleanDetect(link[0], link[1],link[2], cookie)
        b.unionDetect(link[0], link[1],link[2], cookie)
        '''
        b = sqlDetect()                                  # sqli
        #url, method, params, cookie
        b.boleanDetect(link[0], link[1],link[2], cookie)
        b.unionDetect(link[0], link[1],link[2], cookie)
        time.sleep(2)

        '''
        c = lfi()                                        #lfi
        payloads = c.linux_lfi()
        x= 0
        for payload in payloads:
            x = x+1
            #url, method, params, payload, cookie
            c.scanner(link[0], link[1], link[2], payload, cookie)
            if x == 9: 
                break
            scan(self,  url, method, params, cookie):
        '''
        c = lfi() 
        c.scan(link[0], link[1], link[2], cookie)
        time.sleep(2)
        
        '''
        x = Csrf_Scanner('', password, '')            #csrf
        # link, cookie
        x.run_csrf_test(link[0], cookie)
        '''
        x = Csrf_Scanner('', password, '')  
        x.scan(link[0], cookie)
        time.sleep(2)
        '''
        g = cmd()
        g.scan(link[0], link[1], link[2], cookie)
        '''
        g = cmd()
        g.scan(link[0], link[1], link[2], cookie)
        time.sleep(2)


        
def crawl(url, cookies):
    
    c = crawler(url, [], cookies)
    listedCrawl = c.run_crawler()
    return listedCrawl


def xss(url, params, cookies, method):
    #url, params, method, cookie = parseCookie()
    
    a = xssPayload()

    a.scan(url, params, cookies, method) 

def sqli(url, params, cookies, method):
    #url, params, method, cookie = parseCookie()
    
    a = sqlDetect()
    a.boleanDetect(url, params, cookies, method)
    a.unionDetect(url, params, cookies, method)


def lfi1(url, params, cookies, method):
    #url, params, method, cookie = parseCookie()
    
    a = lfi()
    a.scan(url, method, params, cookies)


def csrf(url, cookies, password):
    
    #url, params, method, cookie = parseCookie()

    x = Csrf_Scanner('', password, '')
    #x.run_csrf_test(url, cookies)


def oscommand(url, params, cookies, method):
    
    #url, params, method, cookie = parseCookie()
    a = cmd()
    payloads = a.result_base_generator()
    payloads.update(a.another_command())
    payloads.update(a.time_base_generator)
    for payload in payloads:
        a.scanner_oscmd(url, method, params, cookies, payload)



def menu():
    while 1:
        print("------Scanner for SQLi, XSS, LFI, CSRF, OS command injection------")
        print("---------------------Author: Nguyen Anh---------------------------")
        print("------------------------------------------------------------------")
        print("1. Scan web.")
        print("2. Crawler module.")
        print("3. SQLi module.")
        print("4. XSS module.")
        print("5. CSRF module.")
        print("6. LFI module.")
        print("7. Os command injection module.")
        print("8. exit() ")
        choice = str(input("enter your chose: "))
        if choice == "exit()" or choice == "exit" or choice == "Exit()" or choice == "Exit":
            print("Thank for use!")
            return 0
        if choice == "1": 
            print("Chose Scanner web.")
            runScan()
            return 0
        '''
        if choice == "2":
            print("Chose Scawler module.")
            crawl()
        if choice == "3":
            print("Chose SQLi module.")
            sqli()
        if choice == "4":
            print("Chose XSS module.")
            xss()
        if choice == "5":
            print("Chose CSRF module.")
            csrf()
        if choice == "6":
            print("Chose LFI module.")
            lfi1()
        if choice == "7":
            print("Chose Os command injection module.")
            oscommand()
        '''


menu()