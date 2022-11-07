#!/bin/bash

start=mysterious-delivery.tcc.
domain=$start

while true; do
	read domain keys <<< $(dig +short +tcp +retry=10 NSEC @ns1.mysterious-delivery.thecatch.cz @ns2.mysterious-delivery.thecatch.cz "$domain")
	echo $domain $keys
	if [[ "$keys" == *TXT* ]]; then
		echo -n "   TXT: "
		dig +short +tcp +retry=10 TXT @ns1.mysterious-delivery.thecatch.cz @ns2.mysterious-delivery.thecatch.cz "$domain" 2>/dev/null
	fi

	if [ "$domain" = "$start" ]; then break; fi
done
