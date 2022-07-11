# Datasets
To reproduce our data and replicate experiments, we publish our data at all stages and describe how to produce each one. 

### EarlyCrow Data
To run all experiments, you only need to generate the data from EarlyCrow which is stored in `data/contextual_summaries/`

### PairFlow Data
 To run EarlyCrow, you need data at PairFlow level. These can be found in `data/pairflows/`. 

1- Our data files are stored separately from GitHub due to their size. Please download data from Google Drive as follows:
 Download the raw data in the folder path `\data\pcap\`

```wget https://drive.google.com/file/d/19YDapH-hdcj5okuVHaNfInfWlb4emLd2/view?usp=sharing```

2- Compile the raw data using `PairFlow_data_format` module.

``` python PairFlow_data_format.py ``` 

3- File will be stored automaltcally in `\data\pairflows\[FileName]`

### PCAP Data
To run PairFlow, you can access the raw data stored in  `data/pcap/csv/`. Then following the instruction here to generate PairFlows. 
### Running Experiements:

You can directly use the ContextualSummaries in `\EarlyCrowAPT\data\contextual_summaries\`. Therefore, you only need to follow the instructions in the <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/">Main Page</a>. 







