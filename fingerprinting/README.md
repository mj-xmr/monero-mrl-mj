# Fingerprinting

Documenting and experimenting on the fingerprinting of Monero's forks.

## Strategy

- Because the test encompasses multiple Monero versions, a [multi-version compatible patch](https://github.com/mj-xmr/monero-patches/blob/master/src/mrl-decoy-fee-ut-clsag.patch) shall be maintained and tested for compatibility using GitHub Actions.
- The differences in behavior captured across the relevant Monero versions are expected to be reflected in the forks, suspected of being fingerprintable. The methodology to collect & visualize the differences shall be as close to the Monero's patch, as possible.
- A timeline shall be presented, that combines all the intervening, relevant versions of software, where it's easier to infer the chronology.
- Plots shall be prepared as tools for manual inference, inspired by [Fingerprinting a flood](https://mitchellpkt.medium.com/fingerprinting-a-flood-forensic-statistical-analysis-of-the-mid-2021-monero-transaction-volume-a19cbf41ce60), by Mitchell P. Krawiec-Thayer, PhD (aka Isthmus).
- Blockchain shall be analyzed to find the alleged fingerprints. In order to perform this efficiently, a framework shall be prepared, based on [this unmerged PR #8264](https://github.com/monero-project/monero/pull/8264), and [its followup patch](https://github.com/mj-xmr/monero-patches/blob/master/src/testnet-scripts.patch) already under CI. The framework will ease the performance of experiments on the Blockchain in a non-destructive way, using private Testnet.
- The public shall be enabled to verify the steps, by delivering easy to use tools to convert the blockchain into data, readable by Python scripts. Preliminary work has already been done via [A data conversion and plotting script](src/fee.py), [data extraction scripts](../generic/src/) as well as a [relevant PR to an external project](https://github.com/moneroexamples/transactions-export/pull/33), with possibly more such PRs to come.
- After confirming the act of fingerprinting, a solution shall be presented for a review and ideally applied across the Monero space.


## Results

Except for the last point, namely the mathematical expression, the research project already delivers satisfying results.

## Visualization

### Unit tests

We will want to achieve the same result on the allegedly fingerprintable forks: capturing differences between the returned values across various public versions of the forks. 
The above Monero-Core example serves primarily as a test of the methodology.

![clsag uts](https://user-images.githubusercontent.com/63722585/200007357-559d604d-d610-4902-8ac5-45cc0d363e21.png)

### Patches CI

An example of an easily accessible report, generated on schedule, displaying the final status of each patch for each version under test. This helps with keeping consistency of the patches across the versions.

![Patches CI](https://user-images.githubusercontent.com/63722585/200007682-022ecfc5-4bbc-4d17-80a3-11c5a297096f.png)



### Fees line

Line plot of the (logarithm) of fees:

![plot fees linear](https://user-images.githubusercontent.com/63722585/200007775-3e3300da-cb8f-4c25-9f83-6e1e3dda5c89.png)

### Fees heightmap logarithmic scaling

The same in a different, clustered representation and log scaling:

![plot fees heightmap logarithmic](https://user-images.githubusercontent.com/63722585/200007860-9522a705-55f7-4e50-82ec-0587eef1885e.png)

### Fees heightmap linear scaling

Now scaled linearly: 

![plot fees heightmap linear](https://user-images.githubusercontent.com/63722585/200007958-8a1e9845-b306-4bbd-ad48-56ddab8fb989.png)

Compare with Isthmus' fees plot:

![Isthmus fees](https://user-images.githubusercontent.com/63722585/200008485-42e7fd03-ff30-46d5-8783-f5af43bdfb59.png)


## Time tables

[All tags](doc/tags)

[Filtered tags, showing a delay in MyMonero's update](doc/tags/tags-filtered.md), only until public version `v1.2.6`  as reprinted below:

Date       | Project 		|      Tag                | Descr
---------- | ------------------ | ----------------- 	| -----------------
2022-04-07 11:43:45 | mm-app-js- 	| v1.2.6 		| Merge pull request #472 from mymonero/develop
2022-02-28 02:58:43 | mm-core-cpp-c 	| 2a5d944 		| Re-use the same set of outs and associated mix outs across tx construction attempts
2022-02-28 02:55:41 | mm-core-cpp-c 	| 9032a05 		| Update fee calc to use CLSAG + other minor changes
2022-01-20 10:53:31 | mm-app-js- 	| v1.2.5 		| Merge pull request #453 from mymonero/develop
2021-11-30 17:07:33 | monero-core 	| v0.17.3.0 		| Oxygen Orion, Point Release 3.0
2021-11-08 14:29:24 | mm-app-js- 	| v1.2.1 		| Merge pull request #430 from mymonero/develop
2021-10-07 14:04:33 | mm-app-js- 	| v1.2.0 		| Merge pull request #424 from mymonero/develop
2021-08-29 12:30:57 | monero-core 	| v0.17.2.3 		| Oxygen Orion, Point Release 2.3
2021-07-06 13:02:41 | mm-app-js- 	| v1.1.22 		| Merge pull request #393 from mymonero/develop
2021-06-08 11:42:09 | mm-core-cpp-c 	| 79413fb 		| Update monero-core-custom to 0.17.2.0
2021-04-30 13:01:04 | mm-app-js- 	| v1.1.21 		| Merge pull request #383 from mymonero/develop
2021-04-06 12:25:41 | monero-core 	| v0.17.2.0 		| Oxygen Orion, Point Release 2.0



## Verification & usage

[Process (WIP)](doc/process.md)

TBD.
