#!/bin/bash
listOfPdfs=("big-10.pdf" "big-15.pdf" "big-20.pdf" "big-25.pdf" "big-30.pdf")
listSize=${#listOfPdfs[@]}

#echo "${listOfPdfs[$(($RANDOM % $listSize))]}"

#while :
#do
        pdfName=${listOfPdfs[$(($RANDOM % $listSize))]}
        
        echo "~/Downloads/firefox/firefox -new-tab file:///home/pranjal/Downloads/${pdfName} -headless"
        nohup firefox -new-tab file:///home/pranjal/Downloads/${pdfName} -headless &
	export PID=$!

        sleep $(($RANDOM % 15 + 15))
	kill -9 "$PID"
#done
