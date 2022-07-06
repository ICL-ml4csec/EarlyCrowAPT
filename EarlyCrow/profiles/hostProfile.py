import numpy as np
import re


def host_features(_df):
    # Windows XP = Windows NT 5.1, Windows Vista = Windows NT 6.0,
    # Windows 7 = Windows NT 6.1,  Windows 8 = Windows NT 6.2
    # Windows 8.1 = Windows NT 6.3, Windows 10 ==  Windows NT 10.0,
    OS= ['Windows NT 5.1','Windows NT 6.0','Windows NT 6.1','Windows NT 6.2',
         'Windows NT 6.3','Windows NT 10.0','Linux','Macintosh']
    browsers = ['MSIE','Chrome','Safari','Firefox',]
    renderingEngine = ['Trident','Presto','AppleWebKit', 'Gecko', 'KHTML']
    non_browser = ['Mozilla','Opera'] # check if it is  UA does not start with these strings, if it is it should be non browser

    ###############################################################

    def startwith(_df,_SERIES,_STR_REG,_COL):
        _df["P_temp"]=_df['{}'.format(_SERIES)].str.findall(_STR_REG)
        _df["P_temp"]=_df["P_temp"].apply(len)
        _df["startwith_{}".format(_COL)]=False
        _df["startwith_{}".format(_COL)].loc[_df['P_temp']>0]=True
        _df=_df.drop(columns=['P_temp'])
        return _df

    def Frac_UA_greater_x(_df_host,_serialized_ua_hist,_NUM_HOSTS):
        df_host['HP_Frac_UA_{}'.format(_NUM_HOSTS)] = 0
        PRINT_MESSAGE = "Identify the UAs usage among "

        for i in range(len(_df_host)):
            print(
                "{} {} hosts {}%".format(PRINT_MESSAGE,_NUM_HOSTS,
                                round((i / len(_df_host)) * 100, 1)),
                end='\r')
            UA_counter =0
            Distinct_UAs_per_host=_df_host.loc[i,'HP_Distinct_UAs_per_host']

            if len(_df_host.loc[i, 'HP_all_ua_per_host']) > 0:
                if len(_df_host.loc[i, 'HP_all_ua_per_host']) == 1:
                    #print("HERE")
                    if (_serialized_ua_hist[df_host.loc[i,'HP_all_ua_per_host'][0]] >=_NUM_HOSTS):
                        _df_host.loc[i, 'HP_Frac_UA_{}'.format(_NUM_HOSTS)]=1
                else:
                    for k in range(len(_df_host.loc[i, 'HP_all_ua_per_host'])):
                        # print(k)
                        if (_serialized_ua_hist[
                            _df_host.loc[i, 'HP_all_ua_per_host'][k]]  >=_NUM_HOSTS):
                            UA_counter +=1
                    _df_host.loc[i,'HP_Frac_UA_{}'.format(_NUM_HOSTS)] = UA_counter / Distinct_UAs_per_host
        print('{} {} hosts - Done'.format(PRINT_MESSAGE,_NUM_HOSTS))

        return _df_host


    def clean_str(_STR_CLEAN):
        _STR_CLEAN=_STR_CLEAN.replace("[","")
        _STR_CLEAN=_STR_CLEAN.replace("]","")
        _STR_CLEAN=_STR_CLEAN.replace("'","")
        return _STR_CLEAN

    def lowestVal(_a, _b, _c):
        if _a < _b:
            if _a < _c:
                return _a
            else:
                return _c
        else:
            if _b < _c:
                return _b
            else:
                return _c

    ################################################################
    #df=pd.read_csv(DATA, converters={'User_Agent': eval})
    #df_ua=df[['multiple_label','Source','Destination','User_Agent']]
    PRINT_MESSAGE="\n*** Host Profile Features Extractions"
    print("{}".format(PRINT_MESSAGE))
    df_ua=_df
    ################################################################
    # # # # # # #  # UA Features (Host-based # # # # # # # # # # # #
    ################################################################


    #### Todo:  Distinct_UAs_per_host, Avg_UAs_per_host, Min_UAs_per_host, Max_UAs_per_host
    df_host=_df.groupby(by=['multiple_label','Source']).total_sent_bytes.sum()
    df_host=df_host.reset_index()
    df_host['HP_all_ua_per_host']=np.nan
    df_host['HP_all_ua_per_host']=df_host['HP_all_ua_per_host'].astype('object')
    PRINT_MESSAGE="Dumping UAs for user"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,round((i/len(df_host))*100,1)), end='\r')
        end_point=_df[(_df.multiple_label==df_host.loc[i,'multiple_label']) & (_df.Source==df_host.loc[i,'Source']) ]
        end_point=end_point.reset_index(drop=True)

        all_ua=[]
        all_ua_per_host=[]
        for j in range(len(end_point)):
            if len(end_point.loc[j,'User_Agent']) >0 :
                if len(end_point.loc[j, 'User_Agent']) == 1:
                    all_ua.append(end_point.loc[j,'User_Agent'][0])
                else:
                    for k in range (len(end_point.loc[j,'User_Agent'])):
                        all_ua.append(end_point.loc[j, 'User_Agent'][k])
        all_ua_per_host=list(dict.fromkeys(all_ua))
        df_host.at[i, 'HP_all_ua_per_host'] = all_ua_per_host

    df_host['HP_Distinct_UAs_per_host']=df_host.HP_all_ua_per_host.apply(len)
    df_host['HP_Avg_UAs_per_host']=df_host['HP_Distinct_UAs_per_host'].mean()
    df_host['HP_Min_UAs_per_host']=df_host['HP_Distinct_UAs_per_host'].min()
    df_host['HP_Max_UAs_per_host']=df_host['HP_Distinct_UAs_per_host'].max()

    ### Todo: Feature: nAvg_UA_Popularity


    ua_analysis_df= df_host.copy(deep=True)
    ua_analysis_df=ua_analysis_df.reset_index(drop=True)
    serialized_ua_per_host_list=[]
    PRINT_MESSAGE="Seralize UAs per host"
    for i in range(len(ua_analysis_df)):
        print(
            "{} {}%".format(PRINT_MESSAGE,round((i/len(ua_analysis_df))*100,1)), end='\r')
        single_list=ua_analysis_df.loc[i,'HP_all_ua_per_host']
        for j in range(len(single_list)):
            serialized_ua_per_host_list.append(single_list[j])
    print('{} - Done'.format(PRINT_MESSAGE))

    from collections import Counter
    serialized_ua_hist=Counter(serialized_ua_per_host_list) # dict(ua:occurance)

    df_host[ 'HP_nAvg_UA_Popularity']=0
    PRINT_MESSAGE="Extract UAs popularity"
    for j in range(len(df_host)):
        nAvg=0
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((j / len(df_host)) * 100, 1)),
            end='\r')
        if len(df_host.loc[j, 'HP_all_ua_per_host']) > 0:
            if len(df_host.loc[j, 'HP_all_ua_per_host']) == 1:
                #print("HERE")
                nAvg=1/serialized_ua_hist[df_host.loc[j,'HP_all_ua_per_host'][0]]
                df_host.loc[j, 'HP_nAvg_UA_Popularity']=nAvg
            else:
                for k in range(len(df_host.loc[j, 'HP_all_ua_per_host'])):
                    # print(k)
                    if k>0:
                         nAvg= nAvg + 1 / serialized_ua_hist[
                            df_host.loc[j, 'HP_all_ua_per_host'][k]]
                    else: # for first element of many UAs
                        nAvg =  1 / serialized_ua_hist[
                            df_host.loc[j, 'HP_all_ua_per_host'][k]]
                df_host.loc[j,'HP_nAvg_UA_Popularity'] = nAvg
    print('{} - Done'.format(PRINT_MESSAGE))

    ## Todo: Frac_UA_1, Frac_UA_10: Fraction unpopular UAs used by 1 and ≤ 10 hosts

    #
    # first Match UA occurance among host using dict serialized_ua_hist,
    # if used by one host counter_UA1 +=1 , by more than 10  counter_UA10 +=1 ,
    # Second compute Frac_UA_1=  counter_UA1 / Distinct_UAs_per_host and
    #                Frac_UA_10= counter_UA10 / Distinct_UAs_per_host
    df_host[ 'HP_Frac_UA_1']=0
    df_host[ 'HP_Frac_UA_10']=0
    PRINT_MESSAGE="Identify the UAs usage at least one time"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')
        UA_1_counter =0
        Distinct_UAs_per_host=df_host.loc[i,'HP_Distinct_UAs_per_host']

        if len(df_host.loc[i, 'HP_all_ua_per_host']) > 0:
            if len(df_host.loc[i, 'HP_all_ua_per_host']) == 1:
                #print("HERE")
                if (serialized_ua_hist[df_host.loc[i,'HP_all_ua_per_host'][0]] ==1):
                    df_host.loc[i, 'HP_Frac_UA_1']=1
            else:
                for k in range(len(df_host.loc[i, 'HP_all_ua_per_host'])):
                    # print(k)
                    if (serialized_ua_hist[
                        df_host.loc[i, 'HP_all_ua_per_host'][k]] == 1):
                        UA_1_counter +=1
                df_host.loc[i,'HP_Frac_UA_1'] = UA_1_counter / Distinct_UAs_per_host
    print('{} - Done'.format(PRINT_MESSAGE))
    df_host=Frac_UA_greater_x(df_host,serialized_ua_hist,5)
    df_host=Frac_UA_greater_x(df_host,serialized_ua_hist,10)

    ## Todo: Ratio_UAs  Ratio UAs over hosts:

    df_host['HP_Ratio_UAs'] =df_host['HP_Distinct_UAs_per_host'] / len(serialized_ua_hist)

    ## Todo: avg OS per host
    os_str= "(Windows NT 5.1|Windows NT 6.0|Windows NT 6.1|Windows NT 6.2|" \
            "Windows NT 6.3|Windows NT 10.0|Linux|Macintosh)"
    pat=re.compile(r'{}'.format(os_str), re.IGNORECASE)
    df_host['HP_ua_osList']=np.nan
    df_host['HP_ua_osList']=df_host['HP_ua_osList'].astype('object')
    PRINT_MESSAGE="Average OS per host"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')

        os_list = []

        if len(df_host.loc[i, 'HP_all_ua_per_host']) > 0:
            if len(df_host.loc[i, 'HP_all_ua_per_host']) >= 1:
                for j in range(len(df_host.loc[i, 'HP_all_ua_per_host'])):
                    str_temp=df_host.loc[i, 'HP_all_ua_per_host'][j]
                    res=pat.findall(str_temp)
                    if (len(res)) !=0:
                        os_list.append(res[0]) # it is one for each UA
                os_list=list(dict.fromkeys(os_list))
                df_host.at[i,'HP_ua_osList'] = os_list

    df_host['HP_Avg_OS']= df_host['HP_ua_osList'].dropna().apply(len).mean()
    print('{} - Done'.format(PRINT_MESSAGE))

    for i in range(len(df_host)):
        try:
            df_host.loc[i,'HP_OS_per_host']=len(df_host.loc[i,'HP_ua_osList'])
        except:
            pass

    ## Todo: dominant_OS
    df_host['HP_ua_osList_str']=df_host['HP_ua_osList'].dropna().astype(str)
    ua_osList_str=df_host['HP_ua_osList'].dropna().astype(str)
    ua_osList_str=ua_osList_str.value_counts()
    ua_osList_str=ua_osList_str.reset_index()


    dominant_OS_list=[]
    for i in range(len(ua_osList_str)):
        dominant_OS=ua_osList_str.loc[i,'index']
        dominant_OS=clean_str(dominant_OS)
        if len(dominant_OS)!=0:
            dominant_OS_list.append(dominant_OS)

    df_host['HP_dominant_OS1_{}'.format(dominant_OS_list[0])]=df_host.HP_ua_osList_str.str.contains(dominant_OS_list[0])
    df_host['HP_dominant_OS2_{}'.format(dominant_OS_list[1])]=df_host.HP_ua_osList_str.str.contains(dominant_OS_list[1])



    ## Todo: avg browsers per host
    #browsers = ['MSIE','Chrome','Safari','Firefox','Opera']

    browsers_str= "(MSIE|Chrome|Safari|Firefox|Opera)"
    pat=re.compile(r'{}'.format(browsers_str), re.IGNORECASE)
    df_host['HP_ua_browserList']=np.nan
    df_host['HP_ua_browserList']=df_host['HP_ua_browserList'].astype('object')

    for i in range(len(df_host)):
        PRINT_MESSAGE="Average Browser per host"
        browser_list = []
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')

        if len(df_host.loc[i, 'HP_all_ua_per_host']) > 0:
            if len(df_host.loc[i, 'HP_all_ua_per_host']) >= 1:
                for j in range(len(df_host.loc[i, 'HP_all_ua_per_host'])):
                    str_temp=df_host.loc[i, 'HP_all_ua_per_host'][j]
                    res=pat.findall(str_temp)
                    if (len(res)) !=0:
                        browser_list.append(res[0]) # it is one for each UA
                browser_list=list(dict.fromkeys(browser_list))
                df_host.at[i,'HP_ua_browserList'] = browser_list

    df_host['HP_Avg_Browsers']= df_host['HP_ua_browserList'].dropna().apply(len).mean()
    print('{} - Done'.format(PRINT_MESSAGE))

    for i in range(len(df_host)):
        try:
            df_host.loc[i,'HP_Browsers_per_host']=len(df_host.loc[i,'HP_ua_browserList'])
        except:
            pass


    ## Todo: dominant_browser

    df_host['HP_ua_browserList_str']=df_host['HP_ua_browserList'].dropna().astype(str)
    ua_browserList_str=df_host['HP_ua_browserList'].dropna().astype(str)
    ua_browserList_str=ua_browserList_str.value_counts()
    ua_browserList_str=ua_browserList_str.reset_index()
    dominant_Browser_list=[]

    for i in range(len(ua_browserList_str)):
        dominant_Browser=ua_browserList_str.loc[i,'index']
        dominant_Browser=clean_str(dominant_Browser)
        if len(dominant_Browser)!=0:
            dominant_Browser_list.append(dominant_Browser)

    df_host['HP_dominant_Browser1_{}'.format(dominant_Browser_list[0])]=df_host.HP_ua_browserList_str.str.contains(dominant_Browser_list[0])
    df_host['HP_dominant_Browser2_{}'.format(dominant_Browser_list[1])]=df_host.HP_ua_browserList_str.str.contains(dominant_Browser_list[1])


    ## Max, Min, Mean HP_ResumedConnectionsNo No of resumed connections per flow for a host

    df_host['HP_MeanResumedConnections'] = 0
    df_host['HP_MaxResumedConnections'] = 0
    df_host['HP_MinResumedConnections'] = 0
    PRINT_MESSAGE="Resumed connections per host"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')
        end_point = _df[
            (_df.multiple_label == df_host.loc[i, 'multiple_label']) & (
                        _df.Source == df_host.loc[i, 'Source'])]
        end_point = end_point.reset_index(drop=True)
        df_host.loc[
            i, 'HP_MeanResumedConnections'] = end_point.PF_ResumedConnectionsNo.mean()
        df_host.loc[
            i, 'HP_MaxResumedConnections'] = end_point.PF_ResumedConnectionsNo.max()
        df_host.loc[
            i, 'HP_MinResumedConnections'] = end_point.PF_ResumedConnectionsNo.min()
    print('{} - Done'.format(PRINT_MESSAGE))

    ## Max/Min/Mean time between new destination,
    ## we use control, udp and icmp planes to find the first packet for each
    ## flow and compute the statstics Max/Min/Mean
    PRINT_MESSAGE="Max/Min/Mean time between new destination"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')
        end_point = _df[
            (_df.multiple_label == df_host.loc[i, 'multiple_label']) & (
                        _df.Source == df_host.loc[i, 'Source'])]
        end_point = end_point.reset_index(drop=True)

        cp_timestamp_list = []
        udpp_timestamp_list = []
        icmpp_timestamp_list = []
        earlyfirst = []
        PADDING = 999999

        for j in range(len(end_point)):
            try:
                cp_timestamp_list.append(
                    end_point.loc[j, 'control_plane'][0][
                        2])  # relative time locate at 2 on control plane
            except:
                cp_timestamp_list.append(PADDING)
            try:
                udpp_timestamp_list.append(
                    end_point.loc[j, 'udp_plane'][0][
                        3])  # relative time locate at 3 on udp plane
            except:
                udpp_timestamp_list.append(PADDING)

            try:
                icmpp_timestamp_list.append(
                    end_point.loc[j, 'icmp_plane'][0][
                        3])  # relative time locate at 3 on icmp plane
            except:
                icmpp_timestamp_list.append(PADDING)

        for k in range(len(cp_timestamp_list)):
            earlyfirst.append(
                lowestVal(cp_timestamp_list[k], udpp_timestamp_list[k],
                          icmpp_timestamp_list[k]))
        earlyfirst.sort()

        # calculate Mean Time Difference of Sequenced Connections MTDSC 1/n Segma t_i+1 - t_i
        TimeDiff = []
        MTDSC = 0
        MinTDSC = 0
        MaxTDSC = 0
        for k in range(len(earlyfirst) - 1):
            MTDSC = MTDSC + (earlyfirst[k + 1] - earlyfirst[k])
        MTDSC = MTDSC / len(earlyfirst)

        for k in range(len(earlyfirst) - 1):
            TimeDiff.append(earlyfirst[k + 1] - earlyfirst[k])
        if len(
                TimeDiff) != 0:  ## means there is  one pairflow for a host
            MinTDSC = min(TimeDiff)
            MaxTDSC = max(TimeDiff)
        df_host.loc[i, 'HP_MTDSC'] = MTDSC
        df_host.loc[i, 'HP_MinTDSC'] = MinTDSC
        df_host.loc[i, 'HP_MaxTDSC'] = MaxTDSC
    print('{} - Done'.format(PRINT_MESSAGE))

    ## No of DNS request per flow for a host
    df_host['HP_dnsReq_perflow'] = 0
    PRINT_MESSAGE="DNS requests per host"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')
        end_point = _df[
            (_df.multiple_label == df_host.loc[i, 'multiple_label']) & (
                        _df.Source == df_host.loc[i, 'Source'])]
        end_point = end_point.reset_index(drop=True)
        df_host.loc[i, 'HP_dnsReq_perflow'] = end_point.PF_dnsReqNo.mean()
    print('{} - Done'.format(PRINT_MESSAGE))

    ## Ratio of Connected Destination by IP only
    df_host['HP_DestByIP'] = 0
    PRINT_MESSAGE="Identify connections to remote server with IP only"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')
        end_point = _df[
            (_df.multiple_label == df_host.loc[i, 'multiple_label']) & (
                        _df.Source == df_host.loc[i, 'Source'])]
        end_point = end_point.reset_index(drop=True)
        end_point['NoFQDN'] = end_point['fqdn_lists'].apply(len)

        df_host.loc[i, 'HP_DestByIP'] = len(
            end_point[end_point['NoFQDN'] == 0]) / len(end_point)
    print('{} - Done'.format(PRINT_MESSAGE))

    ## Transfer df_user to the main PairFlow
    df_host=df_host.drop(columns=['HP_ua_osList_str','HP_ua_browserList_str'])
    host_col=df_host.columns
    host_col=host_col[3:]
    host_col=host_col[3:]
    scalar_col=[ 'HP_Distinct_UAs_per_host', 'HP_Avg_UAs_per_host',
           'HP_Min_UAs_per_host', 'HP_Max_UAs_per_host', 'HP_nAvg_UA_Popularity',
           'HP_Frac_UA_1', 'HP_Frac_UA_10', 'HP_Frac_UA_5', 'HP_Ratio_UAs',
           'HP_Avg_OS', 'HP_OS_per_host', 'HP_dominant_OS1_{}'.format(dominant_OS_list[0]),
            'HP_dominant_OS2_{}'.format(dominant_OS_list[1]),  'HP_Avg_Browsers',
           'HP_Browsers_per_host', 'HP_dominant_Browser1_{}'.format(dominant_Browser_list[0]),
                 'HP_dominant_Browser2_{}'.format(dominant_Browser_list[1]),
            'HP_MeanResumedConnections','HP_MaxResumedConnections','HP_MinResumedConnections'
                 ,'HP_MTDSC','HP_MinTDSC','HP_MinTDSC','HP_dnsReq_perflow','HP_DestByIP']

    PRINT_MESSAGE="Transfer features to the contextual summaries"
    for i in range(len(df_host)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(df_host)) * 100, 1)),
            end='\r')
        for col in  scalar_col:
            df_ua.loc[(df_ua['multiple_label'] == df_host.loc[i, 'multiple_label']) &
                              (df_ua['Source'] == df_host.loc[i, 'Source']) ,
                              '{}'.format(col)] = df_host.loc[i, '{}'.format(col)]

    print('{} - Done'.format(PRINT_MESSAGE))

    return _df,df_host

