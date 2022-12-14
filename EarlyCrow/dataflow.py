import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from EarlyCrow.PairFlow import pairflow_dataflow as pf_features
from EarlyCrow.profiles import urlProfile as up_features
from EarlyCrow.profiles import hostProfile as hp_features
from EarlyCrow.profiles import destProfile as dp_features
from EarlyCrow.CSUpdatingProcess import CSU_dataflow as update

PATH=".data/pairflows/merged_pairflow_files/"
FILENAME="PairFlow_http.csv"

try:
    pairflow_df = pd.read_csv(PATH+FILENAME, converters={'packet_datapoint': eval,'control_plane': eval,
                                                      'udp_plane': eval,'data_plane': eval,
                                             'url_cf_list': eval,'User_Agent': eval,
                                             'fqdn_lists': eval})

    ContextualSummary = pf_features.pairflow_features(pairflow_df)
    ContextualSummary, HP = hp_features.host_features(ContextualSummary)
    up_features.url_features_extractor(ContextualSummary)
    dp_features.destination_features(ContextualSummary)
    updated_ContextualSummary = update.cs_upate(ContextualSummary)
except:
    print("PairFlow_http.csv is not available. \nPlease follow the instruction on README.md, then store the dataset in {} ".format(PATH))
