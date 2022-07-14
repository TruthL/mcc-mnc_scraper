from numpy import NaN
import pandas as pd

def get_iso(df,mcc):
    index = get_index(df,mcc)
    if index != None:
        loc = df.iloc[index]
        iso = loc['alpha-2']
        return iso
    return None

def get_dest(df,mcc):
    index = get_index(df,mcc)
    if index != None:
        loc = df.iloc[index]
        dest = loc['destination']
        return dest
    return None

def get_index(df,mcc):
    loc = df.loc[df['MCC']== mcc]
    if len(loc) != 0:
        return loc.index.values[0]
    else :
        return None

def locate(df,mcc,mnc):
    get = df.loc[df['MCC'] == mcc]
    if len(get)  != 0:
        entry = get.loc[get['MNC']== mnc]
        if len(entry) != 0:
            index = entry.index.values[0]
            return index
    return None

def to_df(df, mcc,mnc,iso,dest,op_name,net_name,status,patch):
    dict = {'MCC':[mcc], 'MNC':[mnc], 'alpha-2':[iso], 
            'destination':[dest], 'operator_name':[op_name], 
            'network_name':[net_name], 'status':[status], 'patched':[patch]}
    df2 = pd.DataFrame.from_dict(dict)
    df = pd.concat([df,df2],ignore_index=True)
    return df