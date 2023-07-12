from datetime import datetime
from collections import defaultdict
import json

def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

row_info = None

offset_h_time = None
offset_uptime = None

time_stat_dict = defaultdict(lambda: dict())

linenum = 0
prev_time_id = None
with open("sysstat.log", "r") as f:

    time_id = 0
    for line in f:
        tokens = line.split()

        if linenum == 0:
            offset_h_time = datetime.strptime(
                tokens[0] + " " + tokens[1], "%I:%M:%S %p")

        elif linenum == 1:
            offset_uptime = int(tokens[0])

        elif linenum >= 4 and len(tokens) > 1:
            if tokens[1] != "AM" and tokens[1] != "PM":
                time_id += 1
                continue

            if isint(tokens[2]) or isfloat(tokens[2]):
                # time_id = datetime.strptime(
                #     tokens[0] + " " + tokens[1], "%I:%M:%S %p")
                # time_id = offset_uptime + \
                #     int((time_id - offset_h_time).total_seconds())

                # if prev_time_id is None or len(time_stat_dict[prev_time_id].keys()) == 30:
                #     time_id = (time_id - 1 + 0.5) if (time_id - 1 +
                #                                   0.5) not in time_stat_dict.keys() else float(time_id)
                #     prev_time_id = time_id
                # else:
                #     time_id = prev_time_id

                data = dict(zip(row_info, list(map(float, tokens[2:]))))
                time_stat_dict[time_id].update(data)

            else:
                row_info = tokens[2:]

        linenum += 1

        # if linenum == 48:
        #     break

with open("sysstat.json", "w") as outfile:
    json.dump(dict(time_stat_dict), outfile)
