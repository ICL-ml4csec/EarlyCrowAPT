import pandas as pd
import EarlyCrow.preprocessing.flags as prep
PATH=""
FILESET=[]
CSV = ".csv"
TXT = '.txt'
FILEWITHLABEL = "_labelled"

def labelling(IoCpath, _df):
    domains, ip=prep.IoC_parser(IoCpath)
    return domains, ip,_df


for fs in FILESET:
    print("Labelling {}".format(fs))
    FILENAME=fs
    IOC= FILENAME + TXT
    df=pd.read_csv(PATH+FILENAME+CSV)
    domains, ip,df=labelling(PATH+IOC,df)
    df = df.fillna({'Info': ''})
    for i in range(len(ip)):
        df.loc[ (df.Source == ip[i]) | (df.Destination == ip[i]), "label"] = "malicious"

    for i in range(len(domains)):
        df.loc[ (df.Info.str.contains(domains[i]) ) , "label"] = "malicious"
    df=df.fillna({'label':'legitimate'})
    df.insert(0, 'multiple_label', FILENAME)

    #df.to_csv(PATH+FILENAME+FILEWITHLABEL+CSV,index=False)


