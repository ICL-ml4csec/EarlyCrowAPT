# PairFlow

PairFlow is our proposed data format that allows the NIDS designer to quickly pivot flows into many profiles such as host, destination,
URL profiles. PairFlow data can also be used by detectors of malicious domains or IPs. Instead of detecting one flow according to the
initiation and termination of TCP, protocol-based or time window, PairFlow digests all information to extract features later based on
the whole context over time.

PairFlow receives raw PCAP data and stores these packets in a buffer until a time window of size 𝑡 has passed. The buffer sends
the current granular data of a time window of all connections at an enterprise network to the Tracking module to group unique pairs and label related packets. A unique pair refers to any (possibly
bidirectional) connection observed between a host on the local network and a remote server. We take the source of the pair to be
the local host, and the destination to be the remote server. Next, the Aggregator module add a PairFlow ID and time window to the
flow data. The Aggregator module is also responsible for marking packets according to their plane, extracting the domains and HTTP
fields. Next, the Encapsulation module groups all these pieces of information contextually, so that all possible TTPs in Figure 1 can
be analyzed later. Therefore, each pair of connections has a comprehensive description of their packets behavior (described in Section
A.3.1), HTTP settings, accessed domains, and cipher suites setting.

Finally, PairFlow outputs four additional json files which can be used by any external classifier. We only use the HTTP variant for
EarlyCrow. The details for each component of PairFlow can be found in Appendix A.


<br />
<div align="center">
  <a href="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/tree/EarlyCrow/PairFlow_data_format/">
    <img src="https://gitfront.io/r/user-8496580/tRoT9bsPi6hi/EarlyCrowAPT/raw/EarlyCrow/PairFlow_data_format/figures/PairFlow_arch.png" class="center"  width="1039" height="350">
  </a>

  </p>
</div>

## Compile data using PairFlow
1- Generate PairFlow for all files and store them in `\data\pairflows\`
``` python EarlyCrow/PairFlow_data_format/PairFlowGenerator.py ```

2- Unify all generated PairFlows for each trace into one file

``` python EarlyCrow/PairFlow_data_format/unify_data.py ```

3- Generate all possible files variants

``` python EarlyCrow/PairFlow_data_format/file_variants.py ```



