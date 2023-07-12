#!/bin/bash
jdk="/usr/lib/jvm/graalvm-ce-java17-22.3.0"
jar="/home/pranjal/IdeaProjects/RxJava/build/libs/rxjava-3.0.0-SNAPSHOT-jmh.jar"

nohup perf stat -e syscalls:sys_enter_brk -e kmem:kmalloc -e kmem:mm_page_alloc -e syscalls:sys_enter_mmap -a -I 200 -o perfstat.log &
export PID=$!

"${jdk}/bin/java" -Djmh.ignoreLock=true -XX:NativeMemoryTracking=summary -jar "${jar}" -wi 5 -i 5 -f 1 "RxVsStreamPerf.rangeObservableFlatMapJust"

kill -9 "${PID}"
