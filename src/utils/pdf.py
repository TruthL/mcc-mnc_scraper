import PyPDF2 as pdf
import tabula
import re
import os
import pandas as pd

def get_page(obj):
    num = obj.getNumPages()
    string = "international identification plan"
    string2 = "public networks and subscriptions"
    for i in range(4,num):
        page = obj.getPage(i)
        text = page.extract_text()
        if re.search(string,text):
            return i+1
        elif re.search(string2,text):
            return i+1
    return None

def get_table(path):
    list = []
    df = pd.DataFrame()
    obj = pdf.PdfFileReader(path) 
    page_num = get_page(obj)
    if page_num != None:
        table = tabula.read_pdf(path, pages= page_num,silent = True,stream = True)
        for i in range(len(table)):
            if 'Country/Geographical area' in table[i].columns:
                list.append(i)
        for i in list:
            df = pd.concat([df,table[i]],ignore_index=True)
        df = df.fillna("")
        if "Unnamed: 0" in df.columns:
            df['Country/Geographical area'] = df['Country/Geographical area'] + df["Unnamed: 0"]
            df = df.drop("Unnamed: 0",axis=1)
        return df

#get table 
#read what is updated
#get table and give date updated (bulletin num)

def to_df(df,mcc,mnc,dest,network_name,op):
    dict = {'MCC':[mcc], 'MNC':[mnc], 'destination':[dest], 
            'network_name':[network_name], 'op':[op]}
    df2 = pd.DataFrame.from_dict(dict)
    df = pd.concat([df,df2],ignore_index=True)
    return df

def check_mcc_col_name(df):
    if 'MCC+MNC *' in df.columns:
        return 'MCC+MNC *'
    elif 'MCC+MNC' in df.columns:
        return 'MCC+MNC'

def check_net_col_name(df):
    if 'Operator/Network' in df.columns :
        return 'Operator/Network'
    elif 'Applicant/Network' in df.columns:
        return 'Applicant/Network'