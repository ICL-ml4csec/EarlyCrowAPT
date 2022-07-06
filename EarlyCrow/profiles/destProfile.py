def destination_features(_df):
    PRINT_MESSAGE="\n*** Destination Profile Features Extractions"
    print("{}".format(PRINT_MESSAGE))
    df_dest=_df.groupby(by=['multiple_label','Destination']).total_sent_bytes.sum()
    df_dest=df_dest.reset_index()

    ## No. host connected to a destination
    df_dest['DP_HostsConnected']=0
    PRINT_MESSAGE="Identify number of hosts connected to a destination"
    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        end_point = _df[(_df.multiple_label==df_dest.loc[i,'multiple_label']) & (
                    _df.Destination == df_dest.loc[i, 'Destination'])]
        df_dest.loc[i,'DP_HostsConnected']=len(end_point)
    print('{} - Done'.format(PRINT_MESSAGE))


    df_dest['DP_RecvSentBytes_Mean']=0
    df_dest['DP_RecvSentBytes_Max']=0
    df_dest['DP_RecvSentBytes_Min']=0

    PRINT_MESSAGE="Estimate recieved/sent bytes"
    ## Dst.Received/SentMax/Min/Averag
    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        end_point = _df[(_df.multiple_label==df_dest.loc[i,'multiple_label']) & (
                    _df.Destination == df_dest.loc[i, 'Destination'])]
        df_dest.loc[i,'DP_RecvSentBytes_Mean']=end_point.PF_RecvSentBytes.mean()
        df_dest.loc[i,'DP_RecvSentBytes_Max']=end_point.PF_RecvSentBytes.max()
        df_dest.loc[i,'DP_RecvSentBytes_Min']=end_point.PF_RecvSentBytes.min()
    print('{} - Done'.format(PRINT_MESSAGE))


    ## Dst.IdleTimeMax/Min/Mean

    df_dest['DP_IdleTime_Mean']=0
    df_dest['DP_IdleTime_Max']=0
    df_dest['DP_IdleTime_Min']=0
    PRINT_MESSAGE="Measure idle time"
    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        end_point = _df[(_df.multiple_label==df_dest.loc[i,'multiple_label']) & (
                    _df.Destination == df_dest.loc[i, 'Destination'])]
        df_dest.loc[i,'DP_IdleTime_Mean']=end_point.PF_Mean_idleTime.mean()
        df_dest.loc[i,'DP_IdleTime_Max']=end_point.PF_Mean_idleTime.max()
        df_dest.loc[i,'DP_IdleTime_Min']=end_point.PF_Mean_idleTime.min()
    print('{} - Done'.format(PRINT_MESSAGE))



    ## No of resumed connectionsper flow for a destination
    df_dest['DP_ResumedConnectionsNo_Mean']=0
    df_dest['DP_ResumedConnectionsNo_Max']=0
    df_dest['DP_ResumedConnectionsNo_Min']=0
    PRINT_MESSAGE="Resumed connections per destination"
    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        end_point = _df[(_df.multiple_label==df_dest.loc[i,'multiple_label']) & (
                    _df.Destination == df_dest.loc[i, 'Destination'])]
        df_dest.loc[i,'DP_ResumedConnectionsNo_Mean']=end_point.PF_ResumedConnectionsNo.mean()
        df_dest.loc[i,'DP_ResumedConnectionsNo_Max']=end_point.PF_ResumedConnectionsNo.max()
        df_dest.loc[i,'DP_ResumedConnectionsNo_Min']=end_point.PF_ResumedConnectionsNo.min()
    print('{} - Done'.format(PRINT_MESSAGE))



    ## No. of Distinct URLs associ-ated to Dst.


    df_dest['DP_Distinct_url_Mean']=0
    PRINT_MESSAGE="Count distinct URLs associated to a destination"
    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        end_point = _df[(_df.multiple_label==df_dest.loc[i,'multiple_label']) & (
                    _df.Destination == df_dest.loc[i, 'Destination'])]
        df_dest.loc[i,'DP_Distinct_url_Mean']=end_point.UP_Distinct_url.mean()
    print('{} - Done'.format(PRINT_MESSAGE))


    ## Dst. Max/Min/Mean PacketsFailure
    df_dest['DP_PacketFailure_Mean']=0
    df_dest['DP_PacketFailure_Max']=0
    df_dest['DP_PacketFailure_Min']=0
    _df['PacketFailure']=_df.PF_SCode_4xx + _df.PF_SCode_5xx
    PRINT_MESSAGE="Identify packet failures"
    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        end_point = _df[(_df.multiple_label==df_dest.loc[i,'multiple_label']) & (
                    _df.Destination == df_dest.loc[i, 'Destination'])]
        df_dest.loc[i,'DP_PacketFailure_Mean']=end_point.PacketFailure.mean()
        df_dest.loc[i,'DP_PacketFailure_Max']=end_point.PacketFailure.mean()
        df_dest.loc[i,'DP_PacketFailure_Min']=end_point.PacketFailure.mean()

    print('{} - Done'.format(PRINT_MESSAGE))


    ## No of DNS request per flowfor a destination
    df_dest['DP_dnsReqNo_Mean']=0
    df_dest['DP_dnsReqNo_Max']=0
    df_dest['DP_dnsReqNo_Min']=0
    df_dest['DP_dnsReqRatio_Mean']=0
    df_dest['DP_dnsReqRatio_Max']=0
    df_dest['DP_dnsReqRatio_Min']=0
    PRINT_MESSAGE="Calculate DNS requests and their ratio"

    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        end_point = _df[(_df.multiple_label==df_dest.loc[i,'multiple_label']) & (
                    _df.Destination == df_dest.loc[i, 'Destination'])]
        df_dest.loc[i,'DP_dnsReqNo_Mean']=end_point.PF_dnsReqNo.mean()
        df_dest.loc[i,'DP_dnsReqNo_Max']=end_point.PF_dnsReqNo.max()
        df_dest.loc[i,'DP_dnsReqNo_Min']=end_point.PF_dnsReqNo.min()

        df_dest.loc[
            i, 'DP_dnsReqRatio_Mean'] = end_point.PF_dnsReqRatio.mean()
        df_dest.loc[
            i, 'DP_dnsReqRatio_Max'] = end_point.PF_dnsReqRatio.max()
        df_dest.loc[
            i, 'DP_dnsReqRatio_Min'] = end_point.PF_dnsReqRatio.min()

        ## Transfer df_user to the main PairFlow

        dest_col = df_dest.columns
        dest_col = dest_col[3:]
        scalar_col = ['DP_HostsConnected','DP_RecvSentBytes_Mean', 'DP_RecvSentBytes_Max'
                    , 'DP_RecvSentBytes_Min', 'DP_IdleTime_Mean', 'DP_IdleTime_Max',
                      'DP_IdleTime_Min', 'DP_ResumedConnectionsNo_Mean', 'DP_ResumedConnectionsNo_Max'
                    ,'DP_ResumedConnectionsNo_Min', 'DP_Distinct_url_Mean',
                      'DP_PacketFailure_Mean','DP_PacketFailure_Max',
                    'DP_PacketFailure_Min', 'DP_dnsReqNo_Mean','DP_dnsReqNo_Max','DP_dnsReqNo_Min',
                    'DP_dnsReqRatio_Mean','DP_dnsReqRatio_Max','DP_dnsReqRatio_Min'
                    ,'DP_dnsReqNo_Mean','DP_dnsReqNo_Max','DP_dnsReqNo_Min',
                    'DP_dnsReqRatio_Mean','DP_dnsReqRatio_Max','DP_dnsReqRatio_Min']
    print('{} - Done'.format(PRINT_MESSAGE))

    PRINT_MESSAGE="Transfer destination profile features to the contextual summaries"
    for i in range(len(df_dest)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_dest)) * 100, 1)),
            end='\r')
        for col in scalar_col:
            _df.loc[(_df['multiple_label'] == df_dest.loc[
                    i, 'multiple_label']) &
                          (_df['Destination'] == df_dest.loc[i, 'Destination']),
                          '{}'.format(col)] = df_dest.loc[
                    i, '{}'.format(col)]

    print('{} - Done'.format(PRINT_MESSAGE))

    return _df