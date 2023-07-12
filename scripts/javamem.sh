#!/bin/bash
while true; do
	echo "start"
        /usr/lib/jvm/java-8-openjdk-amd64/bin/java TriggerOOM
	echo "end"
	sleep $(($RANDOM % 30 + 1))
        :
done
