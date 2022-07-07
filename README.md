# MCC-MNC web scraper

## Table of Contents

- [About](#about)
- [Getting Started](#pre)
- [Usage](#usage)

## About <a name = "about"></a>

Simple web scraper which scrapes mcc-mnc values from wikipedia.\n
https://en.wikipedia.org/wiki/Mobile_country_code\n
Also makes use of bulletin pdfs to keep up to date with the changing values.


## Prerequisites<a name = "pre"></a>

```
pip install beautifulsoup
pip install pandas
pip install PyPDF2
```


## Usage <a name = "usage"></a>
case:\n
1 = full scraping\n
2 = download bulletins\n
3 = verification with bulletins\n
```
python3 scraper.py (case)
```
