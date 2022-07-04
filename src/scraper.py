from email.mime import base
from re import L
import pandas as pd
import mechanicalsoup
from utils import func

#want to retrieve:
# mcc
# mnc
# alpha-2
# destination
# network name
# operator name
#check the policy of web scraping of wikipedia again

url = "https://en.wikipedia.org/wiki/Mobile_country_code"
browser = mechanicalsoup.Browser()
page = browser.get(url)
base_html = page.soup

span_flag = 0
cont_flag = 0
many_flag = 0
i = 0
glob_dest = ''
glob_iso = ''


soup_arr = func.get_soups()

table = base_html.find("table", class_ = 'wikitable sortable mw-collapsible')
#print(table)
int_op = base_html.find("span", id= "International_operators")
int_table = int_op.find_next('table')

df = pd.DataFrame(columns= ['MCC','MNC','alpha-2','destination','operator_name','network_name','status'])
no_mnc = pd.DataFrame(columns= ['MCC','alpha-2','destination'])
#html into df
for row in table.tbody.find_all('tr'):
    if cont_flag:
        cont_flag = 0
        continue

    col = row.find_all('td')
    if col != [] :
        if len(col) > 1:
            mcc = col[0].text.strip()
            #340 and 742 share mcc
            #362 many to many iso = BQ/CW/SX
            #one mcc many alpha-2
            if(mcc == '340' or mcc == '647' or mcc == '742'):
                if( mcc == '647'):
                    cont_flag = 1
                continue

            if (mcc == '362') :
                if (many_flag):
                    continue
                else:
                    destination = 'Former Netherlands Antilles'
                    iso = 'BQ/CW/SX'
                    ind = func.get_ind(mcc)
                    reg = soup_arr[ind]
                    head = reg.find('a', string = destination)
                    tab = head.find_next('table')
                    for r in tab.tbody.find_all('tr'):
                        c = r.find_all('td')
                        if c != []:
                            mnc = c[1].text.strip()
                            net_name = func.get_t(c[2])
                            op_name = func.get_t(c[3])
                            status = func.get_t(c[4])
                            df = func.to_df(df,mcc,mnc,iso,destination,op_name,net_name,status)
                    many_flag = 1
                    continue
            else:
                if span_flag:
                    if func.get_t(col[1]) == 'no networks yet':
                        df = func.to_df(df,mcc,'',glob_iso,glob_dest,'','','')
                    i -= 1
                    if i == 1:
                        span_flag = 0
                    continue

                destination = func.get_t(col[1]) 
                #destination = needs.read_head(col[1])
                iso = col[2].text.strip()
                mnc_l = func.get_t(col[3])

                if col[1].has_key("rowspan"):
                    span_flag = 1
                    i = int(col[1]["rowspan"])
                    glob_dest = destination
                    glob_iso = iso

                if(mnc_l == 'no networks yet'):
                    df = func.to_df(df,mcc,'',iso,destination,'','','')
                    d = {'MCC':[mcc], 'alpha-2':[iso],'destination':[destination]}
                    df1 = pd.DataFrame.from_dict(d)
                    no_mnc = pd.concat([no_mnc,df1],ignore_index=True)
                    continue
                
                #print(destination)
                ind = func.get_ind(mcc)
                #print(ind)
                reg = soup_arr[ind]
                tbl = func.get_table(col[1],reg)
                for r in tbl.tbody.find_all('tr'):
                    #print(r)
                    c = r.find_all('td')
                    if c != []:
                        mnc = c[1].text.strip()
                        net_name = func.get_t(c[2])
                        op_name = func.get_t(c[3])
                        status = func.get_t(c[4])
                        df = func.to_df(df,mcc,mnc,iso,destination,op_name,net_name,status)
        else:
            continue        

#International Operators
for row in int_table.tbody.find_all('tr'):
    dest = int_op.text.strip()
    #print(dest)
    col = row.find_all('td')
    if col !=  []:
         mcc = col[0].text.strip()
         mnc = col[1].text.strip()
         net_name = col[2].text.strip()
         op_name = col[3].text.strip()
         status = col[4].text.strip()
         df = func.to_df(df,mcc,mnc,'',dest,op_name,net_name,status)
    

df.to_csv("mcc-mnc.csv", encoding='utf-8')
no_mnc.to_csv("mcc_with_no_networks.csv", encoding='utf-8')
