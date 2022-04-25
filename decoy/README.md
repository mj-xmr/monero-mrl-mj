# Decoy

Documenting and experimenting on the Decoy Selection Algorithm.

## Results

![image](https://user-images.githubusercontent.com/63722585/165168523-9ed20d59-c406-491e-a10d-148076d1952a.png)


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

