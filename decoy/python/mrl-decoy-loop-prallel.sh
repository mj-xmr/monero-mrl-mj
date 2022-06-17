#!/bin/bash -e

START=10
END=40

FILE_STATUS="/tmp/mrl-status.txt"

for num in $(seq $START $END); do
	echo "Num $num of $END 	C++" > $FILE_STATUS
	cat $FILE_STATUS
	$HOME/bin/tts.sh $FILE_STATUS || true
	date
	rm /tmp/*.csv || true
	DIR=/tmp/monero/decoy/decoy-$num
	mkdir -p $DIR/cpp
	mkdir -p $DIR/python
	/tmp/monero/build-monero-icecc/tests/unit_tests/unit_tests
	mv /tmp/*.csv $DIR/cpp/
	echo "Num $num of $END 	Python" > $FILE_STATUS
	cat $FILE_STATUS
	$HOME/bin/tts.sh $FILE_STATUS || true
	python3 mrl_decoy_reimpl_parallel.py
	mv /tmp/*.csv $DIR/python/
done

