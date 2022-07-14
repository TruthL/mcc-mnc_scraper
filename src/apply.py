import pandas as pd
import utils.patch as patch
import utils.func as func
#op = the operation applied to the code:
#ADD = insert
#SUP = delete
#REP = replace (not sure if there is a replace for mcc & mnc)
#LIR = read = status == read

#States of status:
#Operational, Not operational, Ongoing, Returned spare, 
def patch_apply():
    delta_file ='delta_2018-2022.csv'
    wiki_file = 'mcc-mnc.csv'
    iso_file = 'iso_mcc.csv'
    df = pd.read_csv(delta_file)
    wiki_df = pd.read_csv(wiki_file, keep_default_na=False, na_values=[""])
    print(wiki_df.head)
    wiki_df['MNC'] = wiki_df['MNC'].astype('Int64')
    print(wiki_df.head)

    for index, row in df.iterrows():
        mcc = row['MCC']
        mnc = int(row['MNC'])
        dest = row['destination']
        net_name = row['network_name']
        number = row['bulletin no.']
        op = row['op']

        if op == 'ADD':
            iso_pd = pd.read_csv(iso_file)
            iso = patch.get_iso(iso_pd,mcc)
            # dest = patch.get_dest(df,mcc)
            index = patch.locate(wiki_df,mcc,mnc)
            if index == None :
                wiki_df = patch.to_df(wiki_df,mcc,str(mnc),iso,dest,net_name,net_name,'Operational',str(number))
            else :
                wiki_df.at[index,'status'] = 'Operational'
                wiki_df.at[index,'patched'] = str(number)
            # print('add')
        elif op == 'SUP':
            index = patch.locate(wiki_df,mcc,mnc)
            if index != None:
                wiki_df.at[index,'status'] = 'Not operational'
                wiki_df.at[index,'patched'] = str(number)
            else:
                print('DELETE(SUP): MCC+MNC ('+ str(mcc)+' '+str(mnc)+') not found')
            # print('delete')
            #change the status to 'Not operational'
        elif op == 'REP':
            print('replace: not yet implemented')
        elif op == 'LIR':
            index = patch.locate(wiki_df,mcc,mnc)
            wiki_df.at[index,'status'] = 'Read'
            wiki_df.at[index,'patched'] = str(number)
            # print('read')
        else:
            print('Invalid operation given : '+ op)
    wiki_df = wiki_df.sort_values(by=['destination'])
    wiki_df['alpha-2'] = wiki_df['alpha-2'].astype('str')
    wiki_df.to_csv("mcc-mnc(delta applied).csv", encoding='utf-8', index= False)


if __name__ == '__main__':
    patch_apply()
