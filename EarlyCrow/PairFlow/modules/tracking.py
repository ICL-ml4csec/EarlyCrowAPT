import pandas as pd
import re
pat = re.compile(' A ([a-zA-Z0-9-.]+)')
pat_ns = re.compile('NS ([a-zA-Z0-9-.]+)')

pat_full = re.compile(' A ([0-9-.]+)')
pat_ip = re.compile(' A ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)')
def tracking_packets(df, GRANULARITY, gr):
    df_tcp_udp = df.loc[
        (df.EPFLAG_TCP == 1) | (df.EPFLAG_UDP == 1) | (
                df.EPFLAG_HTTP == 1)]

    # this is to bring all packets that has extrenal connection, we add HTTP too
    # for external connection for those does not use raw tcp or udp at all
    # but we stick to df_tcp_udp as HTTP is built on the top of such protocols

    # for ICMP
    df_tcp_udp_icmp = df.loc[
        (df.EPFLAG_TCP == 1) | (df.EPFLAG_UDP == 1) | (
                    df.EPFLAG_ICMP == 1)]

    # here we can find all unique bidirectional flow to find sent and recieve packet length bytes
    conn_pairs_df = df_tcp_udp.groupby(
        by=['Source', 'Destination']).Length.sum()
    conn_pairs_df = conn_pairs_df.reset_index()
    if len(conn_pairs_df) == 0:
        print("No packets found in a given time interval ({},{})"
              .format(gr * GRANULARITY, gr * GRANULARITY + GRANULARITY),
              end='\r')
        return conn_pairs_df ## for those time interval the does not have any connection, break and
    conn_pairs_unique_df = pd.DataFrame(index=[0],
                                        columns=conn_pairs_df.columns)
    for i in range(len(conn_pairs_df)):
        if i == 0:
            conn_pairs_unique_df.iloc[0] = conn_pairs_df.iloc[i]
        else:

            for j in range(len(conn_pairs_unique_df)):
                if ((conn_pairs_df.loc[i, 'Source'] ==
                     conn_pairs_unique_df.loc[
                         j, 'Destination']
                     and conn_pairs_df.loc[i, 'Destination'] ==
                     conn_pairs_unique_df.loc[j, 'Source'])):
                    j = len(
                        conn_pairs_unique_df)  # for last flow if duplicate, so won't be bypass the next condition
                    break
            if j == len(conn_pairs_unique_df) - 1:
                conn_pairs_unique_df = conn_pairs_unique_df.append(
                    conn_pairs_df.iloc[i])
                conn_pairs_unique_df = conn_pairs_unique_df.reset_index(
                    drop=True)
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

    return conn_pairs_unique_df


def tracking_dns(df, flow_biPkts, GRANULARITY, gr):
    ########################
    ## START: DNS PACKETS ##
    ########################
    domain_list = []
    ns_list = []
    ip_list = []
    # find the dns related response packets first by find any dns packets includes the destination
    dnsRes_packets = pd.DataFrame(columns=flow_biPkts.columns)
    # find the dns related response packets first by find any dns packets includes the destination
    if len(df[df.Info.str.contains(
            flow_biPkts.loc[0, 'Destination'])]) > 0:
        dnsRes_packets = df[df.Info.str.contains(
            flow_biPkts.loc[0, 'Destination'])]

    dnsRes_packets = dnsRes_packets.reset_index(drop=True)
    dnsRes_packets = dnsRes_packets[dnsRes_packets.EPFLAG_DNS == 1]
    dnsRes_packets_unique = dnsRes_packets.copy(deep=True)
    if len(dnsRes_packets_unique) > 0:
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

            # ip_list=a_rr_ips
            domain_res = list(
                set(a_rr).symmetric_difference(set(a_rr_ips)))
            try:
                domain_list.append(domain_res[0])
                ip_list.append(tuple(a_rr_ips))
                ns_list.append(tuple(ns_rr))
            except:
                pass

            # if len(flow_biPkts[flow_biPkts.EPFLAG_DNS==1]) !=0:
            try:

                if j == 0:

                    dnsReq_packets = df[df.Info.str.contains(domain_res[
                                                                 0])]  ## domain_res[0] is indexed with
                    # zero because a list with one element
                    # always
                else:
                    dnsReq_packets_new = df[
                        df.Info.str.contains(domain_res[0])]
                    dnsReq_packets = dnsReq_packets.append(
                        dnsReq_packets_new)

                dnsReq_packets = dnsReq_packets.drop_duplicates()
                dnsReq_packets = dnsReq_packets[
                    dnsReq_packets.Relative_Time < gr * GRANULARITY + GRANULARITY]  # filter out beoynd time window for now
                dnsReq_packets = dnsReq_packets.reset_index(drop=True)
                flow_biPkts = flow_biPkts.append(dnsReq_packets)
                flow_biPkts = flow_biPkts.append(dnsRes_packets)
            # else:
            except:
                # print("Flow Does not use DNS request and response")
                pass
    else:
        # print("No DNS Packets")
        pass



    ######################
    ## END: DNS PACKETS ##
    ######################

    return flow_biPkts,domain_list, ns_list, ip_list