from email.mime import base
from re import L
import pandas as pd
import utils.func as func
import sys

#want to retrieve:
# mcc
# mnc
# alpha-2
# destination
# network name
# operator name
#check the policy of web scraping of wikipedia again

#exceptions: 340, 647, 362 and international operators

def formulate():
    url = "https://en.wikipedia.org/wiki/Mobile_country_code"
    base_html = func.get_soup(url)

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
    iso_df = pd.DataFrame(columns=['MCC','alpha-2','destination'])
    #html into df
    #for debugging
    print("begin")
    for row in table.tbody.find_all('tr'):
        if cont_flag:
            cont_flag = 0
            continue

        col = row.find_all('td')
        if col != [] :
            if len(col) > 1:
                # mcc = col[0].text.strip()
                # print(col[0].text.strip())
                mcc = func.get_mcc(col[0].text.strip())
                #340 and 742 share mcc
                #one mcc many alpha-2
                if(mcc == '340'):
                    ind = func.get_ind(mcc)
                    reg = soup_arr[ind]
                    destination = "French Antilles"
                    head = reg.find('a',string = destination)
                    iso = "BL/GF/GP/MF/MQ"
                    table = head.find_next('table')
                    df = func.parse_table(table,iso,destination,df)
                    if func.check_iso(iso_df,mcc,iso):
                        iso_df = func.to_iso(iso_df,mcc,iso,destination)
                    continue

                if( mcc == '647'):
                    cont_flag = 1
                    ind = func.get_ind(mcc)
                    reg = soup_arr[ind]
                    destination = "French Departments and Territories in the Indian Ocean"
                    head = reg.find('a',string = destination)
                    iso = "YT/RE"
                    table = head.find_next('table')
                    df = func.parse_table(table,iso,destination,df)
                    if func.check_iso(iso_df,mcc,iso):
                        iso_df = func.to_iso(iso_df,mcc,iso,destination)
                    continue

                #362 many to many iso = BQ/CW/SX
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
                        df = func.parse_table(tab,iso,destination,df)
                        if func.check_iso(iso_df,mcc,iso):
                            iso_df = func.to_iso(iso_df,mcc,iso,destination)
                        many_flag = 1
                        continue
                else:
                    if span_flag:
                        if func.get_t(col[1]) == 'no networks yet':
                            #print(mcc + " glob dest = " + glob_dest)
                            df = func.to_df(df,mcc,'',glob_iso,glob_dest,'','','')
                            d = {'MCC':[mcc], 'alpha-2':[glob_iso],'destination':[glob_dest]}
                            df1 = pd.DataFrame.from_dict(d)
                            no_mnc = pd.concat([no_mnc,df1],ignore_index=True)
                        i -= 1
                        if i == 1:
                            span_flag = 0
                        continue

                    destination = func.get_t(col[1]) 
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
                        if func.check_iso(iso_df,mcc,iso):
                            iso_df = func.to_iso(iso_df,mcc,iso,destination)
                        continue
                    
                    #print(destination)
                    ind = func.get_ind(mcc)
                    #print(ind)
                    reg = soup_arr[ind]
                    tbl = func.get_table(col[1],reg)
                    df = func.parse_table(tbl,iso,destination,df)
                    if func.check_iso(iso_df,mcc,iso):
                        iso_df = func.to_iso(iso_df,mcc,iso,destination)
            else:
                continue        

    #International Operators'
    dest = 'International Mobile, shared code'
    iso = 'IO'
    for row in int_table.tbody.find_all('tr'):
        col = row.find_all('td')
        if col != []:
            mcc = func.get_mcc(col[0].text.strip())
            mnc = col[1].text.strip()
            net_name = func.get_t(col[2])
            op_name = func.get_t(col[3])
            status = func.get_t(col[4])
            df = func.to_df(df,mcc,mnc,iso,dest,op_name,net_name,status)
            if func.check_iso(iso_df,mcc,iso):
                iso_df = func.to_iso(iso_df,mcc,iso,dest)

    df = df.sort_values(by=['destination'])
    df.to_csv("mcc-mnc.csv", encoding='utf-8', index= False)
    no_mnc.to_csv("mcc_with_no_networks.csv", encoding='utf-8', index= False)
    iso_df.to_csv("iso_mcc.csv", encoding='utf-8', index= False)