import numpy as np
def aggregation(flow_biPkts,PairFlow,currCF_idx,gr, GRANULARITY):
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

    PairFlow.at[currCF_idx, 'EPFLAG_ICMP'] = flow_biPkts[
        'EPFLAG_ICMP'].max()
    PairFlow.at[currCF_idx, 'EPFLAG_UDP'] = flow_biPkts[
        'EPFLAG_UDP'].max()
    PairFlow.at[currCF_idx, 'EPFLAG_TCP'] = flow_biPkts[
        'EPFLAG_TCP'].max()
    PairFlow.at[currCF_idx, 'EPFLAG_DNS'] = flow_biPkts[
        'EPFLAG_DNS'].max()
    PairFlow.at[currCF_idx, 'EPFLAG_HTTP'] = flow_biPkts[
        'EPFLAG_HTTP'].max()
    PairFlow.at[currCF_idx, 'EPFLAG_HTTP_XML'] = flow_biPkts[
        'EPFLAG_HTTP_XML'].max()
    PairFlow.at[currCF_idx, 'EPFLAG_TLS'] = flow_biPkts[
        'EPFLAG_TLS'].max()
    PairFlow.at[currCF_idx, 'EPFLAG_SSL'] = flow_biPkts[
        'EPFLAG_SSL'].max()

    ## general statistics

    PairFlow.loc[currCF_idx, 'tcp_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_TCP'] == 1]) + len(
        flow_biPkts[flow_biPkts['EPFLAG_HTTP'] == 1]) + len(
        flow_biPkts[flow_biPkts['EPFLAG_TLS'] == 1]) + len(
        flow_biPkts[flow_biPkts['EPFLAG_SSL'] == 1])
    PairFlow.loc[currCF_idx, 'udp_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_UDP'] == 1]) + len(
        flow_biPkts[flow_biPkts['EPFLAG_DNS'] == 1])
    PairFlow.loc[currCF_idx, 'icmp_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_ICMP'] == 1])
    PairFlow.loc[currCF_idx, 'http_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_HTTP'] == 1])
    PairFlow.loc[currCF_idx, 'http_xml_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_HTTP_XML'] == 1])
    PairFlow.loc[currCF_idx, 'tls_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_TLS'] == 1])
    PairFlow.loc[currCF_idx, 'ssl_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_SSL'] == 1])
    PairFlow.loc[currCF_idx, 'dns_packets'] = len(
        flow_biPkts[flow_biPkts['EPFLAG_DNS'] == 1])

    ## now statistical behaviour

    try:
        PairFlow.loc[currCF_idx, 'TTL_max'] = \
            flow_biPkts.TTL.dropna().astype(int).max()
    except:  # for ICMP case, because it has to TTL, we picked the higher one
        flow_biPkts['TTL'] = flow_biPkts.TTL.str.replace(
            "([0-9]+,)", "")
        PairFlow.loc[currCF_idx, 'TTL_max'] = \
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

    PairFlow.loc[currCF_idx, 'Delta_Time_max'] = \
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
        flow_biPkts.loc[len(flow_biPkts) - 1, 'Relative_Time'] - \
        flow_biPkts.loc[0, 'Relative_Time']

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
            flow_biPkts[
                flow_biPkts.EPFLAG_UDP == 1].reset_index().loc[
                0, 'Source']
        ip_dest = flow_biPkts[
            flow_biPkts.EPFLAG_UDP == 1].reset_index().loc[
            0, 'Destination']

    PairFlow.at[
        currCF_idx, 'total_bytes'] = flow_biPkts.Length.sum()

    PairFlow.loc[currCF_idx, 'total_sent_bytes'] = \
        flow_biPkts[(flow_biPkts.Source == ip_source) &
                    (
                            flow_biPkts.Destination == ip_dest)].Length.sum()

    PairFlow.loc[currCF_idx, 'total_recv_bytes'] = \
        flow_biPkts[(flow_biPkts.Source == ip_dest) &
                    (
                            flow_biPkts.Destination == ip_source)].Length.sum()
    PairFlow.loc[currCF_idx, 'sample_interval'] = \
        "({},{})".format(gr * GRANULARITY,
                         gr * GRANULARITY + GRANULARITY)

    PairFlow.loc[currCF_idx, 'multiple_label'] = \
        flow_biPkts.loc[0, 'multiple_label']

    ## Certificate and HTTP Enryption
    flow_biPkts_tls_server_hello = flow_biPkts[
        flow_biPkts.Info.str.contains("Server Hello")]
    flow_biPkts_tls_client_hello = flow_biPkts[
        flow_biPkts.Info.str.contains("Client Hello")]
    flow_biPkts_tls_encrypted_packets = flow_biPkts[
        flow_biPkts.Info.str.contains("Application Data")]

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

