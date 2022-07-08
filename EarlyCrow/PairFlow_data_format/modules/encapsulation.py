import numpy as np
def encapsulation(PairFlow,flow_biPkts,currCF_idx,domain_list,ns_list,ip_list):
    ##Todo: extract domain name
    #

    ##Encapsulation
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

    PairFlow.at[currCF_idx, 'User_Agent'] = User_Agent

    PairFlow.at[currCF_idx, 'Content_Type'] = Content_Type

    PairFlow.at[
        currCF_idx, 'Status_Code_Description'] = Status_Code_Description

    PairFlow.at[currCF_idx, 'Status_Code'] = Status_Code

    PairFlow.at[currCF_idx, 'http_server'] = http_server

    ######
    ######
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

    ### Encapsulation
    Client_Extension_Type = list(
        flow_biPkts_tls_client_hello.Extension_Type.unique())
    PairFlow.at[
        currCF_idx, 'Client_Extension_Type'] = Client_Extension_Type
    Server_Extension_Type = list(
        flow_biPkts_tls_server_hello.Extension_Type.unique())
    PairFlow.at[
        currCF_idx, 'Server_Extension_Type'] = Server_Extension_Type

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

