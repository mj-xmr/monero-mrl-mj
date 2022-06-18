# Decoy

Documenting and experimenting on the Decoy Selection Algorithm.

## Strategy

- New unit tests shall be written, that cover the happy path and edge cases of the decoy algorithm
- The nevralgic parts of the system shall be first experimentally probed and the results shall be gathered
- An alternative Python implementation shall be prepared, since Python offers many statistical analysis and visualization tools. The correspondence between this and the original implementation shall be confirmed via the Kolmogorov-Smirnov test
- Based on the Python implementation, and R implementation shall be created and its results are confirmed via the same statistical tests
- With the R implementation at hand, a mathematical expression of the decoy algo shall be derived

## Results

Except for the last point, namely the mathematical expression, the research project already delivers satisfying results.

## Visualization

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
```

... and so on.


