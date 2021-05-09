from crawler import crawler
from sqlDectect import sqlDetect


cookie = {"PHPSESSID" : "hnjcqd3len458svhn70014ojfi", "security": "low"} 

a = sqlDetect()
c = crawler('http://192.168.1.125/dvwa/',[], cookie)

forms = c.run_crawler()
for i in forms:
    a.unionDetect(i[0],i[1],i[2],cookie)