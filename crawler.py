import logging
import csv
from selenium import webdriver
from urllib.parse import urldefrag, urljoin, urlsplit, parse_qs
from bs4 import BeautifulSoup
import platform
from os import getcwd   
from selenium import webdriver
from collections import deque 

class SeleniumCrawler(object):
 
    def __init__(self, base_url, exclusion_list, output_file='example.csv', start_url=None):
        
        assert isinstance(exclusion_list, list), 'Exclusion list - needs to be a list'

        
        self.browser = webdriver.PhantomJS(executable_path="phantomjs/bin/phantomjs")

        self.formList = []
        self.linkList = []
        self.base = base_url
 
        self.start = start_url if start_url else base_url  #If no start URL is passed use the base_url
 
        self.exclusions = exclusion_list  #List of URL patterns we want to exclude
 
        self.crawled_urls = []  #List to keep track of URLs we have already visited
 
        self.url_queue = deque([self.start])  #Add the start URL to our list of URLs to crawl
 
        self.output_file = output_file
    
    def get_page(self, url):
        try:
            self.browser.get(url)
            return self.browser.page_source
        except Exception as e:
            logging.exception(e)
            return
    def get_soup(self, html):
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            return


    def get_links(self, soup):
        for link in soup.find_all('a', href=True): #All links which have a href element
            link = link['href'] #The actually href element of the link
            if any(e in link for e in self.exclusions): #Check if the link matches our exclusion list
                continue #If it does we do not proceed with the link
            url = urljoin(self.base, urldefrag(link)[0]) #Resolve relative links using base and urldefrag
            if url not in self.url_queue and url not in self.crawled_urls: #Check if link is in queue or already crawled
                if url.startswith(self.base): #If the URL belongs to the same domain
                    self.url_queue.append(url) #Add the URL to our queue

    def get_formList(self):
        return self.formList

    def get_linkList(self):
        for url in self.crawled_urls:
            link = []
            link.append(url)
            link.append('get')
            query = urlsplit(url).query
            params = parse_qs(query)
            for x,y in params:
                link.append(x)
                
                

    def get_form(self, soup, url):
        forms = list()
        for form in soup.find_all('form'): #All links which have a href element
            form1 = []
            params = []
            action = form.get("action")
            method = form.get("method")
            inputs = form.findAll('input')  
            for input in inputs:
                param = input.get('name')
                params.append(param)

            form1.append(action)
            form1.append(method)
            form1.append(params)
            forms.append(form1)
        return forms

    def get_data(self, soup):
        try:
            title = soup.find('title').get_text().strip().replace('\n','')
        except:
            title = None

        return title

    def csv_output_link(self, url, title):

        with open(self.output_file, 'a', encoding='utf-8') as outputfile:

            writer = csv.writer(outputfile)
            writer.writerow([url])
            writer.writerow([title])

    def csv_output_form(self, url, title):

        with open(self.output_file, 'a', encoding='utf-8') as outputfile:

            writer = csv.writer(outputfile)
            writer.writerow([url])
            writer.writerow([title])        

    def run_crawler(self):
        linklist = []
        
        while len(self.url_queue): #If we have URLs to crawl - we crawl
            current_url = self.url_queue.popleft() #We grab a URL from the left of the list
            self.crawled_urls.append(current_url) #We then add this URL to our crawled list
            html = self.get_page(current_url) 
            if self.browser.current_url != current_url: #If the end URL is different from requested URL - add URL to crawled list
                self.crawled_urls.append(current_url)
            soup = self.get_soup(html)
            if soup is not None:  #If we have soup - parse and write to our csv file
                check = 0
                self.get_links(soup)
                title = self.get_data(soup)
                returnFrom = self.get_form(soup, current_url)
                for i in returnFrom:
                    if i in self.formList:
                        pass
                    else:
                        self.formList.append(i)
                        
                linklist.append(current_url)
        print(self.formList)    

    def test_crawler_form(self):
        while len(self.url_queue): #If we have URLs to crawl - we crawl
            current_url = self.url_queue.popleft() #We grab a URL from the left of the list
            self.crawled_urls.append(current_url) #We then add this URL to our crawled list
            html = self.get_page(current_url) 
            if self.browser.current_url != current_url: #If the end URL is different from requested URL - add URL to crawled list
                self.crawled_urls.append(current_url)
            soup = self.get_soup(html)
            if soup is not None:  #If we have soup - parse and write to our csv file
                self.get_form(soup, current_url)


a = SeleniumCrawler('http://testphp.vulnweb.com',[])
a.run_crawler()