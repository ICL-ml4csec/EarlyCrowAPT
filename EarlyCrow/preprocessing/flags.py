import numpy as np


def packetsFlags(_df):
    _df['EPFLAG_ICMP'] = np.where((_df['Protocol']== 'ICMP') | (_df['Protocol']== 'ICMPv6'), 1, 0)
    _df['EPFLAG_UDP'] = np.where(_df['Protocol']== 'UDP', 1, 0)
    _df['EPFLAG_TCP'] = np.where(_df['Protocol']== 'TCP', 1, 0)
    _df['EPFLAG_DNS'] = np.where(_df['Protocol']== 'DNS', 1, 0)
    _df['EPFLAG_HTTP'] = np.where(_df['Protocol']== 'HTTP', 1, 0)
    _df['EPFLAG_HTTP_XML'] = np.where(_df['Protocol']== 'HTTP/XML', 1, 0)
    _df['EPFLAG_TLS'] =np.where((_df['Protocol'] == 'TLSv1') |
                                (_df['Protocol'] == 'TLS1.2') |
                                (_df['Protocol'] == 'TLS1.3'), 1, 0)
    _df['EPFLAG_SSL'] = np.where(_df['Protocol']== 'SSLv3.2', 1, 0)
    

    
    _df["EPFLAG"] = _df["EPFLAG_ICMP"].astype(str) +\
                   _df["EPFLAG_UDP"].astype(str) +\
                   _df["EPFLAG_TCP"].astype(str)+\
                   _df["EPFLAG_DNS"].astype(str)+\
                   _df["EPFLAG_HTTP"].astype(str)+\
                   _df["EPFLAG_HTTP_XML"].astype(str)+\
                   _df["EPFLAG_TLS"].astype(str)+\
                   _df["EPFLAG_SSL"].astype(str)

    return _df


