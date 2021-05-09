from a1 import x, xssPayload

a= x()
a.xx()
'''
a= xssPayload()
cookie = {"PHPSESSID" : "f2c280e624310d43cafd4cebf90a1768", "security": "low"}
urls = ["http://localhost/dvwa/vulnerabilities/xss_r/", "http://localhost/dvwa/vulnerabilities/xss_d/"]

a.test_threading("http://localhost/dvwa/vulnerabilities/xss_r/", ["name"],cookie, "get")

'''