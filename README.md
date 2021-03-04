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
