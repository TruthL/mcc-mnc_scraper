#functions used for downloading of bulletins

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import pandas as pd
import func
import re
import os


def bullet_link(url,flag):
    base = "https://www.itu.int/"
    add = "en/publications/ITU-T/pages/"
    u = []
    soup = func.get_soup(url)
    head = soup.find('strong',string = 'Operational Bulletin')
    table = head.find_next('table')
    for bullet in table.find_all('tr'):
        col = bullet.find_all('td')
        a = col[1].find('a',href= True)
        link = a['href'].strip()
        if flag :
            new_url = base + add + link
        else:
            new_url = base + link
        u.append(new_url)
    return u

def year_link(url):
    y = []
    soup = func.get_soup(url)
    head = soup.find('strong',string = 'Operational Bulletin')
    temp = head.find_next('font')
    year = temp.find_previous()
    #since taking too long limit retriving years to 4
    rows = year.find_all('a',href=True)
    #for row in year.find_all('a',href=True):
    for i in range(2):
        link = rows[i]['href'].strip()
        temp = url +'/'+ link
        y.append(temp)
    return y

def mnc_exist(url):
    soup = func.get_soup(url)
    mnc = soup.find(string = re.compile(r"MNC"))
    if mnc != None:
        return True
    else: return False

def get_file_name(head):
    title = head.text.strip('Operational Bulletin')
    file_name = re.sub(r"\([^()]*\)","",title).strip()
    name = file_name.replace(" ","_") + '.pdf'
    return name

def get_date(head):
    title = head.text.strip('Operational Bulletin')
    year = re.search(r"\([^()]*\)",title).group()
    return year

def get_year(date):
    text = date.strip("()")
    year = text.split(".")
    return year[-1]

def download_file(url,file,name):
    path = 'data/'+file
    exist = os.path.exists(path)
    if not exist :
        os.makedirs(path)
    dest = path + '/' + name
    urlretrieve(url,dest)

def is_toc(row):
    toc = row.find('a',href=True)
    if toc == None:
        return False
    else:
        return True