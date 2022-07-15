import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import EarlyCrow.PairFlow as pf
PATH= "./data/pcap/csv/"


## You may add all files here, here a sample of our data.
# If you want all captures, please go to our Google Drive  then drop files in PATH
FILESET=['njRAT1', 'zebrocy2', 'Remcos1', 'Mivast&Sakula1', 'bitsadmin',
       'carbank', 'miniduke1', 'NanoCore2', 'Mivast&Sakula2', 'Remcos2',
       'PlugX1',  'zebrocy1', 'zebrocy3', 'empire4',
        'Maze', 'onionduke1', 'poisonivy1', 'ChChes', 'GRIFFON16',
       'ImminentMonitor2', 'ImminentMonitor4', 'apt_strongpity1',
       'cobaltstrike1', 'cobaltstrike2', 'empire1', 'empire5', 'empire6',
       'empire7']


FILEWITHLABEL= "_labelled"
CSV = ".csv"
PF='_PairFlow'


GRANULARITY = [600]
for gr in GRANULARITY:
    for fs in FILESET:
        print("Generating PairFlow for {}".format(fs))
        DATA = PATH+fs+FILEWITHLABEL+CSV
        df=pd.read_csv(DATA)
        FILENAME=fs
        PairFlow=pf.pf_generator(df,gr)
        STORE_PATH = PATH + FILENAME + PF + "_"+str(gr)+ FILEWITHLABEL +CSV
        print("Exporting to {}".format(STORE_PATH))
        #PairFlow.to_csv(STORE_PATH, index=False)
