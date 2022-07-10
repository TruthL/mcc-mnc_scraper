import pandas as pd

#ADD = insert
#SUP = delete
#REP = replace
def main():
    df = pd.read_csv('mcc-mnc.csv',dtype = str)
    #df = pd.DataFrame(columns= ['MCC','MNC','alpha-2','destination','operator_name','network_name','status'],dtype='string')
    dest = df.loc[df['destination']=='International Mobile, shared code']
    det = dest.loc[dest['MNC']=='93']
    ind = get_index(det)
    print(ind)
    p = df.at[ind,'destination']
    print(p)


def get_index(entry):
    ind = entry.index.values[0]
    return ind

if __name__ == '__main__':
    main()