import pandas as pd
import numpy as np

import re
PAT_HTML="html"
PAT_APP="application"
PAT_JAVA="java"
PAT_GENERIC_TEXT="text"
PAT_EMPTY="Empty"
PAT_IMG="image"
PAT_VIDEO="video"
NONE_CT='None'
re_html=re.compile(PAT_HTML)
re_app=re.compile(PAT_APP)
re_java=re.compile(PAT_JAVA)
re_gtext=re.compile(PAT_GENERIC_TEXT)
re_empty=re.compile(PAT_EMPTY)
re_img=re.compile(PAT_IMG)
re_video=re.compile(PAT_VIDEO)


def pairflow_features(_df):
    def create_bins(lower_bound, width, quantity):

        bins = []
        for low in range(lower_bound,
                         lower_bound + quantity * width + 1, width):
            bins.append(low)
        return bins

    def initlist(n):
        list_init = [0] * n
        return list_init
    PRINT_MESSAGE="*** PairFlow Features Extractions"
    print("{}".format(PRINT_MESSAGE))
    ## Statstical Behaviour
    ## Related PairFlow Format: 'total_bytes', 'total_sent_bytes', 'total_recv_bytes'
    ##'SCode_1xx', 'SCode_2xx', 'SCode_3xx', 'SCode_4xx', 'SCode_5xx'
    ##'tcp_packets', 'udp_packets', 'icmp_packets', 'http_packets', 'tls_packets',
    ## 'ssl_packets', 'dns_packets', 'GET_freq', 'POST_freq'
    PRINT_MESSAGE="Estimate exchange bytes and packets number and ratio for each protocol"
    # TotalBytes, SentRecvBytes
    _df['PF_TotalBytes'] = _df['total_bytes']
    _df['PF_RecvSentBytes'] = _df['total_recv_bytes']/  _df['total_sent_bytes']



    # tcpRatio, udpRatio, icmpRatio, dnsRatio, httpRatio, encryptedRatio
    packetStat= ['tcp_packets', 'udp_packets', 'icmp_packets', 'http_packets', 'tls_packets',
    'ssl_packets', 'dns_packets']
    _df['PF_total_packets']=0
    for ps in packetStat:
        _df['PF_total_packets'] += _df["{}".format(ps)]

    _df['PF_tcpRatio'] = _df['tcp_packets'] / _df['PF_total_packets']
    _df['PF_udpRatio'] = _df['udp_packets'] / _df['PF_total_packets']
    _df['PF_icmpRatio'] = _df['icmp_packets'] / _df['PF_total_packets']
    _df['PF_dnsRatio'] = _df['dns_packets'] / _df['PF_total_packets']
    _df['PF_httpRatio'] = _df['http_packets'] / _df['PF_total_packets']
    _df['PF_encryptedRatio'] = (_df['tls_packets'] + _df['ssl_packets'] ) / _df['PF_total_packets']
    print("{} - Done".format(PRINT_MESSAGE))

    # SCode_1xxRatio, SCode_2xxRatio, SCode_3xxRatio, SCode_4xxRatio, SCode_5xxRatio
    PRINT_MESSAGE = "Count GET/POST, SCodeXXX, Content Type"
    for i in range(len(_df)):

        SCode_1xx = SCode_2xx = SCode_3xx = \
            SCode_4xx = SCode_5xx = cf_js = \
            cf_html = cf_image = cf_video = cf_app \
            = cf_text = cf_empty = \
            GET_freq = POST_freq = 0

        print(
            "{} {}%".format(PRINT_MESSAGE,round((i/len(_df))*100,1)), end='\r')
        if len(_df.loc[i, 'data_plane']) !=0:
            for j in range(len(_df.loc[i, 'data_plane'])):
                str_code=""
                if len(str(_df.loc[i, 'data_plane'][j][3]))!=0:
                    str_code = str(_df.loc[i, 'data_plane'][j][3])[0]
                if str_code == "1":
                    SCode_1xx += 1
                elif str_code == "2":
                    SCode_2xx += 1

                elif str_code == "3":
                    SCode_3xx += 1

                elif str_code == "4":
                    SCode_4xx += 1

                elif str_code == "5":
                    SCode_5xx += 1

                elif str_code == "G":
                    GET_freq += 1

                elif str_code == "P":
                    POST_freq += 1

                str_ct = _df.loc[i, 'data_plane'][j][4]
                if "{}".format(re_java.search(str_ct))!=NONE_CT:
                    cf_js += 1

                elif "{}".format(re_html.search(str_ct))!=NONE_CT:
                    cf_html += 1

                elif "{}".format(re_img.search(str_ct))!=NONE_CT:
                    cf_image += 1

                elif "{}".format(re_video.search(str_ct)) !=NONE_CT:
                    cf_video += 1

                elif "{}".format(re_app.search(str_ct)) !=NONE_CT:
                    cf_app += 1

                elif "{}".format(re_gtext.search(str_ct)) !=NONE_CT:
                    cf_text += 1


        tl_idx = 0
        transfer_list = [SCode_1xx, SCode_2xx, SCode_3xx,
                         SCode_4xx, SCode_5xx, cf_js,
                         cf_html, cf_image, cf_video, cf_app
            , cf_text,
                         GET_freq, POST_freq]

        transfer_list_name = ['SCode_1xx', 'SCode_2xx', 'SCode_3xx',
                              'SCode_4xx', 'SCode_5xx', 'cf_js',
                              'cf_html', 'cf_image', 'cf_video',
                              'cf_app'
            , 'cf_text',
                              'GET_freq', 'POST_freq']

        for tl in transfer_list_name:
            _df.loc[i,"PF_" + tl] = transfer_list[tl_idx]
            tl_idx += 1
    print('{} - Done'.format(PRINT_MESSAGE))
    packetSCode= ['PF_SCode_1xx', 'PF_SCode_2xx', 'PF_SCode_3xx', 'PF_SCode_4xx', 'PF_SCode_5xx']
    _df['PF_total_SCode']=0
    for psc in packetSCode:
        _df['PF_total_SCode']+=_df[psc] # total packets with status code response


    _df['PF_SCode_1xxRatio'] = _df['PF_SCode_1xx'] / _df['PF_total_SCode']
    _df['PF_SCode_2xxRatio'] = _df['PF_SCode_2xx'] / _df['PF_total_SCode']
    _df['PF_SCode_3xxRatio'] = _df['PF_SCode_3xx'] / _df['PF_total_SCode']
    _df['PF_SCode_4xxRatio'] = _df['PF_SCode_4xx'] / _df['PF_total_SCode']
    _df['PF_SCode_5xxRatio'] = _df['PF_SCode_5xx'] / _df['PF_total_SCode']
    NO_STATUSCODE=0
    _df = _df.fillna({'PF_SCode_1xxRatio': NO_STATUSCODE,
                      'PF_SCode_2xxRatio': NO_STATUSCODE,
                      'PF_SCode_3xxRatio': NO_STATUSCODE,
                      'PF_SCode_4xxRatio': NO_STATUSCODE,
                      'PF_SCode_5xxRatio': NO_STATUSCODE,
                      })
    # GET_ratio, POST_ratio, POST_GET_ratio
    _df['PF_total_getpost']= _df['PF_GET_freq']+ _df['PF_POST_freq']
    _df['PF_GET_ratio'] = _df['PF_GET_freq'] / _df['PF_total_getpost']
    _df['PF_POST_ratio'] = _df['PF_POST_freq'] / _df['PF_total_getpost']
    _df['PF_POST_GET_ratio'] = _df['PF_POST_freq'] / _df['PF_GET_freq']
    NO_GET_POST=0
    _df = _df.fillna({'PF_GET_ratio': NO_GET_POST,
                      'PF_POST_ratio': NO_GET_POST,
                      })

    # ResumedConnectionsNo
    # each connection start with syn, synack, ack so it has the following sequence flags: (0x002, 0x012, 0x010)  or we can count finack 0x011
    # both deduced with -1 to count the resumed connections, we use the latter for lower computation purpose
    _df['PF_ResumedConnectionsNo']=0
    for i in range(len(_df)):
        ResumedConnectionsNo= 0
        PRINT_MESSAGE="Caculate resumed connections between two end points"
        print(
            "{} {}%".format(PRINT_MESSAGE,round((i/len(_df))*100,1)), end='\r')
        for j in range(len(_df.loc[i,'control_plane'])):
            if (_df.loc[i,'control_plane'][j][1] == '0x011'):
                    ResumedConnectionsNo+=1

        _df.loc[i,'PF_ResumedConnectionsNo']=ResumedConnectionsNo -1 # so for those -1 means the connection never terminated during time window of pairflow
    print('{} - Done'.format(PRINT_MESSAGE))

    # dnsReqRatio
    PRINT_MESSAGE = "Caculate DNS requests and their ratio from UDP plane"

    _df['PF_dnsReqNo']=0
    for i in range(len(_df)):
        dnsReqNo= 0
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(_df)) * 100, 1)),
            end='\r')
        for j in range(len(_df.loc[i,'udp_plane'])):
            if (_df.loc[i,'udp_plane'][j][2] == 'DNS_Request'):
                    dnsReqNo+=1

        _df.loc[i,'PF_dnsReqNo']=dnsReqNo

    _df['PF_dnsReqRatio'] = _df['PF_dnsReqNo']/_df['PF_total_packets']
    print('{} - Done'.format(PRINT_MESSAGE))



    ## Time-based Analysis
    ## Related PairFlow Format: 'TTL_max', 'TTL_min', 'TTL_mean', 'TTL_median',
    ##       'Delta_Time_max', 'Delta_Time_min', 'Delta_Time_mean',
    ##       'Delta_Time_median', 'Duration'
    _df['PF_TTL_max'] = _df['TTL_max']
    _df['PF_TTL_min'] = _df['TTL_min']
    _df['PF_TTL_mean'] = _df['TTL_mean']
    _df['PF_TTL_median'] = _df['TTL_median']
    _df['PF_Delta_Time_max'] = _df['Delta_Time_max']
    _df['PF_Delta_Time_min'] = _df['Delta_Time_min']
    _df['PF_Delta_Time_mean'] = _df['Delta_Time_mean']
    _df['PF_Delta_Time_median'] = _df['Delta_Time_median']
    _df['PF_Duration'] = _df['Duration']

    ## Time Series Analysis
    ## Related PairFlow Format: control_plane, data_plane, udp_plane

    ## Content Analysis
    ## Related PairFlow Format: 'Content_Length_Total', 'Content_Length_min',
    ## 'Content_Length_max','Content_Length_median', 'cf_js', 'cf_html',
    ##  'cf_image', 'cf_video', 'cf_app', 'cf_text'

    # 'Content_Length_Total', 'Content_Length_min', 'Content_Length_max', 'Content_Length_median'
    _df['PF_Content_Length_Total'] = _df['Content_Length_Total']
    _df['PF_Content_Length_min'] = _df['Content_Length_min']
    _df['PF_Content_Length_max'] = _df['Content_Length_max']
    _df['PF_Content_Length_median'] = _df['Content_Length_median']

    # cf_jsRatio, cf_htmlRatio, cf_imageRatio, cf_videoRatio, cf_appRatio, cf_textRatio
    cf_type= ['PF_cf_js', 'PF_cf_html','PF_cf_image', 'PF_cf_video', 'PF_cf_app', 'PF_cf_text']
    _df['PF_total_cf']=0
    for cf in cf_type:
        _df['PF_total_cf']+=_df[cf] # total packets with of all http content

    _df['PF_cf_jsRatio'] = _df['PF_cf_js'] / _df['PF_total_cf']
    _df['PF_cf_htmlRatio'] = _df['PF_cf_html'] / _df['PF_total_cf']
    _df['PF_cf_imageRatio'] = _df['PF_cf_image'] / _df['PF_total_cf']
    _df['PF_cf_videoRatio'] = _df['PF_cf_video'] / _df['PF_total_cf']
    _df['PF_cf_appRatio'] = _df['PF_cf_app'] / _df['PF_total_cf']
    _df['PF_cf_textRatio'] = _df['PF_cf_text'] / _df['PF_total_cf']

    NO_CONTENT=0
    _df = _df.fillna({'PF_cf_jsRatio': NO_CONTENT,
                      'PF_cf_htmlRatio': NO_CONTENT,
                      'PF_cf_imageRatio': NO_CONTENT,
                      'PF_cf_videoRatio': NO_CONTENT,
                      'PF_cf_appRatio': NO_CONTENT,
                      'PF_cf_textRatio': NO_CONTENT,
                      })
    ########## Time-based Features



    WIDTH = 1 # sec
    INTERVAL=60 # sec
    window_size = int(INTERVAL / WIDTH) # because width is 10 sec, Inteval = 60, so window size is 60/10 = 6 means, it has 6 unit each represent 10 sec equal to 1 minute
    #window_size = int(window_size)
    PRINT_MESSAGE = "Analyzing Time-Based Flows"

    for i in range(len(_df)):
        packetLength_list = []
        arrival_time = []
        arrival_time_reset = []
        arrival_diff_list = []
        print("{} {}%".format(PRINT_MESSAGE,round((i/len(_df))*100,1)), end='\r')
        ######### First we calculate Idle Time
        for j in range(len(_df.loc[i, 'data_plane'])):
            packetLength_list.append(_df.loc[i, 'data_plane'][j][6])
            arrival_time.append(_df.loc[i, 'data_plane'][j][5])

            arrival_diff_list.append(_df.loc[i, 'data_plane'][j][5] -
                                     _df.loc[i, 'data_plane'][j - 1][5])

        ######### Second we calculate Moving Average
        arrival_time_reset[:] = [arr_time - arrival_time[0] for arr_time
                                 in
                                 arrival_time]  # subtract the first element from all values for easier binning

        if len(arrival_time_reset) > 0:
            bins = create_bins(lower_bound=0,
                               width=WIDTH,
                               quantity=np.ceil(
                                   arrival_time_reset[-1]/WIDTH).astype(
                                   int))
        else:
            bins = []
        packetLengthBinned = initlist(len(bins))
        arr_idx = 0
        for binidx in range(len(bins)):
            while arrival_time_reset[arr_idx] <= bins[binidx]:
                packetLengthBinned[binidx] = packetLengthBinned[
                                                 binidx] + \
                                             packetLength_list[arr_idx]
                arr_idx += 1
                if arr_idx == len(arrival_time_reset):
                    break

        numbers_series = pd.Series(packetLengthBinned)
        windows = numbers_series.rolling(window_size)
        moving_averages = windows.mean()
        moving_averages = moving_averages.fillna(numbers_series)
        diff = numbers_series - moving_averages
        No_belowAVG = len(diff[diff < 0])
        No_aboveAVG = len(diff[diff > 0])
        ratio_aboveAvg = 0
        ratio_belowAvg = 0
        if len(numbers_series) != 0:
            ratio_aboveAvg = No_aboveAVG / len(numbers_series)
            ratio_belowAvg = No_belowAVG / len(numbers_series)
        outliers_bool = numbers_series > 2 * moving_averages
        No_outliers = len(outliers_bool[outliers_bool == True])
        ratio_outliers = 0
        if len(numbers_series) != 0:
            ratio_outliers = No_outliers / len(numbers_series)
        magnitudeMax_outliers = numbers_series[outliers_bool].max()
        magnitudeMin_outliers = numbers_series[outliers_bool].min()
        magnitudeMean_outliers = numbers_series[outliers_bool].mean()
        magnitudeStd_outliers = numbers_series[outliers_bool].std()

        _df.loc[i, 'PF_No_belowAVG'] = No_belowAVG
        _df.loc[i, 'PF_No_aboveAVG'] = No_aboveAVG
        _df.loc[i, 'PF_ratio_aboveAvg'] = ratio_aboveAvg
        _df.loc[i, 'PF_ratio_belowAvg'] = ratio_belowAvg
        _df.loc[i, 'PF_No_outliers'] = No_outliers
        _df.loc[i, 'PF_ratio_outliers'] = ratio_outliers
        _df.loc[i, 'PF_magnitudeMax_outliers'] = magnitudeMax_outliers
        _df.loc[i, 'PF_magnitudeMin_outliers'] = magnitudeMin_outliers
        _df.loc[i, 'PF_magnitudeMean_outliers'] = magnitudeMean_outliers
        _df.loc[i, 'PF_magnitudeStd_outliers'] = magnitudeStd_outliers

        try:
            arrival_diff_list = arrival_diff_list[
                           1:]  ## remove the first because it subtracts from the last element, we avoid if else for performance
            arrival_diff_list.sort()
            Max_idleTime = arrival_diff_list[-1]
            Min_idleTime = arrival_diff_list[1]
            Mean_idleTime = sum(arrival_diff_list) / len(arrival_diff_list)

            _df.loc[i, 'PF_Max_idleTime'] = Max_idleTime
            _df.loc[i, 'PF_Min_idleTime'] = Min_idleTime
            _df.loc[i, 'PF_Mean_idleTime'] = Mean_idleTime
        except:
            try:
                _df.loc[i, 'PF_Max_idleTime'] = arrival_diff_list[0]
                _df.loc[i, 'PF_Min_idleTime'] = arrival_diff_list[0]
                _df.loc[i, 'PF_Mean_idleTime'] = arrival_diff_list[0]
            except:
                #print("only one packet in this CF")
                _df.loc[i, 'PF_Max_idleTime'] = 0
                _df.loc[i, 'PF_Min_idleTime'] = 0
                _df.loc[i, 'PF_Mean_idleTime'] = 0
    _df = _df.fillna({'PF_magnitudeMax_outliers': _df.PF_No_outliers,
                    'PF_magnitudeMin_outliers': _df.PF_No_outliers,
                    'PF_magnitudeMean_outliers': _df.PF_No_outliers,
                    'PF_magnitudeStd_outliers': _df.PF_No_outliers,
                    })

    print('{} - Done'.format(PRINT_MESSAGE))


    return _df


