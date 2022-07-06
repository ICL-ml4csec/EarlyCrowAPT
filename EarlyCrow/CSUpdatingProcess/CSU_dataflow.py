import pandas as pd
import numpy as np

def cs_upate(ContextualSummary):
    PRINT_MESSAGE="\n*** Contextual summaries updating process"
    print("{}".format(PRINT_MESSAGE))

    identifiers=['CSID', 'LastFlowID', 'Source', 'Destination','label','multiple_label']
    pf_format_flags=['EPFLAG_ICMP', 'EPFLAG_UDP', 'EPFLAG_TCP', 'EPFLAG_DNS', 'EPFLAG_HTTP',
           'EPFLAG_TLS', 'EPFLAG_SSL']
    time_window=['sample_interval']

    pf_format=[  'tcp_packets', 'udp_packets',
           'icmp_packets', 'http_packets', 'tls_packets', 'ssl_packets',
           'dns_packets', 'TTL_max', 'TTL_min', 'TTL_mean', 'TTL_median',
           'Delta_Time_max', 'Delta_Time_min', 'Delta_Time_mean',
           'Delta_Time_median', 'Duration', 'Content_Length_Total',
           'Content_Length_min', 'Content_Length_max', 'Content_Length_median',
           'total_bytes', 'total_sent_bytes', 'total_recv_bytes' ]
    pf_col=['PF_TotalBytes',
           'PF_RecvSentBytes', 'PF_total_packets', 'PF_tcpRatio', 'PF_udpRatio',
           'PF_icmpRatio', 'PF_dnsRatio', 'PF_httpRatio', 'PF_encryptedRatio',
           'PF_SCode_1xx', 'PF_SCode_2xx', 'PF_SCode_3xx', 'PF_SCode_4xx',
           'PF_SCode_5xx', 'PF_cf_js', 'PF_cf_html', 'PF_cf_image', 'PF_cf_video',
           'PF_cf_app', 'PF_cf_text',  'PF_GET_freq', 'PF_POST_freq',
           'PF_total_SCode', 'PF_SCode_1xxRatio', 'PF_SCode_2xxRatio',
           'PF_SCode_3xxRatio', 'PF_SCode_4xxRatio', 'PF_SCode_5xxRatio',
           'PF_total_getpost', 'PF_GET_ratio', 'PF_POST_ratio',
           'PF_POST_GET_ratio', 'PF_ResumedConnectionsNo', 'PF_dnsReqNo',
           'PF_dnsReqRatio', 'PF_TTL_max', 'PF_TTL_min', 'PF_TTL_mean',
           'PF_TTL_median', 'PF_Delta_Time_max', 'PF_Delta_Time_min',
           'PF_Delta_Time_mean', 'PF_Delta_Time_median', 'PF_Duration',
           'PF_Content_Length_Total', 'PF_Content_Length_min',
           'PF_Content_Length_max','PF_Content_Length_median', 'PF_total_cf', 'PF_cf_jsRatio',
           'PF_cf_htmlRatio', 'PF_cf_imageRatio', 'PF_cf_videoRatio',
           'PF_cf_appRatio', 'PF_cf_textRatio',
           'PF_No_belowAVG', 'PF_No_aboveAVG', 'PF_ratio_aboveAvg',
           'PF_ratio_belowAvg', 'PF_No_outliers', 'PF_ratio_outliers',
           'PF_magnitudeMax_outliers', 'PF_magnitudeMin_outliers',
           'PF_magnitudeMean_outliers', 'PF_magnitudeStd_outliers',
           'PF_Max_idleTime', 'PF_Min_idleTime', 'PF_Mean_idleTime']

    hp_col=['HP_Distinct_UAs_per_host', 'HP_Avg_UAs_per_host',
           'HP_Min_UAs_per_host', 'HP_Max_UAs_per_host', 'HP_nAvg_UA_Popularity',
           'HP_Frac_UA_1', 'HP_Frac_UA_10', 'HP_Frac_UA_5', 'HP_Ratio_UAs',
           'HP_MeanResumedConnections', 'HP_MaxResumedConnections',
           'HP_MinResumedConnections', 'HP_MTDSC', 'HP_MinTDSC',
           'HP_dnsReq_perflow', 'HP_DestByIP']

    hp_excluded=['HP_Avg_OS', 'HP_OS_per_host', 'HP_dominant_OS1_Windows NT 6.1',
           'HP_dominant_OS2_Linux', 'HP_Avg_Browsers', 'HP_Browsers_per_host',
           'HP_dominant_Browser1_MSIE', 'HP_dominant_Browser2_Firefox']

    up_col=['UP_Distinct_url',
           'UP_Num_hasString', 'UP_Num_Filename', 'UP_num_exe', 'UP_Frac_query',
           'UP_Frac_URL_filename', 'UP_Frac_URL_filename_exe', 'UP_URL_Length_Max',
           'UP_URL_Length_Min', 'UP_URL_Length_Mean', 'UP_Depth_Max',
           'UP_Depth_Min', 'UP_Depth_Mean', 'UP_No_Para_Max', 'UP_No_Para_Min',
           'UP_No_Para_Mean', 'UP_No_Values_Max', 'UP_No_Values_Min',
           'UP_No_Values_Mean', 'UP_No_Frag_Max', 'UP_No_Frag_Min',
           'UP_No_Frag_Mean']

    dp_col=['DP_HostsConnected',
           'DP_RecvSentBytes_Mean', 'DP_RecvSentBytes_Max', 'DP_RecvSentBytes_Min',
           'DP_IdleTime_Mean', 'DP_IdleTime_Max', 'DP_IdleTime_Min',
           'DP_ResumedConnectionsNo_Mean', 'DP_ResumedConnectionsNo_Max',
           'DP_ResumedConnectionsNo_Min', 'DP_Distinct_url_Mean',
           'DP_PacketFailure_Mean', 'DP_PacketFailure_Max', 'DP_PacketFailure_Min',
           'DP_dnsReqNo_Mean', 'DP_dnsReqNo_Max', 'DP_dnsReqNo_Min',
           'DP_dnsReqRatio_Mean', 'DP_dnsReqRatio_Max', 'DP_dnsReqRatio_Min']
    average_features=pf_format+pf_col+hp_col+up_col+dp_col

    updated_cs = pd.DataFrame(columns=identifiers+pf_format_flags+pf_format+pf_col+hp_col+up_col+dp_col)
    ## update ContextualSummary ID and Flow ID according to Pairs, sample_interval and label
    ## to we will have a dataframe of one CSID for each pairs with
    ##Flow ID that relfect the last number which will be used to count the average weighted
    ##for the update process
    ## update pf,hp, up and dp according to the last flowID and the current
    # one using weighted average
    CSGroup_df = ContextualSummary.groupby(
        by=['multiple_label', 'Source','Destination']).total_sent_bytes.sum()
    CSGroup_df = CSGroup_df.reset_index()
    PRINT_MESSAGE="Updating contextual summaries"

    for i in range(len(CSGroup_df)):
        temp = pd.DataFrame(
            columns=identifiers + pf_format_flags + pf_format + pf_col + hp_col + up_col + dp_col)

        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(CSGroup_df)) * 100, 1)),
            end='\r')
        end_point = ContextualSummary[
            (ContextualSummary.multiple_label == CSGroup_df.loc[i, 'multiple_label']) & (
                        ContextualSummary.Source == CSGroup_df.loc[i, 'Source'])& (
                        ContextualSummary.Destination == CSGroup_df.loc[i, 'Destination'])]
        end_point = end_point.drop(columns="FlowID")
        end_point = end_point.reset_index(drop=True) # reset index
        end_point = end_point.reset_index(drop=False) # to use the new index as FlowID
        end_point=end_point.rename(columns={'index': "LastFlowID"})
        end_point.insert(0, 'CSID',
                           i)  # zero refer to the column position
        end_point['LastFlowID'] = len(end_point) - 1
        for id in identifiers:
            temp.loc[i, '{}'.format(id)] = end_point.loc[0,'{}'.format(id)]

        for flags in pf_format_flags:
            temp.loc[i, '{}'.format(flags)] = end_point['{}'.format(flags)].max() # max here can work as OR for all rows
        for pf_stat in pf_format+pf_col+hp_col+up_col+dp_col:
            temp.loc[i, '{}'.format(pf_stat)] = end_point['{}'.format(pf_stat)].mean() # max here can work as OR for all rows


        multiple_lists = end_point[average_features].values.tolist()
        arrays = [np.array(x) for x in multiple_lists]
        result = [np.mean(k) for k in zip(*arrays)]
        avg_features_counter=0
        for counter, transfer in enumerate(result):
            temp.loc[i, '{}'.format(average_features[avg_features_counter])] = transfer
            avg_features_counter+=1
        updated_cs=updated_cs.append(temp)
    return updated_cs






