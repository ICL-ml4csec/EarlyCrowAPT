import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
PATH = "./data/contextual_summaries/"
FILE_Train='training.csv'
df_train=pd.read_csv(PATH+FILE_Train)
df_cdf = pd.DataFrame(columns=['Feature','Label','X','Y'])
df_temp = pd.DataFrame(columns=['Feature','Label','X','Y'])
n_bins = 100
color_apt = 'r'
color_botnet = 'blueviolet'
color_legitimate = 'royalblue'
def attach_df(_n,_bins,_df_cdf,_LABEL,_FEATURE):
    df_temp = pd.DataFrame(columns=['Feature', 'Label', 'X', 'Y'])
    df_temp['X'] = pd.Series(_bins)
    df_temp['Y'] = pd.Series(_n)
    df_temp['Label'] = df_temp.Label.fillna(_LABEL)
    df_temp['Feature'] = _FEATURE
    return _df_cdf.append(df_temp, ignore_index=True)

def view_cdf(_FEATURE,_minY ,_maxY):
    return df_cdf.loc[(df_cdf.Feature==_FEATURE) &
                      (df_cdf.Y<=_maxY) &
                      (df_cdf.Y>=_minY)]

plt.figure(figsize=(12, 5))
fig = gridspec.GridSpec(3, 6)
ax= plt.subplot(fig[0])
plt.rcParams['font.family'] = "serif"

n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_httpRatio, n_bins, range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf['X']=pd.Series(bins)
df_cdf['Y']=pd.Series(n)
df_cdf['Label']=df_cdf.Label.fillna("APT")
df_cdf['Feature']="PF_httpRatio"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_httpRatio, n_bins,range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_httpRatio")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_httpRatio, n_bins,range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_httpRatio")
major_ticks_x = np.arange(0, 0.6, 0.2)
minor_ticks_x = np.arange(0, 0.6, 0.2/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('HTTP Ratio', fontsize=10)
ax.set_ylabel('CDF', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[1])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_dnsRatio, n_bins, range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)

df_cdf=attach_df(n,bins,df_cdf,"APT","PF_dnsRatio")
n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_dnsRatio, n_bins,range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_dnsRatio")
n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_dnsRatio, n_bins,range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_dnsRatio")
major_ticks_x = np.arange(0, 0.6, 0.2)
minor_ticks_x = np.arange(0, 0.6, 0.2/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('DNS Ratio', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[2])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_dnsReqNo, n_bins, range=[0, 40], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_dnsReqNo")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_dnsReqNo, n_bins,range=[0, 40], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_dnsReqNo")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_dnsReqNo, n_bins,range=[0, 40], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_dnsReqNo")
major_ticks_x = np.arange(0, 41, 10)
minor_ticks_x = np.arange(0, 41, 10/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('DNS Requests', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()


ax= plt.subplot(fig[3])
plt.rcParams['font.family'] = "serif"

n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_tcpRatio, n_bins, range=[0, df_train.PF_tcpRatio.max()], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_tcpRatio")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_tcpRatio, n_bins,range=[0, df_train.PF_tcpRatio.max()], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_tcpRatio")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_tcpRatio, n_bins,range=[0, df_train.PF_tcpRatio.max()], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_tcpRatio")
major_ticks_x = np.arange(0, 1.1, 0.4)
minor_ticks_x = np.arange(0, 1.1, 0.4/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Raw TCP Ratio', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
ax= plt.subplot(fig[4])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_RecvSentBytes, n_bins, range=[0, 5], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_RecvSentBytes")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_RecvSentBytes, n_bins,range=[0, 5], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_RecvSentBytes")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_RecvSentBytes, n_bins,range=[0, 5], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_RecvSentBytes")
major_ticks_x = np.arange(0, 5.1, 1.3)
minor_ticks_x = np.arange(0, 5.1, 1.3/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Received Sent Bytes Ratio', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[5])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_ResumedConnectionsNo, n_bins, range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_ResumedConnectionsNo")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_ResumedConnectionsNo, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_ResumedConnectionsNo")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_ResumedConnectionsNo, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)

df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_ResumedConnectionsNo")
major_ticks_x = np.arange(0, 22, 7)
minor_ticks_x = np.arange(0, 22, 7/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Resumed Connections', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[6])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_Max_idleTime, n_bins, range=[0,400], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_Max_idleTime")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_Max_idleTime, n_bins,range=[0, 400], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_Max_idleTime")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_Max_idleTime, n_bins,range=[0, 400], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_Max_idleTime")
major_ticks_x = np.arange(0, 401, 150)
minor_ticks_x = np.arange(0, 401, 150/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Idle Time', fontsize=10)
ax.set_ylabel('CDF', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

ax= plt.subplot(fig[7])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].Delta_Time_mean, n_bins, range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","Delta_Time_mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].Delta_Time_mean, n_bins,range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","Delta_Time_mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].Delta_Time_mean, n_bins,range=[0, 0.5], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","Delta_Time_mean")
major_ticks_x = np.arange(0, 0.51, 0.2)
minor_ticks_x = np.arange(0, 0.51, 0.2/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Delta Time', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[8])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_magnitudeMax_outliers, n_bins, range=[0, df_train.PF_magnitudeMax_outliers.max()/10], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_magnitudeMax_outliers")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_magnitudeMax_outliers, n_bins,range=[0, df_train.PF_magnitudeMax_outliers.max()/10], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_magnitudeMax_outliers")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_magnitudeMax_outliers, n_bins,range=[0, df_train.PF_magnitudeMax_outliers.max()/10], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_magnitudeMax_outliers")
major_ticks_x = np.arange(0, df_train.PF_magnitudeMax_outliers.max()/10, df_train.PF_magnitudeMax_outliers.max()/20)
minor_ticks_x = np.arange(0, df_train.PF_magnitudeMax_outliers.max()/10, df_train.PF_magnitudeMax_outliers.max()/100)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Max Magnitude Outliers', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[9])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_total_getpost, n_bins, range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_total_getpost")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_total_getpost, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_total_getpost")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_total_getpost, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_total_getpost")

major_ticks_x = np.arange(0, 20.1,5 )
minor_ticks_x = np.arange(0, 20.1, 5/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('GET & Post Req.', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[10])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_cf_htmlRatio, n_bins, range=[0, 1], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_cf_htmlRatio")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_cf_htmlRatio, n_bins,range=[0, 1], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_cf_htmlRatio")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_cf_htmlRatio, n_bins,range=[0, 1], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_cf_htmlRatio")
major_ticks_x = np.arange(0, 1.1, 0.5)
minor_ticks_x = np.arange(0, 1.1, 0.5/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('HTML Declartion Ratio', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[11])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].PF_cf_imageRatio, n_bins, range=[0, 1], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","PF_cf_imageRatio")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].PF_cf_imageRatio, n_bins,range=[0, 1], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","PF_cf_imageRatio")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].PF_cf_imageRatio, n_bins,range=[0, 1], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","PF_cf_imageRatio")
major_ticks_x = np.arange(0, 1.1, 0.5)
minor_ticks_x = np.arange(0, 1.1, 0.5/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Image Declartion Ratio', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[12])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].DP_PacketFailure_Mean, n_bins, range=[0, 5], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","DP_PacketFailure_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].DP_PacketFailure_Mean, n_bins,range=[0, 5], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","DP_PacketFailure_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].DP_PacketFailure_Mean, n_bins,range=[0, 5], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","DP_PacketFailure_Mean")
major_ticks_x = np.arange(0, 5.1, 2)
minor_ticks_x = np.arange(0, 5.1, 2/5)

major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Mean Packet Failure', fontsize=10)
ax.set_ylabel('CDF', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[13])
plt.rcParams['font.family'] = "serif"

n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].UP_Distinct_url, n_bins, range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","UP_Distinct_url")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].UP_Distinct_url, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","UP_Distinct_url")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].UP_Distinct_url, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","UP_Distinct_url")
major_ticks_x = np.arange(0, 21, 5)
minor_ticks_x = np.arange(0, 21, 5/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Distinct URLs', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

ax= plt.subplot(fig[14])
plt.rcParams['font.family'] = "serif"

n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].UP_URL_Length_Mean, n_bins, range=[0, df_train.UP_URL_Length_Mean.max()], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","UP_URL_Length_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].UP_URL_Length_Mean, n_bins,range=[0, df_train.UP_URL_Length_Mean.max()], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","UP_URL_Length_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].UP_URL_Length_Mean, n_bins,range=[0, df_train.UP_URL_Length_Mean.max()], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","UP_URL_Length_Mean")
major_ticks_x = np.arange(0, 250, 100)
minor_ticks_x = np.arange(0, 250, 100/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('URL Length', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

ax= plt.subplot(fig[15])
plt.rcParams['font.family'] = "serif"

n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].UP_Depth_Mean, n_bins, range=[0, 10], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","UP_Depth_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].UP_Depth_Mean, n_bins,range=[0,10], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","UP_Depth_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].UP_Depth_Mean, n_bins,range=[0, 10], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","UP_Depth_Mean")
major_ticks_x = np.arange(0, 11, 5)
minor_ticks_x = np.arange(0, 11, 5/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('URL Depth', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[16])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].UP_No_Para_Mean, n_bins, range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","UP_No_Para_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].UP_No_Para_Mean, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","UP_No_Para_Mean")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].UP_No_Para_Mean, n_bins,range=[0, 20], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","UP_No_Para_Mean")
major_ticks_x = np.arange(0, 21, 5)
minor_ticks_x = np.arange(0, 21, 5/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('URL Parameters', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.tight_layout()

ax= plt.subplot(fig[17])
plt.rcParams['font.family'] = "serif"
n, bins, patches = ax.hist(df_train[df_train.capture_type=="APT"].HP_DestByIP, n_bins, range=[0, df_train.HP_DestByIP.max()], density=True, histtype='step',
                           cumulative=True, label='APT',linewidth=2,color=color_apt)
df_cdf=attach_df(n,bins,df_cdf,"APT","HP_DestByIP")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="botnet"].HP_DestByIP, n_bins,range=[0, df_train.HP_DestByIP.max()], density=True, histtype='step',
                           cumulative=True, label='botnet',linewidth=2,color=color_botnet)
df_cdf=attach_df(n,bins,df_cdf,"botnet","HP_DestByIP")

n, bins, patches = ax.hist(df_train[df_train.capture_type=="legitimate"].HP_DestByIP, n_bins,range=[0, df_train.HP_DestByIP.max()], density=True, histtype='step',
                           cumulative=True, label='legitimate',linewidth=2,color=color_legitimate)
df_cdf=attach_df(n,bins,df_cdf,"legitimate","HP_DestByIP")
major_ticks_x = np.arange(0, 1.1, 0.4)
minor_ticks_x = np.arange(0, 1.1, 0.4/5)
major_ticks_y = np.arange(0, 1.1, 0.2)
minor_ticks_y = np.arange(0, 1.1, 0.05)
ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)
ax.grid(which='minor', alpha=0.3)
ax.grid(which='major', alpha=0.5)
ax.set_xlabel('Destination With IP', fontsize=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
ax.legend(loc='lower right',prop={'size': 9})
plt.tight_layout()
plt.savefig('experiments/figures/Measurement.pdf')
plt.show()