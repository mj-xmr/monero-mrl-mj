# Decoy

Documenting and experimenting on the Decoy Selection Algorithm.

## Strategy

- New unit tests shall be written, that cover the happy path and edge cases of the decoy algorithm
- The nevralgic parts of the system shall be first experimentally probed and the results shall be gathered
- An alternative Python (or R) implementation shall be prepared, since Python offers many statistical analysis and visualization tools. The correspondence between this and the original implementation shall be confirmed via the Kolmogorov-Smirnov test
- With the Python implementation at hand, a mathematical expression of the decoy algo shall be derived

## Results

TODO: use boxplot instead of scatter plot

![image](https://user-images.githubusercontent.com/63722585/165282001-b7ec412d-ff5b-4975-bbf4-d4f517fee47a.png)

## Unit tests

![image](https://user-images.githubusercontent.com/63722585/165281752-8073a130-f46d-450f-9de8-a06c96fb96f5.png)



## Usage

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
BRANCH_MRL=decoy

git clone --recursive https://github.com/mj-xmr/monero-mrl-mj.git
cd monero-mrl-mj
git pull origin $BRANCH_MRL
git checkout -b $BRANCH_MRL
decoy/python/mrl_decoy_plot.py

```

