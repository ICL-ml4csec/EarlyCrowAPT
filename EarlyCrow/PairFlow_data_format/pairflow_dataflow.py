import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import math
import EarlyCrow.preprocessing.flags as prep
import EarlyCrow.PairFlow_data_format.modules as pf
def pf_generator(_df,GRANULARITY):
    MAXIMUM_CAPTURE = 900
    _df=_df.fillna({'Info': '',
                      'Status_Code_Description':'',
                      'http_server':'', 'http_request_uri_query':'',
                      'http_request_uri_query_parameter':''})

    _df=prep.packetsFlags(_df)

    df_data=_df.copy(deep=True)
    #sample_rate= df_data.Relative_Time.max() / GRANULARITY
    sample_rate = MAXIMUM_CAPTURE / GRANULARITY

    col = ['FlowID', 'Source', 'Destination', 'label',
           'packet_datapoint', 'control_plane',
           'data_plane', 'udp_plane', 'icmp_plane', 'User_Agent',
           'Status_Code', 'Status_Code_Description', 'Content_Type',
           'http_server', 'EPFLAG_ICMP',
           'EPFLAG_UDP', 'EPFLAG_TCP', 'EPFLAG_DNS', 'EPFLAG_HTTP',
           'EPFLAG_HTTP_XML', 'EPFLAG_TLS', 'EPFLAG_SSL', 'EPFLAG',
           'fqdn_lists',
           'fqdn_ns_lists', 'fqdn_ip_lists', 'Server_Cipher_Suite',
           'Client_Cipher_Suite',
           'Client_Extension_Type', 'Server_Extension_Type',
           'Client_Signature_Algorithm_Hash',
           'Server_Signature_Algorithm_Hash',
           'Server_Supported_Group', 'Client_Supported_Group',
           'Server_ALPN_Next_Protocol',
           'Client_ALPN_Next_Protocol', 'Server_EC_point_format',
           'Client_EC_point_format',
           'Server_Compression_Method', 'Client_Compression_Method',
           'producedAt', 'nextUpdate', 'thisUpdate'
        , 'url_cf_list']

    #initlize the main PairFlow dataframe
    PairFlow = pd.DataFrame(columns=col)
    cf_col = ['fqdn_lists', 'fqdn_ip_lists', 'User_Agent',
              'Content_Type', 'Status_Code_Description',
              'Status_Code', 'http_server', 'packet_datapoint',
              'control_plane',
              'data_plane', 'udp_plane', 'icmp_plane',
              'Server_Cipher_Suite',
              'Client_Cipher_Suite', 'Server_Extension_Type',
              'Client_Extension_Type',
              'Server_Signature_Algorithm_Hash',
              'Client_Signature_Algorithm_Hash',
              'Server_Supported_Group', 'Client_Supported_Group',
              'Server_ALPN_Next_Protocol',
              'Client_ALPN_Next_Protocol', 'Server_EC_point_format',
              'Client_EC_point_format',
              'Server_Compression_Method', 'Client_Compression_Method',
              'producedAt', 'nextUpdate', 'thisUpdate',
              'url_cf_list']
    for cfc in cf_col:
        PairFlow['{}'.format(cfc)] = PairFlow[
            '{}'.format(cfc)].astype('object')

    lastCF_idx=0

    for gr in range (math.ceil(sample_rate)):
        print("Sample # {} out of {} ".format(gr,sample_rate), end='\r')

        df = df_data[(df_data.Relative_Time >= gr * GRANULARITY) & (
                    df_data.Relative_Time < gr * GRANULARITY + GRANULARITY)]
        ## Tracking

        conn_pairs_unique_df=pf.tracking_packets(df, GRANULARITY, gr)
        if len(conn_pairs_unique_df) == 0:
            print("No packets found in a given time interval ({},{})"
                  .format(gr * GRANULARITY,
                          gr * GRANULARITY + GRANULARITY),
                  end='\r')
            continue

        for i in range(len(conn_pairs_unique_df)):

            print("Overall progress {}%. Working on PairFlow # {} ".format(i,round(i/len(conn_pairs_unique_df)*100),1), end='\r')
            flow_biPkts=df[((df.Source==conn_pairs_unique_df.loc[i,'Source']) &
               (df.Destination==conn_pairs_unique_df.loc[i,'Destination']) )|
               ((df.Destination==conn_pairs_unique_df.loc[i,'Source']) &
               (df.Source==conn_pairs_unique_df.loc[i,'Destination']))]


            flow_biPkts=flow_biPkts.reset_index(drop=True)
            #print("Flow Pairs: {} and {}".format(flow_biPkts.loc[0,'Source'],flow_biPkts.loc[0,'Destination']), end='\r') # static zero, we just want the connection pair

            flow_biPkts,domain_list, ns_list, ip_list=pf.tracking_dns(df, flow_biPkts, GRANULARITY, gr) ## also flow_biPkts will include DNS packets after executing the method

            flow_biPkts = flow_biPkts.drop_duplicates(subset=['No'])
            flow_biPkts=flow_biPkts.sort_values('No')

            flow_biPkts=flow_biPkts.rename(columns={"No": "oIndex"})
            flow_biPkts=flow_biPkts.reset_index(drop=True)

            flow_biPkts.index = flow_biPkts.index.set_names(['Packet_No'])

            flow_biPkts=flow_biPkts.reset_index().rename(columns={flow_biPkts.index.name:'Packet_No'})

            flow_biPkts.insert(0, 'FlowID', i) # zero refer to the column position

            #print("Adding New PairFlow for flow {}".format(i), end='\r')

            ## add basic info
            currCF_idx = i + lastCF_idx
            PairFlow.at[currCF_idx, 'FlowID'] = flow_biPkts.loc[0,'FlowID'] + lastCF_idx
            PairFlow.at[currCF_idx, 'Source'] = conn_pairs_unique_df.loc[i,'Source']
            PairFlow.at[currCF_idx, 'Destination'] = conn_pairs_unique_df.loc[i,'Destination']
            PairFlow.at[currCF_idx, 'label'] = "legitimate"
            check_label = flow_biPkts.label.str.contains(
                'malicious').unique()
            for label_idx in range(len(check_label)):
                if check_label[label_idx] == True:
                    PairFlow.at[currCF_idx, 'label'] = "malicious"
                    break

            pf.aggregation(flow_biPkts,PairFlow,currCF_idx,gr, GRANULARITY)

            pf.encapsulation(PairFlow,flow_biPkts,currCF_idx,domain_list,ns_list,ip_list)
        print("Time Window from {} to {} minutes is completed ".format(gr*GRANULARITY/60,(gr * GRANULARITY + GRANULARITY)/60))
        lastCF_idx = lastCF_idx + len(conn_pairs_unique_df)

    PairFlow["EPFLAG"] = PairFlow["EPFLAG_ICMP"].astype(str) + \
                               PairFlow["EPFLAG_UDP"].astype(str) + \
                               PairFlow["EPFLAG_TCP"].astype(str) + \
                               PairFlow["EPFLAG_DNS"].astype(str) + \
                               PairFlow["EPFLAG_HTTP"].astype(str) + \
                               PairFlow["EPFLAG_HTTP_XML"].astype(
                                   str) + \
                               PairFlow["EPFLAG_TLS"].astype(str) + \
                               PairFlow["EPFLAG_SSL"].astype(str)


    return PairFlow