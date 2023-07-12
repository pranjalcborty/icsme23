#!/bin/bash
jdk="/usr/lib/jvm/graalvm-ce-java17-22.3.0"
jar="/home/pranjal/IdeaProjects/RxJava/build/libs/rxjava-3.0.0-SNAPSHOT-jmh.jar"

nohup "${jdk}/bin/java" -XX:NativeMemoryTracking=summary -jar "${jar}" -wi 10 -i 10 -f 1 "RxVsStreamPerf.rangeObservableFlatMapJust" &
export PID=$!
echo "${PID}"

counter=0
while :
do
	"${jdk}/bin/jcmd" ${PID} VM.native_memory > jvmData/"${counter}".log
	counter=$(expr $counter + 1)
	sleep 0.2
done
