from bs4 import BeautifulSoup
import requests
import random
import time
from lxml.html import fromstring
from itertools import cycle
import traceback

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def header_rotate():
    for i in range(1, 10):
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        return headers


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def scrape():
    jobs = []
    i = 0
    for page in range(0, 10):
        page = page + 1
        base_url = 'https://boss.az/vacancies?action=index&controller=vacancies&only_path=true&page=' + str(page) + '&type=vacancies'
        source_code = requests.get(base_url, headers=header_rotate())
        r = source_code.text
        soup = BeautifulSoup(r, "html.parser")
        all_product = soup.find_all('div', class_="results-i")
        for item in all_product:
            # if i == 3:
            #     break
            # i = i + 1
            d = {}
            title = item.find("h3", {"class": "results-i-title"})
            d['title'] = title.text
            salary = item.find('div', {'class': 'results-i-salary salary'})
            d['salary'] = salary.text
            company = item.find('a', {'class': 'results-i-company'}, href=True)
            d['company'] = company.text
            d['company_url'] = 'https://boss.az'+str(company.get('href'))
            url = item.find('a', {'class': 'results-i-link'}, href=True)
            d['link'] = 'https://boss.az'+str(url.get('href'))
            link = str(url.get('href'))
            vac_link = link.split('/')
            vac_link.reverse()
            d['vac_id'] = vac_link[0]
            jobs.append(d)
    return jobs


def vacancies():
    jobs = scrape()
    vacancies = []
    for job in jobs:
        d = {}
        base_url = job['link']
        source_code = requests.get(base_url, headers=header_rotate())
        r = source_code.text
        soup = BeautifulSoup(r, "html.parser")
        all = soup.find_all('div', class_="main")
        for item in all:
            title = item.find('h1', {'class': 'post-title'})
            d['title'] = title.text if title else None
            salary = item.find('span', {'class': 'post-salary salary'})
            d['salary'] = salary.text if salary else None
            region = item.find('div', {'class':'region params-i-val'})
            d['region'] = region.text if region else None
            age = item.find('div', {'class': 'age params-i-val'})
            d['age'] = age.text if age else None
            education = item.find('div', {'class': 'education params-i-val'})
            d['education'] = education.text if education else None
            experience = item.find('div', {'class': 'experience params-i-val'})
            d['experience'] = experience.text if experience else None
            bumped_on = item.find('div', {'class': 'bumped_on params-i-val'})
            d['bumped_on'] = bumped_on.text
            expires_on = item.find('div', {'class': 'expires_on params-i-val'})
            d['expires_on'] = expires_on.text
            information = item.find('dd', {'class': 'job_description params-i-val'})
            d['information'] = information.text
            requirements = item.find('dd', {'class': 'requirements params-i-val'})
            d['requirements'] = requirements.text
            d['vac_id'] = job['vac_id']
            d['company'] = job['company']
            email = item.find('div', {'class': 'email params-i-val'})
            a_email = email.find('a', href=True)
            code_mail = str(a_email.get('href'))
            mail = code_mail.split('#')
            d['email'] = cfDecodeEmail(mail[1])
            vacancies.append(d)
    return vacancies


proxies = get_proxies()
proxy_pool = cycle(proxies)


def ejobSource(base_url):
    try:
        proxy = next(proxy_pool)
        source_code = requests.get(base_url, headers=header_rotate(), proxies={"http": proxy, "https": proxy})
        r = source_code.text
        soup = BeautifulSoup(r, 'html.parser')
        all_product = soup.find_all('table', {"style": "width:800px; margin-bottom:2px;"})
        return all_product
    except:
        print('proxy error')
        ejobSource(base_url)


def ejobScrape():
    jobs = []
    for page in range(0, 2):
        proxy = next(proxy_pool)
        page = page + 1
        base_url = 'https://ejob.az/is-tap/page-' + str(page) + '/'
        all_product = ejobSource(base_url)
        if all_product != None:
            for item in all_product:
                d = {}
                title = item.find('h3', {'class': 'position'})
                d['title'] = title.text
                url = title.find_all('a', href=True)
                d['url'] = 'https://ejob.az' + str(url[0].get('href'))
                id = d['url'].split('/')[4]
                id = id.split('-')[0]
                d['id'] = id
                jobs.append(d)
    return jobs


def jobScrape():
    jobs = []
    for page in range(0, 5):
        page = page + 1
        base_url = 'http://jobustan.com/job-search?salary_rang_min=&salary_rang_max=&perPage=' + str(page)
        source_code = requests.get(base_url, headers=header_rotate())
        r = source_code.text
        soup = BeautifulSoup(r, 'html.parser')
        all_product = soup.find_all('div', {"class": "jobs-card__text"})
        for item in all_product:
            d = {}
            title = item.find('div', {'class': 'jobs-card__jobsName'})
            d['title'] = title.text
            jobs.append(d)
    return jobs


def ejobVacancies():
    jobs = ejobScrape()
    vacancies = []
    for job in jobs:
        proxy = next(proxy_pool)
        d = {}
        base_url = job['url']
        source_code = requests.get(base_url, headers=header_rotate(), proxies={"http": proxy, "https": proxy})
        r = source_code.text
        soup = BeautifulSoup(r, "html.parser")
        all = soup.find_all('table', {"style":"width:1250px; margin:0 auto;"})
        for item in all:
            title = item.find('h1', {'class': 'position'})
            d['title'] = title.text
            d['vac_id'] = job['id']
            email = item.find('a', {'style': 'color:#000'})
            d['email'] = email.text if email else None
            vacancies.append(d)
    return vacancies


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

