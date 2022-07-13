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
    path = "data/2022/1235.pdf"
    dfs = tabula.read_pdf(path, pages=12)
    print(dfs)


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