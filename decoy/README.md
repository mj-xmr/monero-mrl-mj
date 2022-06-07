# Decoy

Documenting and experimenting on the Decoy Selection Algorithm.

## Strategy

- New unit tests shall be written, that cover the happy path and edge cases of the decoy algorithm
- The nevralgic parts of the system shall be first experimentally probed and the results shall be gathered
- An alternative Python (or R) implementation shall be prepared, since Python offers many statistical analysis and visualization tools. The correspondence between this and the original implementation shall be confirmed via the Kolmogorov-Smirnov test
- With the Python implementation at hand, a mathematical expression of the decoy algo shall be derived

## Results
### Gamma pickers
Comparison of the final Gamma Picker's result. The differences may result at least from the different random samplers chosen in both implementations.

![cpp](https://user-images.githubusercontent.com/63722585/169068204-8e82eb8f-4151-48a9-85d4-c554cc231839.png)

![py](https://user-images.githubusercontent.com/63722585/169068222-50321cd3-2919-418a-87e6-5e97c9e4eb07.png)



### Gamma distributions
The point of this comparison is to make sure, that the parameters of the distribution aren't misinterpreted across the two APIs.

![image](https://user-images.githubusercontent.com/63722585/167909725-0afb8d37-8f95-4fdb-9c0f-4eaa62a49a23.png)

![gamma](https://user-images.githubusercontent.com/63722585/169069214-6f6bdebc-5daa-49d1-af01-bc3b3f37f9b9.png)



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

git clone --recursive https://github.com/mj-xmr/monero-mrl-mj.git
cd monero-mrl-mj
decoy/python/mrl_decoy_plot.py
decoy/python/mrl_decoy_reimpl.py

```

