from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re

base = "https://en.wikipedia.org"

links = ["https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_2xx_(Europe)",
        "https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_3xx_(North_America)",
        "https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_4xx_(Asia)",
        "https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_5xx_(Oceania)",
        "https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_6xx_(Africa)",
        "https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_7xx_(South_America)",
        "https://en.wikipedia.org/wiki/Mobile_country_code"]

#get the sub-table of country given
def get_table(col, html):
    c = col.find('a')
    country = c.get_text()
    head = html.find('a', title = country)
    if head == None :
        country = read_head(col)
        head = html.find('a', title = country)
        if head == None:
            head = html.find('a', string = country)
    table = head.find_next('table')
    return (table)

def get_soups():
    soups = []
    for link in links:
        page = urlopen(link)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        soup.prettify()
        soups.append(soup)
    return soups

def get_soup(url):
    page = urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html,"html.parser")
    return soup

def read_head(ht):
    a = ht.find('a')
    link = base + a['href']
    html = urlopen(link).read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser') 
    head = soup.find('h1')
    return head.text.strip()

def get_ind(code):
    code = int(code)
    if code>=200 and code<300:
        c = 0
    elif code>=300 and code<400:
        c = 1
    elif code>=400 and code<500:
        c = 2
    elif code>=500 and code<600:
        c = 3
    elif code>=600 and code<700:
        c = 4
    elif code>=700 and code<800:
        c = 5
    else:
        c = 6
    return c

def get_t(ln):
    if ln.a == None :
        net = ln.text.strip()
    else:
        a = ln.find('a')
        net = a.get_text()
    return net

def to_df(df, mcc,mnc,iso,dest,op_name,net_name,status):
    dict = {'MCC':[mcc], 'MNC':[mnc], 'alpha-2':[iso], 
            'destination':[dest], 'operator_name':[op_name], 
            'network_name':[net_name], 'status':[status]}
    df2 = pd.DataFrame.from_dict(dict)
    df = pd.concat([df,df2],ignore_index=True)
    return df

#given url the base url
def bullet_link(url):
    u = []
    soup = get_soup(url)

    head = soup.find('strong',string = 'Operational Bulletin')
    table = head.find_next('table')
    for bullet in table.find_all('tr'):
        col = bullet.find_all('td')
        a = col[1].find('a',href= True)
        link = a['href'].strip()
        new_url = url +'/'+ link

        u.append(new_url)
    return u

def year_link(url):
    y = []
    soup = get_soup(url)
    head = soup.find('strong',string = 'Operational Bulletin')
    temp = head.find_next('font')
    year = temp.find_previous()
    for row in year.find_all('a',href=True):
        link = row['href'].strip()
        temp = url +'/'+ link
        y.append(temp)
    return y

def mnc_exist(url):
    soup = get_soup(url)
    mnc = soup.find(string = re.compile(r"MNC"))
    if mnc != None:
        return True
    else: return False