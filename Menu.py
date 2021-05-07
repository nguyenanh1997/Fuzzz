'''
làm menu thôi nào ngưòi anh em thiện lành.
'''
from crawler import crawler
from LFI import lfi
from csrf import csrf
from sqlDectect import sqlDetect
from xssPayload import xssPayload
from OScmd import cmd
import json

def parseCookie():
    cookieJson = "{"
    cookiesInput     = list(input("Enter cookie cookie1:value1, cookie2:value2: ").split(","))
    for cookie in cookiesInput:
        cookie = list(cookie.split(":"))
        cookieJson = "'"+cookie[0]+"':'"+cookie[1]+"', "
    # cookiex:cookieValue
    cookies = cookieJson + "}"
    cookies = json.dump(cookiesInput)
    return cookies


def runScan(listedCrawl):
    '''
    Chay scan thoai.
    '''

def scan():
    url = input("Enter url (http://domain.com)")
    cookies = parseCookie()
    crawl = crawler(url, cookies)
    listedCrawl = crawl.run_crawler()
    runScan(listedCrawl)

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
        choice = input("enter your chose: ")
        if choice == "exit()" or choice == "exit" or choice == "Exit()" or choice == "Exit":
            print("Thank for use!")
            return 0
        if choice == "1": 
            print("Chose Scanner web.")
        if choice == "2":
            print("Chose Scawler module.")
        if choice == "3":
            print("Chose SQLi module.")
        if choice == "4":
            print("Chose XSS module.")
        if choice == "5":
            print("Chose CSRF module.")
        if choice == "6":
            print("Chose LFI module.")
        if choice == "7":
            print("Chose Os command injection module.")


def main():

