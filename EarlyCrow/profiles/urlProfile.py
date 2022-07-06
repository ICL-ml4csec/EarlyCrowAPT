import pandas as pd


def url_features_extractor(_df):
    PRINT_MESSAGE="\n*** URL Profile Features Extractions"
    print("{}".format(PRINT_MESSAGE))

    _df['has_url'] = _df.url_cf_list.apply(len)
    url_df = _df[_df['has_url'] > 0]
    url_df = url_df.reset_index(drop=True)


    serialized_url=pd.DataFrame(columns=['binary_labels','multiple_labels','Source','Destination',
                                             'fqdn','url','Filename','Depth',
                                             'No_Para','No_Values','No_Frag',
                                             'Has_query_string','Referer',
                                             'Cookie'])
    PRINT_MESSAGE="URLs resources analysis"

    for i in range(0,len(url_df)):
        print(
            "{} {}%".format(PRINT_MESSAGE,round((i/len(url_df))*100,1)), end='\r')
        single_list = url_df.loc[i, 'url_cf_list']
        for j, single_list in enumerate(single_list):

            serialized_url = serialized_url.append({'binary_labels': url_df.loc[
                        i, 'label'],'multiple_labels': url_df.loc[i, 'multiple_label'],
                    'Source': url_df.loc[i, 'Source'], 'Destination' : url_df.loc[i, 'Destination'],
                    'fqdn':single_list[0], 'url': single_list[1], 'Filename': single_list[2],
                     'Depth': single_list[3] ,'No_Para': single_list[4], 'No_Values': single_list[5],
              'No_Frag': single_list[6],  'Has_query_string': single_list[7],
             'Referer': single_list[8], 'Cookie': single_list[9] }, ignore_index=True)

    print('{} - Done'.format(PRINT_MESSAGE))

    #single_list=url_df.loc[14250,'url_cf_list']

    single_list_backup=serialized_url.copy(deep=True)
    #single_list_backup.to_csv("D:\Dropbox\Personal\PhD Project\Third Year\Traffic Data Collection\csv/full_data/07042021url_profile_directFrom_url_cf_list.csv",index=False)
    #serialized_url=pd.read_csv("D:\Dropbox\Personal\PhD Project\Third Year\Traffic Data Collection\csv/full_data/07042021url_profile_directFrom_url_cf_list.csv")

    serialized_url=serialized_url.drop_duplicates(subset=['multiple_labels','fqdn','Source','Destination','url'])
    serialized_url=serialized_url.reset_index(drop=True)

    serialized_url['No_Para']=serialized_url.No_Para.str.replace("[a-zA-Z_]+\s","").astype(float)
    serialized_url['Depth']=serialized_url.Depth.str.replace("[a-zA-Z_]+\s","").astype(float)
    serialized_url['No_Values']=serialized_url.No_Values.str.replace("[a-zA-Z_]+\s","").astype(float)
    serialized_url['No_Frag']=serialized_url.No_Frag.str.replace("[a-zA-Z_]+\s","").astype(float)


    serialized_url['url_idx']=1
    serialized_url['URL_Length']=serialized_url.url.apply(len)

    url_col=serialized_url.columns

    distinct_url_df=serialized_url.copy(deep=True)
    distinct_url_df=distinct_url_df.drop_duplicates(subset=['multiple_labels','Source','Destination','fqdn','url'])
    distinct_url_df=distinct_url_df.reset_index(drop=True)



    distinct_url_df.loc[(distinct_url_df['Has_query_string'] == True), 'Has_query_string_idx'] = 1
    distinct_url_df.loc[(distinct_url_df['Filename'] != 'No Filename'), 'Has_Filename_idx'] = 1
    distinct_url_df.loc[(distinct_url_df['Filename'].str.contains(".exe")), 'Has_exe_idx'] = 1



    distinct_url_df.Has_query_string_idx.fillna(0,inplace=True)
    distinct_url_df.Has_Filename_idx.fillna(0,inplace=True)
    distinct_url_df.Has_exe_idx.fillna(0,inplace=True)


    distinct_url_df=distinct_url_df.groupby(['multiple_labels','fqdn','Source','Destination'])["url_idx", "Has_query_string_idx","Has_Filename_idx","Has_exe_idx"].apply(lambda x : x.astype(int).sum())
    distinct_url_df=distinct_url_df.reset_index(drop=False)
    distinct_url_df=distinct_url_df.rename(columns={'url_idx': "UP_Distinct_url",'Has_query_string_idx': "UP_Num_hasString",'Has_Filename_idx': "UP_Num_Filename",'Has_exe_idx':'UP_num_exe'})
    URL_stat=distinct_url_df[['multiple_labels','Source','Destination','fqdn','UP_Distinct_url','UP_Num_hasString','UP_Num_Filename','UP_num_exe']]
    URL_stat['UP_Frac_query']=URL_stat['UP_Num_hasString']/URL_stat['UP_Distinct_url']
    URL_stat['UP_Frac_URL_filename']=URL_stat['UP_Num_Filename']/URL_stat['UP_Distinct_url']
    URL_stat['UP_Frac_URL_filename_exe']=URL_stat['UP_num_exe']/URL_stat['UP_Distinct_url']

    ###############


    def URL_min_mean_max(_serialized_url,_url_stat,_FEATURE):
        _temp = _serialized_url.groupby(
            by=['multiple_labels','fqdn','Source','Destination'])[_FEATURE].max()
        _temp = _temp.reset_index(drop=False)
        _temp = _temp.rename(
            columns={_FEATURE: 'UP_'+_FEATURE+'_Max'})
        _url_stat['UP_'+_FEATURE+'_Max'] = _temp[
            'UP_'+_FEATURE+'_Max']

        _temp = _serialized_url.groupby(
            by=['multiple_labels','fqdn','Source','Destination'])[_FEATURE].min()
        _temp = _temp.reset_index(drop=False)
        _temp = _temp.rename(
            columns={_FEATURE: 'UP_'+_FEATURE+'_Min'})
        _url_stat['UP_'+_FEATURE+'_Min'] = _temp[
            'UP_'+_FEATURE+'_Min']

        _temp = _serialized_url.groupby(
            by=['multiple_labels','fqdn','Source','Destination'])[_FEATURE].mean()
        _temp = _temp.reset_index(drop=False)
        _temp = _temp.rename(
            columns={_FEATURE: 'UP_'+_FEATURE+'_Mean'})
        _url_stat['UP_'+_FEATURE+'_Mean'] = _temp[
            'UP_'+_FEATURE+'_Mean']



        return _url_stat

    spec=['URL_Length','Depth', 'No_Para', 'No_Values', 'No_Frag']
    for s in spec:
        URL_stat=URL_min_mean_max(serialized_url,URL_stat,s)



    ### Transfer to Contextul Flow
    URL_col=URL_stat.columns
    URL_col=URL_col[4:]
    scalar_col=URL_col
    PRINT_MESSAGE="Transfer URL statstics to contextual summaries"
    for i in range(len(URL_stat)):
        print(
            "{} {}%".format(PRINT_MESSAGE,
                            round((i / len(URL_stat)) * 100, 1)),
            end='\r')
        for col in  scalar_col:
            _df.loc[(_df['multiple_label'] == URL_stat.loc[i, 'multiple_labels']) &
                              (_df['Source'] == URL_stat.loc[i, 'Source'])  &
                              (_df['Destination'] == URL_stat.loc[i, 'Destination']),
                              '{}'.format(col)] = URL_stat.loc[i, '{}'.format(col)]

    print('{} - Done'.format(PRINT_MESSAGE))

    ## for those that did not have a url and use  HTTP in CF, it should be reset values to zero means no url, No Para/Value/fragment, zero length ..etc
    for col in  scalar_col:
        _df.fillna({'{}'.format(col): 0}, inplace=True)

    return _df


