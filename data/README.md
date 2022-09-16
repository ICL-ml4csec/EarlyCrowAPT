# Datasets
To reproduce our data and replicate experiments, we publish our data at all stages and describe how to produce each one. 


### PCAP Data
To generate PairFlow from PCAP, you need to access the raw data stored in  `data/pcap/csv/`. Then following the instruction <a href="https://github.com/ICL-ml4csec/EarlyCrowAPT/tree/EarlyCrow/PairFlow_data_format/">here</a> to generate PairFlows. 


### PairFlow Data
To run EarlyCrow, you need data at PairFlow level. These can be found in `data/pairflows/merged_pairflow_files/`. 

1- Our data files are stored separately from GitHub due to their size. Please download data from Google Drive as follows:
 Download the raw data in the folder path `/data/pcap/csv/`

```wget https://drive.google.com/file/d/1kJI-MPFpfMJgyZpHyBRpDE_DIvQCrheB/view?usp=sharing```

2- Compile the raw data using `PairFlow_data_format` module.

``` python PairFlow_data_format.py ``` 

3- File will be stored automatically in `/data/pairflows/[FileName]`



### EarlyCrow Data
To run all experiments, you only need to generate the ContextualSummaries of EarlyCrow which is stored in `/data/contextual_summaries/`


### Dataset for all experiments:

You can directly use the ContextualSummaries in `/EarlyCrowAPT/data/contextual_summaries/`. Therefore, you only need to follow the instructions in the <a href="https://github.com/ICL-ml4csec/EarlyCrowAPT/">Main Page</a>. 







