class connect:
    param = []
    # this function will build content for post request
    def build_content(self, params, payload):
        i = 0
        content = "{"
        for param in params:
            content = content + "\""+param + "\":\""+ payload+"\""
            if i < len(params)-1:
                content = content + ","
            i = i + 1
        content = content + "}"
        return content

    #the function below will build url for get request
    def build_url(self, url, payload):
        from urllib.parse import urlparse, quote
        url = urlparse(url)
        for i in url.query.split("&"):
            self.param.append(i.split("=")[0])
        url = url.scheme + "://" + url.netloc + url.path + "?"
        i = 0
        if len(self.param) > 0: 
            for p in self.param:
                url = url + p + "=" + quote(payload)
                if i != len(self.param)-1: 
                    url = url + "&"
                    i = i + 1
        return url

    def normal_GET(self, url, payload, cookie):
        from requests_html import HTMLSession
        import pyppdf.patch_pyppeteer
        session = HTMLSession()
        url  = self.build_url(url, payload)

        #old function  get() khong auto redirect
        '''
        resp = session.get(url) 
        '''
        
        # new function
        resp = session.request("GET", url=url, cookies=cookie)
        return resp
        
    def normal_POST(self, url, params, payload, cookie):
        from requests_html import HTMLSession
        content = self.build_content(params, payload)
        session = HTMLSession()

        #old function
        '''
        resp = session.post( url, data = content)
        '''

        #new function
        resp = session.request("POST", "url", cookies=cookie, data=content)
        return resp.render()


    def render_GET(self,url, payload, cookie):
        resp = self.normal_GET( url, payload, cookie)
        #resp.html.render()
        return resp
