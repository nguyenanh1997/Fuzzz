class connect:
    def normal_GET(self, url, param, payload):
        from requests_html import HTMLSession
        import pyppdf.patch_pyppeteer
        session = HTMLSession()

        resp = session.get(url + "?" + param + "=" + payload)

        return resp
        
    def normal_POST(self, url='http://testphp.vulnweb.com/search.php', param, payload):
        from requests_html import HTMLSession
        
        session = HTMLSession()
        resp = session.post( url, data = {param : payload})
        return resp


    def render_GET(self,  url, param, payload):
        resp = self.normal_GET( url, param, payload)
        resp.html.render()
        return resp

a = connect()
print(a.render_GET('http://gamek.vn').text)
