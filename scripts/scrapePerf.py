from datetime import datetime
from collections import defaultdict
import json
import math


offset_uptime = 0
time_stat_dict = defaultdict(lambda: dict())

linenum = 0
with open("perfstat.log", "r") as f:
    # time_idx = 0
    for line in f:
        if line.startswith("#"):
            linenum += 1
            continue

        tokens = line.split()
        
        # if linenum == 2:
        #     offset_uptime = int(tokens[0])

        # if linenum > 4 and len(tokens) > 1:
        if len(tokens) > 1:
            # time_idx = math.ceil(float(tokens[0]) * 5) / 5 + offset_uptime
            time_idx = round(float(tokens[0]), 1) + offset_uptime
            count = int(tokens[1].replace(",", ""))
            event = tokens[2]

            time_stat_dict[time_idx][event] = count

        linenum += 1

with open("perfstat.json", "w") as outfile:
    json.dump(dict(time_stat_dict), outfile)
