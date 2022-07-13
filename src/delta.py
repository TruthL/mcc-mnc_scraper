from PyPDF2 import PdfReader
import pandas as pd
from utils import func, bulletin as bullet, pdf
import os
import glob

#path to downloaded pdf : ../data/(year)/
def get_delta():
    flag = 0
    glob_dest = ""
    glob_op = ""
    path = "data"
    dir = os.listdir(path)
    dir.sort()

    df_delta = pd.DataFrame(columns= ['MCC','MNC','destination','network_name','op'])
    for d in dir:
        n_path = path + '/' + d + '/*.pdf'
        files = glob.glob(n_path)
        files.sort()
        for file in files :
            print(file)
            if file == 'data/2021/1214.pdf':
                continue
            table = pdf.get_table(file)
            mcc_name = pdf.check_mcc_col_name(table)
            print(table)
            for index, row in table.iterrows():
                string = row['Country/Geographical area'] 
                mcc_mnc = row[mcc_name]
                net_name = row['Operator/Network']
                if mcc_mnc == '*':
                    continue
                op = string[-3:]
                dest = string.strip(op)
                l_mcc= mcc_mnc.split()
                if dest != "" :
                    glob_dest = dest
                    glob_op = op
                    flag = 1
                if (l_mcc != []) and flag:
                    mcc = l_mcc[0]
                    mnc = l_mcc[1]
                    df_delta = pdf.to_df(df_delta,mcc,mnc,glob_dest,net_name,glob_op)
                    if index != (len(table)-1):
                        next = table.iloc[index+1]
                        if next[mcc_name] == "" :
                            flag = 0

    print(df_delta)
    df_delta.to_csv("delta_2018-2022.csv",encoding='utf-8', index= False)

#op = the operation applied to the code:
#ADD = insert
#SUP = delete
#REP = replace (not sure if there is a replace for mcc & mnc)
#LIR = read = status == read

#States of status:
#Operational, Not operational, Ongoing, Returned spare, 
def apply_update(df,mcc,mnc,operator_name,op):
    if op == 'ADD':
        print('add')
        
    elif op == 'SUP':
        get = df.loc[df['MCC'] == mcc]
        entry = get.loc[get['MNC']== mnc]
        index = entry.index.values[0]
        df.at[index,'status'] = 'Not operational'
        print('delete')
        #change the status to 'Not operational'
    elif op == 'REP':
        print('replace')
    elif op == 'LIR':
        get = df.loc[df['MCC'] == mcc]
        entry = get.loc[get['MNC']== mnc]
        index = entry.index.values[0]
        df.at[index,'status'] = 'Read'
    else:
        print('Invalid operation given')

    return df

if __name__ == '__main__':
    get_delta()