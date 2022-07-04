
pf_col_http=['PF_TotalBytes',
       'PF_RecvSentBytes', 'PF_total_packets', 'PF_tcpRatio', 'PF_udpRatio',
       'PF_icmpRatio', 'PF_dnsRatio', 'PF_httpRatio', 'PF_encryptedRatio',
       'PF_SCode_1xx', 'PF_SCode_2xx', 'PF_SCode_3xx', 'PF_SCode_4xx',
       'PF_SCode_5xx', 'PF_cf_js', 'PF_cf_html', 'PF_cf_image', 'PF_cf_video',
       'PF_cf_app', 'PF_cf_text',  'PF_GET_freq', 'PF_POST_freq',
       'PF_total_SCode', 'PF_SCode_1xxRatio', 'PF_SCode_2xxRatio',
       'PF_SCode_3xxRatio', 'PF_SCode_4xxRatio', 'PF_SCode_5xxRatio',
       'PF_total_getpost', 'PF_GET_ratio', 'PF_POST_ratio',
       'PF_ResumedConnectionsNo', 'PF_dnsReqNo',
       'PF_dnsReqRatio', 'PF_Delta_Time_max', 'PF_Delta_Time_min',
       'PF_Delta_Time_mean', 'PF_Delta_Time_median',
       'PF_Content_Length_Total', 'PF_Content_Length_min',
       'PF_Content_Length_max','PF_Content_Length_median', 'PF_total_cf', 'PF_cf_jsRatio',
       'PF_cf_htmlRatio', 'PF_cf_imageRatio', 'PF_cf_videoRatio',
       'PF_cf_appRatio', 'PF_cf_textRatio',
       'PF_No_belowAVG', 'PF_No_aboveAVG', 'PF_ratio_aboveAvg',
       'PF_ratio_belowAvg', 'PF_No_outliers', 'PF_ratio_outliers',
       'PF_magnitudeMax_outliers', 'PF_magnitudeMin_outliers',
       'PF_magnitudeMean_outliers', 'PF_magnitudeStd_outliers',
       'PF_Max_idleTime', 'PF_Min_idleTime', 'PF_Mean_idleTime']

pf_col_https=['PF_TotalBytes',
       'PF_RecvSentBytes', 'PF_total_packets', 'PF_tcpRatio', 'PF_udpRatio',
       'PF_icmpRatio', 'PF_dnsRatio', 'PF_httpRatio', 'PF_encryptedRatio',
       'PF_ResumedConnectionsNo', 'PF_dnsReqNo',
       'PF_dnsReqRatio', 'PF_Delta_Time_max', 'PF_Delta_Time_min',
       'PF_Delta_Time_mean', 'PF_Delta_Time_median',
       'PF_No_belowAVG', 'PF_No_aboveAVG', 'PF_ratio_aboveAvg',
       'PF_ratio_belowAvg', 'PF_No_outliers', 'PF_ratio_outliers',
       'PF_magnitudeMax_outliers', 'PF_magnitudeMin_outliers',
       'PF_magnitudeMean_outliers', 'PF_magnitudeStd_outliers',
'PF_Max_idleTime', 'PF_Min_idleTime', 'PF_Mean_idleTime'
       ]

hp_http=[
       'HP_MeanResumedConnections', 'HP_MaxResumedConnections',
       'HP_MinResumedConnections', 'HP_MTDSC', 'HP_MinTDSC',
       'HP_dnsReq_perflow', 'HP_DestByIP']
hp_https=[
       'HP_MeanResumedConnections', 'HP_MaxResumedConnections',
       'HP_MinResumedConnections', 'HP_MTDSC', 'HP_MinTDSC',
       'HP_dnsReq_perflow', 'HP_DestByIP']




up_col=['UP_Distinct_url',
        'UP_Num_Filename', 'UP_num_exe', 'UP_Frac_query',
       'UP_Frac_URL_filename', 'UP_Frac_URL_filename_exe', 'UP_URL_Length_Max',
       'UP_URL_Length_Min', 'UP_URL_Length_Mean', 'UP_Depth_Max',
       'UP_Depth_Min', 'UP_Depth_Mean', 'UP_No_Para_Max', 'UP_No_Para_Min',
       'UP_No_Para_Mean', 'UP_No_Values_Max', 'UP_No_Values_Min',
       'UP_No_Values_Mean']

up_col_excluded=[
       'UP_Num_hasString',  'UP_No_Values_Mean', 'UP_No_Frag_Max', 'UP_No_Frag_Min',
       'UP_No_Frag_Mean']

dp_col=['DP_HostsConnected',
       'DP_RecvSentBytes_Mean', 'DP_RecvSentBytes_Max', 'DP_RecvSentBytes_Min',
       'DP_IdleTime_Mean', 'DP_IdleTime_Max', 'DP_IdleTime_Min',
       'DP_ResumedConnectionsNo_Mean', 'DP_ResumedConnectionsNo_Max',
       'DP_ResumedConnectionsNo_Min', 'DP_Distinct_url_Mean',
       'DP_PacketFailure_Mean', 'DP_PacketFailure_Max', 'DP_PacketFailure_Min',
       'DP_dnsReqNo_Mean', 'DP_dnsReqNo_Max', 'DP_dnsReqNo_Min',
       'DP_dnsReqRatio_Mean', 'DP_dnsReqRatio_Max', 'DP_dnsReqRatio_Min']

dp_col_https=['DP_HostsConnected',
       'DP_RecvSentBytes_Mean', 'DP_RecvSentBytes_Max', 'DP_RecvSentBytes_Min',
       'DP_IdleTime_Mean', 'DP_IdleTime_Max', 'DP_IdleTime_Min',
       'DP_ResumedConnectionsNo_Mean', 'DP_ResumedConnectionsNo_Max',
       'DP_ResumedConnectionsNo_Min',

       'DP_dnsReqNo_Mean', 'DP_dnsReqNo_Max', 'DP_dnsReqNo_Min',
       'DP_dnsReqRatio_Mean', 'DP_dnsReqRatio_Max', 'DP_dnsReqRatio_Min']


MADE=['Content_Length_Total',
       'Content_Length_min', 'Content_Length_max', 'Content_Length_median',
       'total_bytes', 'total_sent_bytes', 'total_recv_bytes','PF_TotalBytes',
       'PF_RecvSentBytes', 'PF_SCode_1xx', 'PF_SCode_2xx', 'PF_SCode_3xx', 'PF_SCode_4xx',
       'PF_SCode_5xx', 'PF_cf_js', 'PF_cf_html', 'PF_cf_image', 'PF_cf_video',
       'PF_cf_app', 'PF_cf_text', 'PF_GET_freq', 'PF_POST_freq',
       'PF_total_SCode', 'PF_SCode_1xxRatio', 'PF_SCode_2xxRatio',
       'PF_SCode_3xxRatio', 'PF_SCode_4xxRatio', 'PF_SCode_5xxRatio',
       'PF_total_getpost', 'PF_GET_ratio', 'PF_POST_ratio','PF_Content_Length_Total', 'PF_Content_Length_min',
       'PF_Content_Length_max','PF_Content_Length_median', 'PF_total_cf', 'PF_cf_jsRatio',
       'PF_cf_htmlRatio', 'PF_cf_imageRatio', 'PF_cf_videoRatio',
       'PF_cf_appRatio', 'PF_cf_textRatio', 'UP_Distinct_url',
        'UP_Num_Filename',  'UP_Frac_query',
       'UP_Frac_URL_filename', 'UP_Frac_URL_filename_exe', 'UP_URL_Length_Max',
       'UP_URL_Length_Min', 'UP_URL_Length_Mean', 'UP_Depth_Max',
       'UP_Depth_Min', 'UP_Depth_Mean', 'UP_No_Para_Max', 'UP_No_Para_Min',
       'UP_No_Para_Mean', 'UP_No_Values_Max', 'UP_No_Values_Min',
       'UP_No_Values_Mean','HP_Distinct_UAs_per_host',
        'HP_Ratio_UAs']

MADE_https=[
       'total_bytes', 'total_sent_bytes', 'total_recv_bytes','PF_TotalBytes',
       'PF_RecvSentBytes',
       'PF_total_getpost', 'PF_GET_ratio', 'PF_POST_ratio']