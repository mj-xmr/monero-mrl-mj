#!/bin/bash

START=1
END=10
for num in $(seq $START $END); do
	echo "Num $num of $END 	C++"
	date
	rm /tmp/*.csv
	DIR=/tmp/monero/decoy/decoy-$num
	mkdir -p $DIR/cpp
	mkdir -p $DIR/python
	/tmp/monero/build-monero-icecc/tests/unit_tests/unit_tests
	mv /tmp/*.csv $DIR/cpp/
	echo "Num $num of $END 	Python"
	python3 mrl_decoy_reimpl.py
	mv /tmp/*.csv $DIR/python/
done

