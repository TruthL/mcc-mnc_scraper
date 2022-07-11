import pandas as pd
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import re
import os
#ADD = insert
#SUP = delete
#REP = replace
def main():
    url = "https://www.itu.int/pub/T-SP-OB.1162-2018"
    string = """Operational Bulletin No. 1162 (15.XII.2018)"""
    # df = pd.read_csv('mcc-mnc.csv',dtype = str)
    # #df = pd.DataFrame(columns= ['MCC','MNC','alpha-2','destination','operator_name','network_name','status'],dtype='string')
    # dest = df.loc[df['destination']=='International Mobile, shared code']
    # det = dest.loc[dest['MNC']=='93']
    # ind = get_index(det)
    # print(ind)
    # p = df.at[ind,'destination']
    # print(p)
    # h = re.search(r"^.*?\([^()]*\)",string).group()
    # print(h)
    # trim = h.strip('Operational Bulletin')
    # #print(type(h))
    # print(trim)
    exist = os.path.exists("data/2018/No._1159.pdf")
    print(exist)

def download_file(url,file,name):
    path = 'data/'+file
    exist = os.path.exists(path)
    if not exist :
        os.makedirs(path)
        dest = path + '/' + name
        urlretrieve(url,dest)

def get_index(entry):
    ind = entry.index.values[0]
    return ind

def get_soup(url):
    page = urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html,"html.parser")
    return soup

def pdf_first(a):
    #get link of pdf
    img = a.find('img', title = 'PDF format')
    down = img.find_next('a', string = 'DOWNLOAD',href = True)
    print(down['href'])
    return down

if __name__ == '__main__':
    main()