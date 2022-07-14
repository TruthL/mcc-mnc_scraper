import pandas as pd
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import PyPDF2 as pdf
import tabula
import re
import os
import glob
#ADD = insert
#SUP = delete
#REP = replace
def main():
    iso_pd = pd.read_csv('iso_mcc.csv')
    loc = get_iso(iso_pd,649)
    print(loc)

def get_index(df,mcc):
    loc = df.loc[df['MCC']== mcc]
    return loc.index.values[0]

def get_iso(df,mcc):
    if (mcc== 649):
        return 'NA'
    index = get_index(df,mcc)
    loc = df.iloc[index]
    iso = loc['alpha-2']
    return iso

def download_file(url,file,name):
    path = 'data/'+file
    exist = os.path.exists(path)
    if not exist :
        os.makedirs(path)
        dest = path + '/' + name
        urlretrieve(url,dest)


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