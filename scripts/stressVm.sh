#!/bin/bash
while :
do
	vmCount=$(($RANDOM % 15 + 1))
	vmBytes=$(($RANDOM % 2048 + 256))
	timeOut=$(($RANDOM % 10 + 2))
	
	echo "stress --vm ${vmCount} --vm-bytes ${vmBytes}M --timeout ${timeOut}s"
	stress --vm "${vmCount}" --vm-bytes "${vmBytes}M" --timeout "${timeOut}s"

	sleep $(($RANDOM % 15 + 1))
done
