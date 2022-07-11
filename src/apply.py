from PyPDF2 import PdfReader
import pandas as pd
from utils import func, bulletin as bullet
import os
#path to downloaded pdf : data/(year)/

def get_pdf():

    return(0)

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
