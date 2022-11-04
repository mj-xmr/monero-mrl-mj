# Fingerprinting

Documenting and experimenting on the fingerprinting of Monero's forks.

## Strategy

- Because the test encompasses multiple Monero versions, a [multi-version compatible patch](https://github.com/mj-xmr/monero-patches/blob/master/src/mrl-decoy-fee-ut-clsag.patch) shall be maintained and tested for compatibility using GitHub Actions.
- The differences in behavior captured across the relevant Monero versions are expected to be reflected in the forks, suspected of being fingerprintable. The methodology to collect & visualize the differences shall be as close to the Monero's patch, as possible.
- A timeline shall be presented, that combines all the interviening, relevant versions of software, where it's easier to infer the chronology.
- Plots shall be prepared as tools for manual inference, inspired by [Fingerprinting a flood](https://mitchellpkt.medium.com/fingerprinting-a-flood-forensic-statistical-analysis-of-the-mid-2021-monero-transaction-volume-a19cbf41ce60), by Mitchell P. Krawiec-Thayer, PhD (aka Isthmus).
- Blockchain shall be analyzed to find the alleged fingerprints. In order to perform this efficiently, a framework shall be prepared, based on [this unmerged PR #8264](https://github.com/monero-project/monero/pull/8264), and [its followup patch](https://github.com/mj-xmr/monero-patches/blob/master/src/testnet-scripts.patch) already under CI. The framework will ease the performance of experiments on the Blockchain in a non-destructive way, using private Testnet.
- The public shall be enabled to verify the steps, by delivering easy to use tools to convert the blockchain into data, readable by Python scripts. Preliminary work has already been done via [A data conversion and plotting script](src/fee.py), [data extraction scripts](../generic/src/) as well as a [relevant PR to an external project](https://github.com/moneroexamples/transactions-export/pull/33), with possibly more such PRs to come.
- After confirming the act of fingerprinting, a solution shall be presented for a review and ideally applied across the Monero space.


- New unit tests shall be written, that cover the happy path and edge cases of the decoy algorithm
- The nevralgic parts of the system shall be first experimentally probed and the results shall be gathered
- An alternative Python implementation shall be prepared, since Python offers many statistical analysis and visualization tools. The correspondence between this and the original implementation shall be confirmed via the Kolmogorov-Smirnov test
- Based on the Python implementation, and R implementation shall be created and its results are confirmed via the same statistical tests
- With the R implementation at hand, a mathematical expression of the decoy algo shall be derived

## Results

Except for the last point, namely the mathematical expression, the research project already delivers satisfying results.

## Visualization

### Unit tests

![clsag uts](https://user-images.githubusercontent.com/63722585/200007357-559d604d-d610-4902-8ac5-45cc0d363e21.png)

### Patches CI

![Patches CI](https://user-images.githubusercontent.com/63722585/200007682-022ecfc5-4bbc-4d17-80a3-11c5a297096f.png)

### Fees linear

![plot fees linear](https://user-images.githubusercontent.com/63722585/200007775-3e3300da-cb8f-4c25-9f83-6e1e3dda5c89.png)

### Fees heightmap logarithmic scaling

![plot fees heightmap logarithmic](https://user-images.githubusercontent.com/63722585/200007860-9522a705-55f7-4e50-82ec-0587eef1885e.png)

### Fees heightmap linear scaling

![plot fees heightmap linear](https://user-images.githubusercontent.com/63722585/200007958-8a1e9845-b306-4bbd-ad48-56ddab8fb989.png)

Compare with Isthmus' fees plot:

![Isthmus fees](https://user-images.githubusercontent.com/63722585/200008485-42e7fd03-ff30-46d5-8783-f5af43bdfb59.png)






## Usage

### Plots

Use these steps to recreate the above plots:

```bash
BRANCH=mrl-decoy-descr-tests

git clone --recursive https://github.com/mj-xmr/monero-mj.git
cd monero-mj
git pull origin $BRANCH
git checkout -b $BRANCH
make release-all 	# Build with tests, but don't run them
cd build/Linux/$BRANCH/release  # Linux or whatever host system
tests/unit_tests/unit_tests --gtest_filter=decoy.*  # Run the relevant tests only and generate the data
cd ..
```

```bash
git clone --recursive https://github.com/mj-xmr/monero-mrl-mj.git
cd monero-mrl-mj
decoy/python/mrl_decoy_plot.py
decoy/python/mrl_decoy_reimpl.py

```

### Statistical tests

In order to generate an abundence of test data, being able to perform statistical tests on them, 
just run the following script:

```bash
cd decoy/python
bash mrl-decoy-loop.sh
```

As a result of running this script, there are going to be sets of data generated in: `/tmp/monero/decoy`.
These data can be compared against each other via:

```bash
# Run Kolmogorov-Smirnov test:
./mrl_decoy_ks.py \
-d1 /tmp/monero/decoy/decoy-1/python/picks_raw_py_mul_length_100000.csv \
-d2 /tmp/monero/decoy/decoy-2/cpp/mrl_pick_mul_length_100000.csv

./mrl_decoy_ks.py \
-d1 /tmp/monero/decoy/decoy-1/python/picks_raw_py_mul_length_5.csv \
-d2 /tmp/monero/decoy/decoy-2/cpp/mrl_pick_mul_length_5.csv
```

... and so on. The number suffix of the data files is a multiple of the minimum length, at which the algorithm may start to deliver expected results.
