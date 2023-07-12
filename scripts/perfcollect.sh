#!/bin/bash
date "+%r"
cut -f1 -d. /proc/uptime
echo ---
perf stat -e syscalls:sys_enter_brk -e kmem:kmalloc -e kmem:mm_page_alloc -e syscalls:sys_enter_mmap -a -I 500 -o perfstat.log

