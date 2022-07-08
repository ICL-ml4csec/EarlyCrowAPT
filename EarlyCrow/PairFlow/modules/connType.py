def variants_extraction(df):

    httpBased = df.copy(deep=True)
    httpsBased = df.copy(deep=True)
    tcpudpBased = df.copy(deep=True)

    http_col = ['FlowID', 'Source', 'Destination', 'packet_datapoint',  'control_plane' ,
          'data_plane' ,'udp_plane', 'icmp_plane',
                'User_Agent', 'Status_Code', 'Status_Code_Description',
                'Content_Type',
                'http_server', 'EPFLAG_ICMP', 'EPFLAG_UDP', 'EPFLAG_TCP',
                'EPFLAG_DNS',
                'EPFLAG_HTTP', 'EPFLAG_TLS', 'EPFLAG_SSL', 'EPFLAG',
                'fqdn_lists', 'fqdn_ns_lists', 'fqdn_ip_lists',
                'url_cf_list', 'tcp_packets', 'udp_packets',
                'icmp_packets', 'http_packets', 'tls_packets',
                'ssl_packets', 'dns_packets',
                'TTL_max',
                'TTL_min', 'TTL_mean', 'TTL_median', 'Delta_Time_max',
                'Delta_Time_min', 'Delta_Time_mean',
                'Delta_Time_median', 'Duration', 'Content_Length_Total',
                'Content_Length_min', 'Content_Length_max',
                'Content_Length_median','total_bytes', 'total_sent_bytes',
                'total_recv_bytes',
                'label', 'sample_interval', 'multiple_label']

    httpBased = httpBased[httpBased.EPFLAG_HTTP == 1]
    httpBased = httpBased[http_col]
    httpBased = httpBased.reset_index(drop=True)

    httpsBased = httpsBased[
        (httpsBased.EPFLAG_TLS == 1) | (httpsBased.EPFLAG_SSL == 1)]

    https_col = ['FlowID', 'Source', 'Destination', 'packet_datapoint',  'control_plane' ,
          'data_plane' ,'udp_plane', 'icmp_plane',
                 'EPFLAG_ICMP', 'EPFLAG_UDP', 'EPFLAG_TCP', 'EPFLAG_DNS',
                 'EPFLAG_HTTP', 'EPFLAG_TLS', 'EPFLAG_SSL', 'EPFLAG',
                 'fqdn_lists', 'fqdn_ns_lists', 'fqdn_ip_lists',
                 'Server_Cipher_Suite',
                 'Client_Cipher_Suite', 'Client_Extension_Type',
                 'Client_Supported_Group',
                 'Client_EC_point_format',
                 'tcp_packets', 'udp_packets',
                 'icmp_packets', 'http_packets', 'tls_packets',
                 'ssl_packets', 'dns_packets',
                 'TTL_max', 'TTL_min', 'TTL_mean', 'TTL_median',
                 'Delta_Time_max', 'Delta_Time_min', 'Delta_Time_mean',
                 'Delta_Time_median', 'Duration', 'total_bytes',
                 'total_sent_bytes',
                 'total_recv_bytes',
                 'Client_Cipher_Suites_Length_min',
                 'Client_Cipher_Suites_Length_max',
                 'Client_Cipher_Suites_Length_median',
                 'Total_Encrypted_Bytes',
                 'Total_Encrypted_Sent_Bytes', 'Total_Encrypted_Recv_Bytes',
                 'Client_Extensions_Length_min',
                 'Client_Extensions_Length_max',
                 'Client_Extensions_Length_median', 'label',
                 'sample_interval', 'multiple_label'
                 ]
    httpsBased = httpsBased[https_col]
    httpsBased = httpsBased.reset_index(drop=True)

    tcpudp_col = ['FlowID', 'Source', 'Destination', 'packet_datapoint', 'control_plane' ,
          'data_plane' ,'udp_plane', 'icmp_plane',
                  'EPFLAG_ICMP', 'EPFLAG_UDP', 'EPFLAG_TCP', 'EPFLAG_DNS',
                  'EPFLAG_HTTP', 'EPFLAG_TLS', 'EPFLAG_SSL', 'EPFLAG',
                  'tcp_packets', 'udp_packets',
                  'icmp_packets', 'http_packets', 'tls_packets',
                  'ssl_packets', 'dns_packets', 'TTL_max',
                  'TTL_min', 'TTL_mean', 'TTL_median', 'Delta_Time_max',
                  'Delta_Time_min', 'Delta_Time_mean',
                  'Delta_Time_median',
                  'Duration', 'total_bytes',
                  'total_sent_bytes', 'total_recv_bytes',
                  'multiple_label', 'label', 'sample_interval'
                  ]

    tcpudpBased = tcpudpBased[tcpudp_col]
    tcpudpBased = tcpudpBased.reset_index(drop=True)


    return  httpBased,httpsBased,tcpudpBased
