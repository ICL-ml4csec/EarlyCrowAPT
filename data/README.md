# Data

### Running Experiements:

You can directly use the ContextualSummaries in `\EarlyCrowAPT\data\contextual_summaries\`. Therefore, you do only need to do the intrsuctions in the <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/">Main Page</a>. 

#### PairFlow
If you want to access to our raw data and compile our proposed PairFlow data format to export .csv files for our data or for your own data, Please execute the followings:

1- Our data files are stored separately from GitHub due to their size. Please download data from Google Drive as follows:
 Download the raw data in the folder path `\data\pcap\`

```wget https://drive.google.com/file/d/19YDapH-hdcj5okuVHaNfInfWlb4emLd2/view?usp=sharing```

2- Compile the raw data using `PairFlow_data_format` module.

``` python PairFlow_data_format.py ``` 

3- File will be stored automaltcally in `\data\pairflows\[FileName]`





