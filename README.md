**Note: We are in the process of updating the repository, and it will be ready on 15 July 2022.
The data and codes can still be checked, but please come back later** 




# About 
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



# Architecture
EarlyCrow is composed of four main processes, as depicted in Figure 3. First, it starts with buffering and dispatching using Pair-
Flow, which summarizes a PCAP into contextually relevant fields including packet behavior, domain and URL list, User-Agent, status
code, and content type for HTTP. After the PairFlow HTTP variant is generated, these flows are preprocessed for profile pivoting
to generate three profiles: Host, Destination, and URL. Then, two types of feature extraction follow (PairFlow and profile features)
to form a ContextualSummary which is then classified by a random forest. When another PairFlow is received, it will follow the
same workflow. A further step is required when the new PairFlow matches one of the previous ContextualSummary ID in the repository.
The ContextualSummary updating process is responsible for updating the matched ContextualSummary to maintain the
contextualization and reclassify again. 

<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/EarlyCrow/figures/EarlyCrow_arch.png"  width="1039" height="350">
  </a>

  </p>
</div>




### Installation

* Clone the repo


   ```sh
   git clone pip install https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/
   ```
   
* Prerequests

Before running any files, please make sure to install prerequests packages
  ```sh
  pip install -r requirements.txt
  ```

### Measurement Study: 


  ```sh
  python experiments/measurements_study.py
  ```
<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/EarlyCrow/experiments/figures/features_diversity.png"  width="1700" height="600">
  </a>

  </p>
</div>
### Compile EarlyCrow
1- 
  ```sh
  python EarlyCrow/dataflow.py
  ```




### Results: 
1- Classification Performance on Known Malware
  ```sh
  python experiments/classification_performance_known_malware.py
  ```

2- Classification Performance on Unseen Malware
  ```sh
  python experiments/classification_performance_unseen_malware.py
  ```

3- Features Diversity
  ```sh
  python experiments/unseen_malware_features_diversity.py
  ```
<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/EarlyCrow/experiments/figures/features_diversity.png"  width="800" height="500">
  </a>

  </p>
</div>
4- Top Features Distribution
  ```sh
  python experiments/unseen_malware_top_features_distrbution.py
  ```
<p align="right">(<a href="#top">back to top</a>)</p>

<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/EarlyCrow/experiments/figures/top_features_distribution.png"  width="1800" height="250">
  </a>

  </p>
</div>

