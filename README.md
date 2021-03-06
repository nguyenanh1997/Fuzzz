# Fuzzz


CSRF: Cách làm 
1. check csrf token có tồn tại hay không? Trong cookies, header response, html page
2. check cookies samesite? 

1+2 ---->>> CSRF
1+1.5(samesite bật trong 1 cookie) -----> propaly occur csrf attack


Nhiệm vụ
Trong Crawler.py 
     - Bổ sung thêm hàm check csrf token trong source page
		 - Bổ sung thêm hàm check csrf token trong cookies(kiểm tra luôn samesite)
		 - Bổ sung thêm hàm check csrf token trong header response 
     - Tạo hafm kểm tra xem csrf token có được verified hay không.
     - 

X-Requested-By
X-Requested-With
X-XSRF-TOKEN 
X-CSRF-TOKEN 
CSRF-TOKEN 
XSRF-TOKEN 
Authorization 
Origin

csrf_params_names = [  # Parameters that may contain CSRF tokens
    "csrf",
    "xsrf",
    "token",
    "auth",
    "secret"
]


https://github.com/ManojMelli/Web-Vulnerability-Scanner-VULCAN-/blob/master/csrf_scanner.py
