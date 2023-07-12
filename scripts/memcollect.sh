#!/bin/bash
echo -e "used,free,buffers,cached,swap"
while true; do
	awk ' \
    		/^MemTotal:/    {total=$2}
    		/^MemFree:/     {free=$2}
    		/^Buffers:/     {buff=$2}
    		/^Cached:/      {cached=$2}
    		/^SwapTotal:/   {swaptotal=$2}
    		/^SwapFree:/    {swapfree=$2}
    		END {
        		used=total-(free+buff+cached)
        		swap=swaptotal-swapfree
        		print used "," free "," buff "," cached "," swap
    		}' /proc/meminfo
	sleep 0.5
	:
done
