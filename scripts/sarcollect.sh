#!/bin/bash
date "+%r"
cut -f1 -d. /proc/uptime
echo ---
#sar -B -H -S -r 1
while :
do
    sar -B -H -S -r 0
    sleep 0.5
done

