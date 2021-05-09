class connect:
    def __init__(self):

        self.param = []
    # this function will build content for post request
    def build_content(self, params, payload):
        i = 0
        
        submit = "submit"
        content = "{"
        for param in params:
            if param == None:
                continue
            elif param == "Submit":
                content = content + "\""+param + "\":\""+ submit+"\""
            else:
                content = content + "\""+param + "\":\""+ payload+"\""
            if i < len(params)-1:
                content = content + ","
            i = i + 1
        content = content + "}"
        
        return content

    def build_content1(self, params, payload):
        i = 0
        
        submit = "submit"
        content = {}
        for param in params:
            if param == None:
                continue
            elif param == "Submit":
                content[param] = "submit"
            else:
                content[param] = payload
    
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
                if p.lower() == "Submit":
                    url = url + str(p) + "=submit"
                else:
                    url = url + p + "=" + quote(payload)
                if i != len(self.param)-1: 
                    url = url + "&"
                    i = i + 1
        return url

    def build_url_1(self, url, path , payload, params):
        from urllib.parse import quote
        if "?" in url:
            pass
        else:
            if path  == None or path == "#":
                url = url + "?"
            else:
                url = url + path + "?"
        i = 0
        if len(params) > 0: 
            for p in params:
                if p == None:
                    continue
                if p.lower() == "submit":
                    url = url + str(p) + "=submit"
                else:
                    url = url + str(p) + "=" + quote(payload)
                if i != len(params)-1 and params[i+1] != None: 
                    url = url + "&"
                    i = i + 1
        return url


    def normal_POST(self, url, params, payload, cookie):
        from requests_html import HTMLSession
        content = self.build_content1(params, payload)
        session = HTMLSession()

        #old function
        '''
        resp = session.post( url, data = content)
        '''

        #new function
        resp = session.post(url=url, cookies=cookie, data=content)
        resp.html.render(timeout=1000)
        session.close()
        return resp

    def normal_GET(self, url, params, payload, cookie):
        url = self.build_url_1(url,"", payload, params)
        from requests_html import HTMLSession
        session = HTMLSession()
        resp_page = session.get( url=url, cookies=cookie)
        resp_page.html.render(timeout=1000)
        session.close()
        return resp_page


    def render_GET(self,url, params, payload, cookie):
        resp = self.normal_GET( url, params, payload, cookie)
        #resp.html.render()
        return resp
