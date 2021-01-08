import sys
import urllib
import urllib.request as urllib1


fullurl = input("Url: ")
errormsg = ["You have an error in your SQL syntax", "Warning: mysql_fetch_array()"]
f = open("payload", "r")
errorr = "yes"

for payload in f:
    resp = urllib1.urlopen(fullurl + urllib.parse.quote_plus(payload))
    body = resp.read()
    fullbody = body.decode('utf-8')

    for error in errormsg:
        if error in fullbody:
            if errorr == "no":
                print ("[-] That payload might not work!")
                errorr = "yes"
            else:
                print ("[+] The website is SQL injection vulnerable! Payload: " + payload)

f.close()