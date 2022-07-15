import pandas as pd
import EarlyCrow.PairFlow_data_format.modules.connType as ct
PATH='.data/pairflows/'
FILESET=['njRAT1', 'zebrocy2', 'Remcos1', 'Mivast&Sakula1', 'bitsadmin',
       'carbank', 'miniduke1', 'NanoCore2', 'Mivast&Sakula2', 'Remcos2',
       'PlugX1',  'zebrocy1', 'zebrocy3', 'empire4',
        'Maze', 'onionduke1', 'poisonivy1', 'ChChes', 'GRIFFON16',
       'ImminentMonitor2', 'ImminentMonitor4', 'apt_strongpity1',
       'cobaltstrike1', 'cobaltstrike2', 'empire1', 'empire5', 'empire6',
       'empire7']
#
#
FILEWITHLABEL= "_labelled"
CSV = ".csv"
CF='_PairFlow'
GRANULARITY = 900
version=""
INITALFILE="apt_strongpity1"
DATA = PATH + INITALFILE + CF + "_" + str(
    GRANULARITY) + FILEWITHLABEL + version + CSV
#
df=pd.read_csv(DATA)
col=df.columns

for fs in FILESET:

    DATA = PATH + fs + CF + "_" + str(
        GRANULARITY) + FILEWITHLABEL + version + CSV
    df_temp=pd.read_csv(DATA)
    df=df.append(df_temp)


df=df.reset_index(drop=True)
#
#
PATH="./data/pairflows/merged_pairflow_files/"
FILENAME = "PairFlow"
CSV=".csv"
df.to_csv(PATH+FILENAME+CSV,index=False)
httpBased,httpsBased,tcpudpBased=ct.variants_extraction(df)
VARIANTS = ['_http','_https','_tcp_udp']

httpBased.to_csv(PATH+FILENAME+VARIANTS[0]+CSV,index=False)
httpsBased.to_csv(PATH+FILENAME+VARIANTS[1]+CSV,index=False)
tcpudpBased.to_csv(PATH+FILENAME+VARIANTS[2]+CSV,index=False)

