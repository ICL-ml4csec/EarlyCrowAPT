import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import re
import math
import EarlyCrow.preprocessing.flags as prep
def pf_generator(_df,GRANULARITY):
    MAXIMUM_CAPTURE = 900
    #df = df.fillna({'Info': ''})
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
    pat = re.compile(' A ([a-zA-Z0-9-.]+)')
    pat_ns = re.compile('NS ([a-zA-Z0-9-.]+)')

    pat_full = re.compile(' A ([0-9-.]+)')
    pat_ip = re.compile(' A ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)')
    for gr in range (math.ceil(sample_rate)):
        print("Sample # {} out of {} ".format(gr,sample_rate), end='\r')

        df = df_data[(df_data.Relative_Time >= gr * GRANULARITY) & (
                    df_data.Relative_Time < gr * GRANULARITY + GRANULARITY)]

        df_tcp_udp = df.loc[
            (df.EPFLAG_TCP == 1) | (df.EPFLAG_UDP == 1) | (
                        df.EPFLAG_HTTP == 1)]

        # this is to bring all packets that has extrenal connection, we add HTTP too
        # for external connection for those does not use raw tcp or udp at all
        # but we stick to df_tcp_udp as HTTP is built on the top of such protocols

        # for ICMP
        df_tcp_udp_icmp= df.loc[(df.EPFLAG_TCP==1) | (df.EPFLAG_UDP==1) | (df.EPFLAG_ICMP==1)]


        # here we can find all unique bidirectional flow to find sent and recieve packet length bytes
        conn_pairs_df = df_tcp_udp.groupby(
            by=['Source', 'Destination']).Length.sum()
        conn_pairs_df=conn_pairs_df.reset_index()
        if len(conn_pairs_df) ==0:
            print("No packets found in a given time interval ({},{})"
                  .format(gr * GRANULARITY, gr * GRANULARITY + GRANULARITY), end='\r')
            continue ## for those time interval the does not have any connection, break and
        conn_pairs_unique_df=pd.DataFrame( index=[0], columns=conn_pairs_df.columns)
        for i in range(len(conn_pairs_df)):
            if i==0:
                conn_pairs_unique_df.iloc[0] = conn_pairs_df.iloc[i]
            else:

                for j in range(len(conn_pairs_unique_df)):
                    if ((conn_pairs_df.loc[i, 'Source'] == conn_pairs_unique_df.loc[
                        j, 'Destination']
                         and conn_pairs_df.loc[i, 'Destination'] ==
                         conn_pairs_unique_df.loc[j, 'Source'])):
                        j = len(conn_pairs_unique_df) # for last flow if duplicate, so won't be bypass the next condition
                        break
                if j== len(conn_pairs_unique_df)-1:
                    conn_pairs_unique_df = conn_pairs_unique_df.append(conn_pairs_df.iloc[i])
                    conn_pairs_unique_df = conn_pairs_unique_df.reset_index(drop=True)
        ### source should be internal , swap destination
        # to source if destination is the internal this is important to collect DNS
        # relavent packets
        internalDst = conn_pairs_unique_df.Destination.str.startswith(
            '192.168')
        for d in range(len(internalDst)):
            if internalDst[d] == True:
                swapper = conn_pairs_unique_df.loc[d, 'Source']
                conn_pairs_unique_df.loc[d, 'Source'] = \
                    conn_pairs_unique_df.loc[d, 'Destination']
                conn_pairs_unique_df.loc[d, 'Destination'] = swapper

        internalDst = conn_pairs_unique_df.Destination.str.startswith(
            '10.')
        for d in range(len(internalDst)):
            if internalDst[d] == True:
                swapper = conn_pairs_unique_df.loc[d, 'Source']
                conn_pairs_unique_df.loc[d, 'Source'] = \
                    conn_pairs_unique_df.loc[d, 'Destination']
                conn_pairs_unique_df.loc[d, 'Destination'] = swapper

        internalDst = conn_pairs_unique_df.Destination.str.startswith(
            '147.32')
        for d in range(len(internalDst)):
            if internalDst[d] == True:
                swapper = conn_pairs_unique_df.loc[d, 'Source']
                conn_pairs_unique_df.loc[d, 'Source'] = \
                    conn_pairs_unique_df.loc[d, 'Destination']
                conn_pairs_unique_df.loc[d, 'Destination'] = swapper

        for i in range(len(conn_pairs_unique_df)):
            domain_list=[]
            ns_list = []
            ip_list=[]
            print("Flow # {} is producing and underprocessing.".format(i), end='\r')
            flow_biPkts=df[((df.Source==conn_pairs_unique_df.loc[i,'Source']) &
               (df.Destination==conn_pairs_unique_df.loc[i,'Destination']) )|
               ((df.Destination==conn_pairs_unique_df.loc[i,'Source']) &
               (df.Source==conn_pairs_unique_df.loc[i,'Destination']))]


            flow_biPkts=flow_biPkts.reset_index(drop=True)
            print("Flow Pairs: {} and {}".format(flow_biPkts.loc[0,'Source'],flow_biPkts.loc[0,'Destination']), end='\r') # static zero, we just want the connection pair


            ########################
            ## START: DNS PACKETS ##
            ########################
            # find the dns related response packets first by find any dns packets includes the destination
            dnsRes_packets = pd.DataFrame(columns=flow_biPkts.columns)
            # find the dns related response packets first by find any dns packets includes the destination
            if len(df[df.Info.str.contains(
                    flow_biPkts.loc[0, 'Destination'])]) > 0:
                dnsRes_packets = df[df.Info.str.contains(
                    flow_biPkts.loc[0, 'Destination'])]
            #else:  # if DNS query and response belong to previous sample interval, trace the packets
            #    prev_idx = 1
            #    while len(dnsRes_packets) == 0 and gr - prev_idx >= 0:
            #        print(
            #            "Tracing DNS request and response in previours interval")

            #        prev_df = df_data[(df_data.Relative_Time >= (
            #                gr - prev_idx) * GRANULARITY) & (
            #                                  df_data.Relative_Time < (
            #                                  gr - prev_idx) * GRANULARITY + GRANULARITY)]
            #        if len(prev_df[prev_df.Info.str.contains(
            #                flow_biPkts.loc[0, 'Destination'])]) > 0:
            #            dnsRes_packets = prev_df[
            #                prev_df.Info.str.contains(
            #                    flow_biPkts.loc[0, 'Destination'])]
            #        prev_idx += 1

            # dnsRes_packets=df[df.Info.str.contains(flow_biPkts.loc[0,'Destination'])]
            dnsRes_packets=dnsRes_packets.reset_index(drop=True)
            dnsRes_packets=dnsRes_packets[dnsRes_packets.EPFLAG_DNS == 1]
            dnsRes_packets_unique=dnsRes_packets.copy(deep=True)
            if len(dnsRes_packets_unique)>0:
                dnsRes_packets_unique[
                    'domains_response'] = dnsRes_packets_unique.Info.str.extract(
                    ' A ([a-zA-Z0-9-.]+)\s')

                dnsRes_packets_unique = dnsRes_packets_unique.drop_duplicates(
                    subset=['domains_response'])
                dnsRes_packets = dnsRes_packets.reset_index()
                dnsRes_packets_unique = dnsRes_packets_unique.reset_index()

            # find the dns related request packets
                for j in range(len(dnsRes_packets_unique)):
                    info_str = dnsRes_packets_unique.loc[j, 'Info']
                    a_rr = pat.findall(info_str)
                    a_rr_full = pat_full.findall(
                        info_str)  # we add this to be able to extrat full fqdn without the need of knowing how many subdomains
                    a_rr_ips = pat_ip.findall(info_str)
                    ns_rr = pat_ns.findall(info_str)

                    #ip_list=a_rr_ips
                    domain_res = list(
                        set(a_rr).symmetric_difference(set(a_rr_ips)))
                    try:
                        domain_list.append(domain_res[0])
                        ip_list.append(tuple(a_rr_ips))
                        ns_list.append(tuple(ns_rr))
                    except:
                        pass

                    #if len(flow_biPkts[flow_biPkts.EPFLAG_DNS==1]) !=0:
                    try:

                        if j==0:

                            dnsReq_packets=df[df.Info.str.contains(domain_res[0])] ## domain_res[0] is indexed with
                                                                                        # zero because a list with one element
                                                                                        # always
                        else:
                            dnsReq_packets_new=df[df.Info.str.contains(domain_res[0])]
                            dnsReq_packets=dnsReq_packets.append(dnsReq_packets_new)

                        dnsReq_packets=dnsReq_packets.drop_duplicates()
                        dnsReq_packets = dnsReq_packets[
                            dnsReq_packets.Relative_Time < gr * GRANULARITY + GRANULARITY] #filter out beoynd time window for now
                        dnsReq_packets=dnsReq_packets.reset_index(drop=True)
                        flow_biPkts=flow_biPkts.append(dnsReq_packets)
                        flow_biPkts=flow_biPkts.append(dnsRes_packets)
                    #else:
                    except:
                        #print("Flow Does not use DNS request and response")
                        pass
            else:
                #print("No DNS Packets")
                pass

            ######################
            ## END: DNS PACKETS ##
            ######################

            flow_biPkts = flow_biPkts.drop_duplicates(subset=['No'])
            flow_biPkts=flow_biPkts.sort_values('No')

            flow_biPkts=flow_biPkts.rename(columns={"No": "oIndex"})
            flow_biPkts=flow_biPkts.reset_index(drop=True)

            flow_biPkts.index = flow_biPkts.index.set_names(['Packet_No'])

            flow_biPkts=flow_biPkts.reset_index().rename(columns={flow_biPkts.index.name:'Packet_No'})

            flow_biPkts.insert(0, 'FlowID', i) # zero refer to the column position

            print("Adding New PairFlow for flow {}".format(i), end='\r')

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

            #PairFlow['oIndex'] = PairFlow['oIndex'].astype('object')
            #PairFlow.at[currCF_idx, 'oIndex'] = flow_biPkts.oIndex.to_list()
            ## Seperating Data and Control Planes
            ##
            # TCP flags:
            # URG | ACK | PSH | RST | SYN | FIN
            # Examples:
            #	SYN/ACK = 01 0010 =  0x012
            #	SYN 	= 00 0010 =  0x002
            #	ACK 	= 01 0000 =  0x010
            #	RST	= 00 0100 =  0x004
            #	FIN/ACK = 01 0001 =  0x011
            #	PSH/ACK	= 01 1000 =  0x018 ( HTTP GET, HTTP POST, HTTP Continuation, HTTP/1.1 200 ok, HTTP/1.1 304 Not Modified,
            #				     TLS Client Hello, TLS Continuation Data, TLS Application Data,
            #					TLS Change Cipher Spec, TCP Client Key Exchange, OCSP response)
            #	FIN/PSH/ACK	= 01 1001 = 0x019 ( HTTP/1.0 408 Request Time-out (text/html)

            control_plane = flow_biPkts[flow_biPkts.tcp_flag != '0x018']
            control_plane = control_plane.dropna(subset=['tcp_flag'])
            control_plane = control_plane.reset_index(drop=True)
            data_plane = flow_biPkts[flow_biPkts.tcp_flag == '0x018']

            Cpacket_list = []
            CoIndex_No = control_plane.oIndex.to_list()
            CoIndex_flag = control_plane.tcp_flag.to_list()
            # CoIndex_prot = control_plane.Protocol.to_list()
            CoIndex_timestamp = control_plane.Relative_Time.to_list()
            CoIndex_len = control_plane.Length.to_list()

            for k in range(len(CoIndex_No)):
                # print(i)
                single_tuple = []
                single_tuple.append(CoIndex_No[k])
                single_tuple.append(CoIndex_flag[k])
                # single_tuple.append(CoIndex_prot[k])
                single_tuple.append(CoIndex_timestamp[k])
                single_tuple.append(CoIndex_len[k])
                Cpacket_list.append(tuple(single_tuple))

            PairFlow.at[
                currCF_idx, 'control_plane'] = Cpacket_list

            ## same process for data plane with protocol name and only with flag 0x018

            data_plane['req_resp'] = np.nan
            data_plane['req_resp_type'] = np.nan
            data_plane['resp_content_type'] = np.nan

            dic_req_resp = {'GET': "Request", 'POST': "Request"}
            dic_req_resp_encryption = {'Client Hello': "Request",
                                       'Server Hello': "Response"}

            data_plane['req_resp'] = data_plane['Request_Method'].map(
                dic_req_resp)
            data_plane['req_resp'] = data_plane['req_resp'].fillna(
                data_plane['Info'].map(dic_req_resp_encryption))

            data_plane['req_resp'] = data_plane.req_resp.fillna(
                "Response")

            data_plane['req_resp_type'] = data_plane.Status_Code.fillna(
                data_plane.Request_Method)
            data_plane[
                'req_resp_type'] = data_plane.req_resp_type.fillna(
                data_plane.Info)

            data_plane['resp_content_type'] = data_plane.Content_Type
            data_plane['resp_content_type'] = data_plane[
                'resp_content_type'].fillna("Empty Content")

            Dpacket_list = []
            DoIndex_No = data_plane.oIndex.to_list()
            DoIndex_prot = data_plane.Protocol.to_list()
            DoIndex_req_resp = data_plane.req_resp.to_list()
            DoIndex_req_resp_type = data_plane.req_resp_type.to_list()
            DoIndex_resp_content_type = data_plane.resp_content_type.to_list()
            DoIndex_timestamp = data_plane.Relative_Time.to_list()
            DoIndex_len = data_plane.Length.to_list()

            for k in range(len(DoIndex_No)):
                # print(i)
                single_tuple = []
                single_tuple.append(DoIndex_No[k])
                single_tuple.append(DoIndex_prot[k])
                single_tuple.append(DoIndex_req_resp[k])
                single_tuple.append(DoIndex_req_resp_type[k])
                single_tuple.append(DoIndex_resp_content_type[k])
                single_tuple.append(DoIndex_timestamp[k])
                single_tuple.append(DoIndex_len[k])
                Dpacket_list.append(tuple(single_tuple))

            PairFlow.at[currCF_idx, 'data_plane'] = Dpacket_list

            ## now we seperate non-TCP planes which includes UDP and ICMP planes
            nonTCP_plane = flow_biPkts[flow_biPkts.tcp_flag.isna()]

            ## icmp plane
            icmp_plane = nonTCP_plane[nonTCP_plane.EPFLAG_ICMP == 1]

            ## udp Plane
            udp_plane = nonTCP_plane[nonTCP_plane.EPFLAG_ICMP == 0]

            #### label DNS request and response
            # udp_plane['temp_type1'] = udp_plane.Info.str.contains(
            #    'Standard query')
            # udp_plane['temp_type2'] = udp_plane.Info.str.contains(
            #    'response')
            # udp_plane['temp_type'] = udp_plane['temp_type1'] * udp_plane[
            #    'temp_type2']

            udp_plane['dns_temp_type'] = udp_plane.Info.str.contains(
                'response')
            try:
                udp_plane.loc[
                    udp_plane.dns_temp_type == True, 'udp_type'] = 'DNS_Response'

                udp_plane.loc[(udp_plane.dns_temp_type == False) & (
                        udp_plane.EPFLAG_DNS == 1), 'udp_type'] = 'DNS_Request'
            except:
                print("UDP plane does not have DNS", end='\r')
                udp_plane['udp_type'] = np.nan
            udp_plane['udp_type'] = udp_plane.udp_type.fillna(
                'Raw_UDP')  ## add more exceptions here for udp_type for those non-dns using udp

            UDPpacket_list = []
            UDPoIndex_No = udp_plane.oIndex.to_list()
            UDPoIndex_prot = udp_plane.Protocol.to_list()
            UDPoIndex_type = udp_plane.udp_type.to_list()
            UDPoIndex_timestamp = udp_plane.Relative_Time.to_list()
            UDPoIndex_len = udp_plane.Length.to_list()

            for k in range(len(UDPoIndex_No)):
                # print(i)
                single_tuple = []
                single_tuple.append(UDPoIndex_No[k])
                single_tuple.append(UDPoIndex_prot[k])
                single_tuple.append(UDPoIndex_type[k])
                single_tuple.append(UDPoIndex_timestamp[k])
                single_tuple.append(UDPoIndex_len[k])
                UDPpacket_list.append(tuple(single_tuple))

            PairFlow.at[currCF_idx, 'udp_plane'] = UDPpacket_list

            # now icmp plane
            # icmp_plane

            ICMPpacket_list = []
            ICMPoIndex_No = icmp_plane.oIndex.to_list()
            ICMPoIndex_type = icmp_plane.ICMP_Type.to_list()
            ICMPoIndex_code = icmp_plane.ICMP_Code.to_list()
            ICMPoIndex_timestamp = icmp_plane.Relative_Time.to_list()
            ICMPoIndex_len = icmp_plane.Length.to_list()

            for k in range(len(ICMPoIndex_No)):
                # print(i)
                single_tuple = []
                single_tuple.append(ICMPoIndex_No[k])
                single_tuple.append(ICMPoIndex_type[k])
                single_tuple.append(ICMPoIndex_code[k])
                single_tuple.append(ICMPoIndex_timestamp[k])
                single_tuple.append(ICMPoIndex_len[k])
                ICMPpacket_list.append(tuple(single_tuple))

            PairFlow.at[
                currCF_idx, 'icmp_plane'] = ICMPpacket_list

            ## old packet data point regardless of planes

            packet_list = []
            oIndex_No = flow_biPkts.oIndex.to_list()
            oIndex_prot = flow_biPkts.Protocol.to_list()
            oIndex_timestamp = flow_biPkts.Relative_Time.to_list()
            oIndex_len = flow_biPkts.Length.to_list()

            for k in range(len(oIndex_No)):
                # print(i)
                single_tuple = []
                single_tuple.append(oIndex_No[k])
                single_tuple.append(oIndex_prot[k])
                single_tuple.append(oIndex_timestamp[k])
                single_tuple.append(oIndex_len[k])
                packet_list.append(tuple(single_tuple))

            PairFlow.at[
                currCF_idx, 'packet_datapoint'] = packet_list

            #lastCF_idx=len(PairFlow) ## temp, should be deleted immmediatly

            PairFlow.at[currCF_idx, 'EPFLAG_ICMP'] = flow_biPkts['EPFLAG_ICMP'].max()
            PairFlow.at[currCF_idx, 'EPFLAG_UDP'] = flow_biPkts['EPFLAG_UDP'].max()
            PairFlow.at[currCF_idx, 'EPFLAG_TCP'] = flow_biPkts['EPFLAG_TCP'].max()
            PairFlow.at[currCF_idx, 'EPFLAG_DNS'] = flow_biPkts['EPFLAG_DNS'].max()
            PairFlow.at[currCF_idx, 'EPFLAG_HTTP'] = flow_biPkts['EPFLAG_HTTP'].max()
            PairFlow.at[currCF_idx, 'EPFLAG_HTTP_XML'] = flow_biPkts['EPFLAG_HTTP_XML'].max()
            PairFlow.at[currCF_idx, 'EPFLAG_TLS'] = flow_biPkts['EPFLAG_TLS'].max()
            PairFlow.at[currCF_idx, 'EPFLAG_SSL'] = flow_biPkts['EPFLAG_SSL'].max()





        ## general statistics

            PairFlow.loc[currCF_idx,'tcp_packets']=len(flow_biPkts[flow_biPkts['EPFLAG_TCP']==1]) + len(flow_biPkts[flow_biPkts['EPFLAG_HTTP']==1]) + len(flow_biPkts[flow_biPkts['EPFLAG_TLS']==1]) + len(flow_biPkts[flow_biPkts['EPFLAG_SSL']==1])
            PairFlow.loc[currCF_idx,'udp_packets']=len(flow_biPkts[flow_biPkts['EPFLAG_UDP']==1]) + len(flow_biPkts[flow_biPkts['EPFLAG_DNS'] == 1])
            PairFlow.loc[currCF_idx,'icmp_packets']=len(flow_biPkts[flow_biPkts['EPFLAG_ICMP']==1])
            PairFlow.loc[currCF_idx,'http_packets']=len(flow_biPkts[flow_biPkts['EPFLAG_HTTP']==1])
            PairFlow.loc[currCF_idx,'http_xml_packets']=len(flow_biPkts[flow_biPkts['EPFLAG_HTTP_XML']==1])
            PairFlow.loc[currCF_idx,'tls_packets']=len(flow_biPkts[flow_biPkts['EPFLAG_TLS']==1])
            PairFlow.loc[currCF_idx,'ssl_packets']=len(flow_biPkts[flow_biPkts['EPFLAG_SSL']==1])
            PairFlow.loc[currCF_idx, 'dns_packets'] = len(flow_biPkts[flow_biPkts['EPFLAG_DNS'] == 1])

            ##Todo: extract domain name
            #


            PairFlow.at[currCF_idx, 'fqdn_lists'] = domain_list
            #

            PairFlow.at[currCF_idx, 'fqdn_ns_lists'] = ns_list
            #

            PairFlow.at[currCF_idx, 'fqdn_ip_lists'] = ip_list
            #



            ##Todo: extract HTTP request headers


            if (len(flow_biPkts.User_Agent.dropna()) == 0):
                flow_biPkts[
                    'User_Agent'] = flow_biPkts.User_Agent.fillna(
                    "Empty User Agent")
            User_Agent = list(flow_biPkts.User_Agent.unique())
            User_Agent = [x for x in User_Agent if str(x) != 'nan']
            try:
                User_Agent.remove("")
            except:
                pass

            Content_Type = list(flow_biPkts.Content_Type.unique())
            try:
                Content_Type.remove("")
            except:
                pass

            Status_Code_Description = list(
                flow_biPkts.Status_Code_Description.unique())
            try:
                Status_Code_Description.remove("")
            except:
                pass

            Status_Code = list(flow_biPkts.Status_Code.unique())
            try:
                Status_Code.remove("")
            except:
                pass

            http_server = list(flow_biPkts.http_server.unique())
            try:
                http_server.remove("")
            except:
                pass

            http_request_uri_query = list(
                flow_biPkts.http_request_uri_query.unique())
            try:
                http_request_uri_query.remove("")
            except:
                pass

            http_request_uri_query_parameter = list(
                flow_biPkts.http_request_uri_query_parameter.unique())
            try:
                http_request_uri_query_parameter.remove("")
            except:
                pass

            ## assign these values to PairFlow i^th

            PairFlow.at[currCF_idx,'User_Agent']= User_Agent

            PairFlow.at[currCF_idx,'Content_Type']= Content_Type

            PairFlow.at[currCF_idx,'Status_Code_Description']= Status_Code_Description

            PairFlow.at[currCF_idx,'Status_Code']= Status_Code

            PairFlow.at[currCF_idx,'http_server']= http_server

            #PairFlow.at[currCF_idx,'http_request_uri_query']= http_request_uri_query

            #PairFlow.at[currCF_idx,'http_request_uri_query_parameter']= http_request_uri_query_parameter


        ## now statistical behaviour

            try:
                PairFlow.loc[currCF_idx,'TTL_max']= \
                    flow_biPkts.TTL.dropna().astype(int).max()
            except: # for ICMP case, because it has to TTL, we picked the higher one
                flow_biPkts['TTL']=flow_biPkts.TTL.str.replace("([0-9]+,)", "")
                PairFlow.loc[currCF_idx,'TTL_max']= \
                    flow_biPkts.TTL.dropna().astype(int).max()


            PairFlow.loc[currCF_idx, 'TTL_min'] = \
                flow_biPkts.TTL.dropna().astype(int).min()

            PairFlow.loc[currCF_idx, 'TTL_mean'] = \
                flow_biPkts.TTL.dropna().astype(int).mean()

            PairFlow.loc[currCF_idx, 'TTL_std'] = \
                flow_biPkts.TTL.dropna().astype(int).std()

            PairFlow.loc[currCF_idx, 'TTL_median'] = \
                flow_biPkts.TTL.dropna().astype(int).median()

            PairFlow.loc[currCF_idx, 'TTL_median'] = \
                flow_biPkts.TTL.dropna().astype(int).median()

            PairFlow.loc[currCF_idx, 'Delta_Time_max'] =\
                flow_biPkts.Delta_Time.max()

            PairFlow.loc[currCF_idx, 'Delta_Time_max'] = \
                flow_biPkts.Delta_Time.max()

            PairFlow.loc[currCF_idx, 'Delta_Time_min'] = \
                flow_biPkts.Delta_Time.min()

            PairFlow.loc[currCF_idx, 'Delta_Time_mean'] = \
                flow_biPkts.Delta_Time.mean()

            PairFlow.loc[currCF_idx, 'Delta_Time_std'] = \
                flow_biPkts.Delta_Time.std()

            PairFlow.loc[currCF_idx, 'Delta_Time_median'] = \
                flow_biPkts.Delta_Time.median()

            PairFlow.loc[currCF_idx, 'Duration'] = \
            flow_biPkts.loc[len(flow_biPkts)-1,'Relative_Time']- flow_biPkts.loc[0,'Relative_Time']


            ## HTTP Response Stat.
            try:
                PairFlow.loc[
                    currCF_idx, 'Content_Length_Total'] = flow_biPkts.Content_Length.dropna().astype(
                    int).sum()

            except:  # for ICMP case, because it has to TTL, we picked the higher one
                flow_biPkts[
                    'Content_Length'] = flow_biPkts.Content_Length.str.replace(
                    "([0-9]+,)", "")
                PairFlow.loc[
                    currCF_idx, 'Content_Length_Total'] = flow_biPkts.Content_Length.dropna().astype(
                    int).sum()

            PairFlow.loc[
                currCF_idx, 'Content_Length_min'] = flow_biPkts.Content_Length.dropna().astype(
                int).min()
            PairFlow.loc[
                currCF_idx, 'Content_Length_max'] = flow_biPkts.Content_Length.dropna().astype(
                int).max()
            PairFlow.loc[
                currCF_idx, 'Content_Length_median'] = flow_biPkts.Content_Length.dropna().astype(
                int).median()
            scalar_col = ['Content_Length_min', 'Content_Length_max',
                          'Content_Length_median']
            for col in scalar_col:  ## for those zero content length, max/min/median function will false return nan but it is zero
                PairFlow.loc[currCF_idx, {'{}'.format(col)}] = \
                PairFlow.loc[
                    currCF_idx, {'{}'.format(col)}].fillna(0)


        ## Total Sent and Received bytes
            try:
                ip_source = flow_biPkts[
                    (flow_biPkts.EPFLAG_TCP == 1) | (
                                flow_biPkts.EPFLAG_HTTP == 1)].reset_index().loc[
                    0, 'Source']
                ip_dest = flow_biPkts[(flow_biPkts.EPFLAG_TCP == 1) | (
                            flow_biPkts.EPFLAG_HTTP == 1)].reset_index().loc[
                    0, 'Destination']
            except:
                ip_source = \
                flow_biPkts[flow_biPkts.EPFLAG_UDP == 1].reset_index().loc[
                    0, 'Source']
                ip_dest = flow_biPkts[flow_biPkts.EPFLAG_UDP == 1].reset_index().loc[
                0, 'Destination']

            PairFlow.at[
                currCF_idx, 'total_bytes'] = flow_biPkts.Length.sum()


            PairFlow.loc[currCF_idx, 'total_sent_bytes'] =\
                flow_biPkts[(flow_biPkts.Source==ip_source) &
                            (flow_biPkts.Destination==ip_dest)].Length.sum()

            PairFlow.loc[currCF_idx, 'total_recv_bytes'] = \
                flow_biPkts[(flow_biPkts.Source == ip_dest) &
                            (flow_biPkts.Destination == ip_source)].Length.sum()
            PairFlow.loc[currCF_idx, 'sample_interval'] = \
                "({},{})".format(gr*GRANULARITY ,gr*GRANULARITY + GRANULARITY)

            PairFlow.loc[currCF_idx, 'multiple_label'] = \
                flow_biPkts.loc[0,'multiple_label']

            ######
            ######
            ## Certificate and HTTP Enryption
            flow_biPkts_tls_server_hello = flow_biPkts[
                flow_biPkts.Info.str.contains("Server Hello")]
            flow_biPkts_tls_client_hello = flow_biPkts[
                flow_biPkts.Info.str.contains("Client Hello")]
            flow_biPkts_tls_encrypted_packets = flow_biPkts[
                flow_biPkts.Info.str.contains("Application Data")]

            Server_Cipher_Suite = list(
                flow_biPkts_tls_server_hello.Cipher_Suite.unique())
            # Server_Cipher_Suite.remove("")
            PairFlow.at[
                currCF_idx, 'Server_Cipher_Suite'] = Server_Cipher_Suite

            Client_Cipher_Suite = list(
                flow_biPkts_tls_client_hello.Cipher_Suite.unique())
            PairFlow.at[
                currCF_idx, 'Client_Cipher_Suite'] = Client_Cipher_Suite

            Client_Cipher_Suites_Length_min = flow_biPkts_tls_client_hello.Cipher_Suites_Length.min()
            Client_Cipher_Suites_Length_max = flow_biPkts_tls_client_hello.Cipher_Suites_Length.max()
            Client_Cipher_Suites_Length_median = flow_biPkts_tls_client_hello.Cipher_Suites_Length.median()
            PairFlow.at[
                currCF_idx, 'Client_Cipher_Suites_Length_min'] = Client_Cipher_Suites_Length_min
            PairFlow.at[
                currCF_idx, 'Client_Cipher_Suites_Length_max'] = Client_Cipher_Suites_Length_max
            PairFlow.at[
                currCF_idx, 'Client_Cipher_Suites_Length_median'] = Client_Cipher_Suites_Length_median

            Server_Cipher_Suites_Length_min = flow_biPkts_tls_server_hello.Cipher_Suites_Length.min()
            Server_Cipher_Suites_Length_max = flow_biPkts_tls_server_hello.Cipher_Suites_Length.max()
            Server_Cipher_Suites_Length_median = flow_biPkts_tls_server_hello.Cipher_Suites_Length.median()
            PairFlow.at[
                currCF_idx, 'Server_Cipher_Suites_Length_min'] = Server_Cipher_Suites_Length_min
            PairFlow.at[
                currCF_idx, 'Server_Cipher_Suites_Length_max'] = Server_Cipher_Suites_Length_max
            PairFlow.at[
                currCF_idx, 'Server_Cipher_Suites_Length_median'] = Server_Cipher_Suites_Length_median

            PairFlow.at[
                currCF_idx, 'Total_Encrypted_Bytes'] = flow_biPkts_tls_encrypted_packets.Length.sum()

            PairFlow.loc[
                currCF_idx, 'Total_Encrypted_Sent_Bytes'] = \
                flow_biPkts_tls_encrypted_packets[(
                                                              flow_biPkts_tls_encrypted_packets.Source == ip_source) &
                                                  (
                                                              flow_biPkts_tls_encrypted_packets.Destination == ip_dest)].Length.sum()

            PairFlow.loc[
                currCF_idx, 'Total_Encrypted_Recv_Bytes'] = \
                flow_biPkts_tls_encrypted_packets[(
                                                              flow_biPkts_tls_encrypted_packets.Source == ip_dest) &
                                                  (
                                                              flow_biPkts_tls_encrypted_packets.Destination == ip_source)].Length.sum()

            Client_Extension_Type = list(
                flow_biPkts_tls_client_hello.Extension_Type.unique())
            PairFlow.at[
                currCF_idx, 'Client_Extension_Type'] = Client_Extension_Type
            Server_Extension_Type = list(
                flow_biPkts_tls_server_hello.Extension_Type.unique())
            PairFlow.at[
                currCF_idx, 'Server_Extension_Type'] = Server_Extension_Type

            Client_Extensions_Length_min = flow_biPkts_tls_client_hello.Extensions_Length.min()
            Client_Extensions_Length_max = flow_biPkts_tls_client_hello.Extensions_Length.max()
            Client_Extensions_Length_median = flow_biPkts_tls_client_hello.Extensions_Length.median()
            PairFlow.at[
                currCF_idx, 'Client_Extensions_Length_min'] = Client_Extensions_Length_min
            PairFlow.at[
                currCF_idx, 'Client_Extensions_Length_max'] = Client_Extensions_Length_max
            PairFlow.at[
                currCF_idx, 'Client_Extensions_Length_median'] = Client_Extensions_Length_median

            Server_Extensions_Length_min = flow_biPkts_tls_server_hello.Extensions_Length.min()
            Server_Extensions_Length_max = flow_biPkts_tls_server_hello.Extensions_Length.max()
            Server_Extensions_Length_median = flow_biPkts_tls_server_hello.Extensions_Length.median()
            PairFlow.at[
                currCF_idx, 'Server_Extensions_Length_min'] = Server_Extensions_Length_min
            PairFlow.at[
                currCF_idx, 'Server_Extensions_Length_max'] = Server_Extensions_Length_max
            PairFlow.at[
                currCF_idx, 'Server_Extensions_Length_median'] = Server_Extensions_Length_median

            Client_Signature_Algorithm_Hash = list(
                flow_biPkts_tls_client_hello.Signature_Hash_Algorithm_Hash.unique())
            PairFlow.at[
                currCF_idx, 'Client_Signature_Algorithm_Hash'] = Client_Signature_Algorithm_Hash
            Server_Signature_Algorithm_Hash = list(
                flow_biPkts_tls_server_hello.Extension_Type.unique())
            PairFlow.at[
                currCF_idx, 'Server_Signature_Algorithm_Hash'] = Server_Signature_Algorithm_Hash

            Client_Supported_Group = list(
                flow_biPkts_tls_client_hello.Supported_Group.unique())
            PairFlow.at[
                currCF_idx, 'Client_Supported_Group'] = Client_Supported_Group
            Server_Supported_Group = list(
                flow_biPkts_tls_server_hello.Supported_Group.unique())
            PairFlow.at[
                currCF_idx, 'Server_Supported_Group'] = Server_Supported_Group

            Client_ALPN_Next_Protocol = list(
                flow_biPkts_tls_client_hello.ALPN_Next_Protocol.unique())
            PairFlow.at[
                currCF_idx, 'Client_ALPN_Next_Protocol'] = Client_ALPN_Next_Protocol
            Server_ALPN_Next_Protocol = list(
                flow_biPkts_tls_server_hello.ALPN_Next_Protocol.unique())
            PairFlow.at[
                currCF_idx, 'Server_ALPN_Next_Protocol'] = Server_ALPN_Next_Protocol

            Client_EC_point_format = list(
                flow_biPkts_tls_client_hello.EC_point_format.unique())
            PairFlow.at[
                currCF_idx, 'Client_EC_point_format'] = Client_EC_point_format
            Server_EC_point_format = list(
                flow_biPkts_tls_server_hello.EC_point_format.unique())
            PairFlow.at[
                currCF_idx, 'Server_EC_point_format'] = Server_EC_point_format

            Client_Compression_Method = list(
                flow_biPkts_tls_client_hello.Compression_Method.unique())
            PairFlow.at[
                currCF_idx, 'Client_Compression_Method'] = Client_Compression_Method
            Server_Compression_Method = list(
                flow_biPkts_tls_server_hello.Compression_Method.unique())
            PairFlow.at[
                currCF_idx, 'Server_Compression_Method'] = Server_Compression_Method

            producedAt = list(
                flow_biPkts.producedAt.unique())
            PairFlow.at[
                currCF_idx, 'producedAt'] = producedAt

            thisUpdate = list(
                flow_biPkts.thisUpdate.unique())
            PairFlow.at[
                currCF_idx, 'thisUpdate'] = thisUpdate

            nextUpdate = list(
                flow_biPkts.nextUpdate.unique())
            PairFlow.at[
                currCF_idx, 'nextUpdate'] = nextUpdate
            ##################### URL ####################
            url_df = flow_biPkts.dropna(
                subset=['http_request_full_uri'])
            url_df = url_df.drop_duplicates(
                subset=['http_request_full_uri'], keep='first')

            url_df = url_df.reset_index(drop=True)
            url_cf_list = []

            try:
                url_df[
                    'url_FQDN'] = url_df.http_request_full_uri.str.replace(
                    'http://', "")
                url_df['url_FQDN'] = url_df.url_FQDN.str.replace('/.*',
                                                                 "")
                url_df[
                    'url_Filename'] = url_df.http_request_full_uri.str.findall(
                    "[a-zA-Z0-9._]+(?:.exe|.zip|.css|.js|.woff2|.jpg|.gif|.png|.html|.php|.ashx|.config|.asmx|.ico|.woff)")
                url_df['url_Filename_str'] = url_df[
                    'url_Filename'].astype(
                    str)
                url_df['Referer'] = url_df.Referer.fillna('No Referer')
                url_df['Cookie'] = url_df.Cookie.fillna('No Cookie')
                # url_df.http_request_uri_query_parameter.str.findall("=")
                url_df[
                    'url_parameters'] = url_df.http_request_full_uri.str.findall(
                    "[a-zA-Z0-9_]+=")
                url_df['no_para'] = np.nan
                for upara in range(len(url_df)):
                    para_list = url_df.loc[upara, 'url_parameters']
                    para_list = list(dict.fromkeys(para_list))
                    url_df.loc[upara, 'no_para'] = len(para_list)

                url_df[
                    'No_values'] = url_df.http_request_full_uri.str.findall(
                    "=").apply(len)
                url_df[
                    'url_depth'] = url_df.http_request_full_uri.str.findall(
                    "[a-zA-Z0-9]+/").apply(
                    len) - 1  ## minus 1 to exclude the domain suffix from RegEx results
                url_df[
                    'No_frag'] = url_df.http_request_full_uri.str.findall(
                    "#").apply(len)
                url_df[
                    'Has_query_string'] = url_df.http_request_full_uri.str.contains(
                    "=[a-zA-Z]+\%+")
                url_list = []
                url_FQDN_list = url_df.url_FQDN.to_list()
                url_fullURI_list = url_df.http_request_full_uri.to_list()
                url_Referer_list = url_df.Referer.to_list()
                url_Cookie_list = url_df.Cookie.to_list()
                url_No_para_list = url_df.no_para.to_list()
                url_No_values_list = url_df.No_values.to_list()
                url_url_depth_list = url_df.url_depth.to_list()
                url_No_frag_list = url_df.No_frag.to_list()
                url_Has_query_string_list = url_df.Has_query_string.to_list()

                temp = url_df.url_Filename.dropna().to_list()
                url_filename_list = []
                for z in range(len(temp)):
                    try:
                        url_filename_list.append(
                            temp[z][len(temp[0]) - 1])
                    except:
                        url_filename_list.append("No Filename")
                for z in range(len(url_fullURI_list)):
                    # print(i)
                    single_tuple = []
                    single_tuple.append(url_FQDN_list[z])
                    single_tuple.append(url_fullURI_list[z])
                    try:
                        single_tuple.append(url_filename_list[z])
                    except:
                        single_tuple.append("No Filename")

                    single_tuple.append(
                        "Depth {}".format(url_url_depth_list[z]))
                    single_tuple.append(
                        "No_Para {}".format(url_No_para_list[z]))
                    single_tuple.append(
                        "No_Values {}".format(url_No_values_list[z]))
                    single_tuple.append(
                        "No_Frag {}".format(url_No_frag_list[z]))
                    single_tuple.append("Has_query_string {}".format(
                        url_Has_query_string_list[z]))
                    single_tuple.append(
                        "Referer {}".format(url_Referer_list[z]))
                    single_tuple.append(
                        "Cookie {}".format(url_Cookie_list[z]))
                    url_cf_list.append(tuple(single_tuple))
            except:
                pass

            PairFlow.at[currCF_idx, 'url_cf_list'] = url_cf_list

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