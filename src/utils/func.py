#functions for formulating the mcc-mnc scraped table

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

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

#gets the "soups" into an arry from the links provided
def get_soups():
    soups = []
    for link in links:
        page = urlopen(link)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        soup.prettify()
        soups.append(soup)
    return soups

#given the url, soup is returned
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

#get the index of soup from given mcc (soups categorized by the range)
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

# gets text
def get_t(ln):
    if ln.a == None :
        net = ln.text.strip()
    else:
        a = ln.find('a')
        net = a.get_text()
    return net

#puts the attributes given to a df
def to_df(df, mcc,mnc,iso,dest,op_name,net_name,status):
    dict = {'MCC':[mcc], 'MNC':[mnc], 'alpha-2':[iso], 
            'destination':[dest], 'operator_name':[op_name], 
            'network_name':[net_name], 'status':[status]}
    df2 = pd.DataFrame.from_dict(dict)
    df = pd.concat([df,df2],ignore_index=True)
    return df

#goes through given table and inserts to a data frame
def parse_table(table, iso, destination, df):
    for row in table.tbody.find_all('tr'):
        col = row.find_all('td')
        if col != []:
            mcc = get_mcc(col[0].text.strip())
            mnc = col[1].text.strip()
            net_name = get_t(col[2])
            op_name = get_t(col[3])
            #make status uppercase
            status = get_t(col[4])
            df = to_df(df,mcc,mnc,iso,destination,op_name,net_name,status)
    return df

def get_mcc(txt):
    if len(txt) > 3 :
        mcc = txt[-3:]
        return mcc
    else : return txt

def to_iso(df, mcc,iso,dest):
    dict = {'MCC':[mcc],'alpha-2':[iso],'destination':[dest]}
    df2 = pd.DataFrame.from_dict(dict)
    df = pd.concat([df,df2],ignore_index=True)
    return df

def check_iso(df,mcc,iso):
    if len(df) !=0:
        loc_mcc = df.loc[df['MCC']== str(mcc)]
        if len(loc_mcc) != 0 :
            loc_iso = loc_mcc.loc[loc_mcc['alpha-2']== iso]
            if len(loc_iso) != 0:
                return False
    return True
    