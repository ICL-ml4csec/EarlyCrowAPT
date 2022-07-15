<br />

<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/">
    &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/EarlyCrow_logo.png" class="center"  width="700" height="148.75">
  </a>

  </p>
</div>



<i>Last Update: Friday, 15 Jul 2022 </i>




## About
Advanced Persistent Threats (APTs) are among the most sophisticated threats facing critical organizations worldwide. APTs employ
specific tactics, techniques, and procedures (TTPs) which make them difficult to detect in comparison to frequent and aggressive attacks.
In fact, current network intrusion detection systems struggle to detect APTs communications, allowing such threats to persist
unnoticed on victims’ machines for months or even years.
In this paper, we present EarlyCrow, an approach to detect APT malware Command and Control connections using contextual
summaries. The design of EarlyCrow is informed by a novel threat model focused on TTPs present in traffic generated by tools recently
used as part of APT campaigns. The threat model highlights the importance of the context around the malicious connections, and
suggests traffic attributes which help APT detection. EarlyCrow defines a novel multipurpose network flow format called PairFlow,
which is leveraged to build the contextual summary of a PCAP capture, representing key behavioral, statistical and protocol information
relevant to APT TTPs. We evaluate the effectiveness of EarlyCrow on unseen APTs obtaining a headline macro average
F1-score of 93.02% with FPR of 0.74%.


### Installation

* Clone the repo


   ```sh
   git clone https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT.git
   ```
   
* Prerequests

1- Before running any files, please make sure to install prerequisites packages
  ```sh
  pip install -r requirements.txt
  ```

2- It is required that PYTHONPATH be set up so that all EarlyCrow modules are available for use during the below commands 

```sh
export PYTHONPATH=/home/[PC_NAME]/EarlyCrowAPT/
```
### Architecture
EarlyCrow is composed of four main processes, as depicted in Figure 3. First, it starts with buffering and dispatching using <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/tree/EarlyCrow/PairFlow_data_format/">PairFlow</a>, which summarizes a PCAP into contextually relevant fields including packet behavior, domain and URL list, User-Agent, status
code, and content type for HTTP. After the PairFlow HTTP variant is generated, these flows are preprocessed for profile pivoting
to generate three profiles: Host, Destination, and URL. Then, two types of feature extraction follow (PairFlow and profile features)
to form a ContextualSummary which is then classified by a random forest. When another PairFlow is received, it will follow the
same workflow. A further step is required when the new PairFlow matches one of the previous ContextualSummary ID in the repository.
The ContextualSummary updating process is responsible for updating the matched ContextualSummary to maintain the
contextualization and reclassify again. 

  ```sh
  python EarlyCrow/dataflow.py
  ```


<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/tree/EarlyCrow/">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/EarlyCrow/figures/EarlyCrow_arch.png" class="center"  width="1039" height="350">
  </a>

  </p>
</div>


## Data Preparetion
If you are interested in running the experiments directly, you can **skip** this section. 
We have already attached the training and test set in our repository to be used for the Experiment section, so you do not need to download data from our Google Drive storage. 
Google Drive storage includes all <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/tree/data/">datasets</a> for each step. 
However, this section is to regenerate (replicate) datasets based on our PCAP files or anyone interested in using EarlyCrow.

### PairFlow
You need first to use our proposed data format in our paper which is called <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/tree/EarlyCrow/PairFlow_data_format/">PairFlow</a> . 
Please <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/tree/EarlyCrow/PairFlow_data_format/">click here</a> and follow the instructions. 

### Feature Extraction
After the PairFlow is prepared and stored in ```data/pairflows/``` , the next step is to generate ContextualSummaries. Please run the following command, which includes pivoting, PairFlow and Profile feature generation, and Continual Updating process.

``` python EarlyCrow/dataflow.py```

Now the data is ready to be used for the experiments. You may run the following command to evaluate EarlyCrow on Known malware (The first experiment on the paper).
```python experiments/classification_performance_known_malware.py```

Note: make sure to update the PATH and FILENAME in the file ```classification_performance_known_malware.py``` to match your own generated data. 



## Experiements
### Measurement Study: 
We provide several measurements taken on the training set summarized in Table 1 and described in Section 4. Since our scope is
to detect APTs at the early stage, all measurements are observed during the first 15 minutes of each connection.

  ```sh
  python experiments/measurements_study.py
  ```
<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/blob/experiments/measurements_study.py">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/experiments/figures/Measurement.png" class="center"  width="850" height="300">
  </a>

  </p>
</div>



## Results: 
Classifiers are evaluated in two modes. First, HTTP-Mode, which assumes the administrator connects the NIDS to a web proxy to
decrypt HTTPS and accesses features such as UA, HTTP response codes, content type, and URL. Second, HTTPS-Mode, where the
administrator places the NIDS at the network edge, without deciphering HTTPS. 

#### Classification Performance on Known Malware.

We randomly split the training and testing sets ten times. Then, we take the average performance under two
constraints. First, the malware should be presented in both sets. Second, the infected hosts and the destination C&C server should be
unique and not leaked from training to testing.

  ```sh
  python experiments/classification_performance_known_malware.py
  ```

#### Classification Performance on Unseen Malware

We train our classifiers on the training set used for our measurement study. Then we evaluate the performance
against unseen malware.

  ```sh
  python experiments/classification_performance_unseen_malware.py
  ```

#### Features Diversity

The detection APTs necessitates a spread of features, as presented in Section 2. In Figure 4, we show the
extent to which additional features affect the performance of the various classifiers.
  ```sh
  python experiments/unseen_malware_features_diversity.py
  ```
<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/blob/experiments/unseen_malware_features_diversity.py">
    &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/experiments/figures/features_diversity.png" class="center" width="400" height="250">
  </a>

  </p>
</div>

<br />

#### Top Features Distribution

We investigate feature importance on the third dataset in HTTPS mode, which comprises APTs, botnets, and legitimate
samples because it is the one closest to a realistic scenario for APT hunting.

  ```sh
  python experiments/unseen_malware_top_features_distrbution.py
  ```

<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/blob/experiments/unseen_malware_top_features_distribution.py">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/experiments/figures/top_features_distribution.png" class="center" width="900" height="125">
  </a>

  </p>
</div>

<p align="right">(<a href="#top">back to top</a>)</p>
