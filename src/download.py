from utils import bulletin as bullet
from PyPDF2 import PdfReader
from urllib.request import urlopen, urlretrieve
import re
import os
from utils import func

url = "https://www.itu.int/pub/T-SP-OB"
base = "https://www.itu.int/"

def bulletin():
    #flag = 0
    #check_link = func.bullet_link(url,flag)
    flag = 1
    years = bullet.year_link(url)
    #print(years)
    for year in years:
        #print(year)
        new = bullet.bullet_link(year,flag)
        #instead of downloading all bulletins, save to cache (later)
        download_bulletins(new)

def download_bulletins(list):
    for link in list:
        print(link)
        soup = func.get_soup(link)
        table = soup.find('table')
        rows = table.tbody.find_all('tr')
        head = rows[0].find('strong')
        print(head)
        file_name = bullet.get_file_name(head.get_text())
        print(file_name)
        file_date = bullet.get_date(head.get_text())
        file_year = bullet.get_year(file_date)

        if bullet.is_toc(rows[1]):
            a = head.find_next('a',href = True)
            toc_link = base  + a['href']

            if bullet.mnc_exist(toc_link):
                pdf = base + bullet.pdf_first(soup)
                bullet.download_file(pdf,file_year,file_name)
            else:
                print('no mnc')
        else:
            pdf = base + bullet.pdf_first(soup)
            bullet.download_file(pdf,file_year,file_name)
            print('no toc')

#open file instead of downloading and return the pdf