#!/bin/bash
# echo 1 > /sys/kernel/debug/tracing/events/vmscan/mm_vmscan_node_reclaim_begin/enable
# echo 1 > /sys/kernel/debug/tracing/events/vmscan/mm_vmscan_wakeup_kswapd/enable
# echo 1 > /sys/kernel/debug/tracing/events/vmscan/mm_vmscan_kswapd_wake/enable

# echo 1 > /sys/kernel/debug/tracing/events/kmem/kmalloc/enable
# echo 1 > /sys/kernel/debug/tracing/events/kmem/mm_page_alloc/enable

# echo 1 > /sys/kernel/debug/tracing/events/syscalls/sys_enter_clone/enable
# echo 1 > /sys/kernel/debug/tracing/events/syscalls/sys_enter_brk/enable
# echo 1 > /sys/kernel/debug/tracing/events/syscalls/sys_enter_mmap/enable

# echo 1 > /sys/kernel/debug/tracing/events/oom/oom_score_adj_update/enable

# echo 1 > /sys/kernel/debug/tracing/events/huge_memory/mm_collapse_huge_page_swapin/enable

for i in {1..1000}; 
do
	#echo "start"
    	tail /dev/zero
	cut -f1 -d. /proc/uptime
	#echo "end"
	sleep $(($RANDOM % 60 + 1))
        :
done

# echo 0 > /sys/kernel/debug/tracing/events/vmscan/mm_vmscan_node_reclaim_begin/enable
# echo 0 > /sys/kernel/debug/tracing/events/vmscan/mm_vmscan_wakeup_kswapd/enable
# echo 0 > /sys/kernel/debug/tracing/events/vmscan/mm_vmscan_kswapd_wake/enable

# echo 0 > /sys/kernel/debug/tracing/events/kmem/kmalloc/enable
# echo 0 > /sys/kernel/debug/tracing/events/kmem/mm_page_alloc/enable

# echo 0 > /sys/kernel/debug/tracing/events/syscalls/sys_enter_clone/enable
# echo 0 > /sys/kernel/debug/tracing/events/syscalls/sys_enter_brk/enable
# echo 0 > /sys/kernel/debug/tracing/events/syscalls/sys_enter_mmap/enable

# echo 0 > /sys/kernel/debug/tracing/events/oom/oom_score_adj_update/enable

# echo 0 > /sys/kernel/debug/tracing/events/huge_memory/mm_collapse_huge_page_swapin/enable
