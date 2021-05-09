from requests_html import AsyncHTMLSession

'''
asession = AsyncHTMLSession()
async def get_pythonorg(url):
    r = await asession.get(url,cookies={"PHPSESSID":"f2c280e624310d43cafd4cebf90a1768", "security":"low"})
    return r

async def get_reddit():
    r = await asession.get('https://reddit.com/')
    return r

async def get_google():
    r = await asession.get('https://google.com/')
    return r

results = asession.run( lambda: get_pythonorg('http://localhost/dvwa/vulnerabilities/xss_r/?name=nguyenanh'))
for result in results:
    print(result.content)


async def get_reddit(url):
    asession = AsyncHTMLSession()
    r = await asession.get(url)
    await r.html.arender()
    resp=r.html.raw_html
    print(resp)

get_reddit('http://localhost/dvwa/vulnerabilities/xss_r/?name=nguyenanh')
'''


from multiprocessing import Pool
from requests_html import HTMLSession

links = ["https://localhost/dvwa/vulnerabilities/xss_r/?name=a", "https://localhost/dvwa/vulnerabilities/xss_d/?name=a"]
n = 5
batch = [links[i:i+n] for i in range(0, len(links), n)]


def link_processor(batch_link):
    session = AsyncHTMLSession()
    results = []

    for l in batch_link:
        print(l)
        r = session.get(l)
        r.html.arender()
        tmp_next = r.html.xpath('//a[contains(@href, "/matches/")]')

    return tmp_next


pool = Pool(processes=3)
output = pool.map(link_processor, batch[:2])
pool.close()
pool.join()
print(output)