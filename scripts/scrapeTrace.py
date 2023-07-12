from collections import defaultdict
from matplotlib import pyplot as plt
import re
import json
import time


timefind = r".+?[\s]([0-9]+[.][0-9]+)[:][\s](.+?)[:(\s)].+"

time_call_dict = defaultdict(lambda: defaultdict(lambda: 0))
count = 1
error = 0

with open("trace.log", "r") as log:
    for line in log:
        print(str(count) + " - " + str(error), end="\r")
        res = re.search(timefind, line)

        try:
            res = res.groups()
            time_call_dict[int(float(res[0]))][res[1]] += 1
        except:
            print(line)
            error += 1
        
        count += 1

suffix = int(time.time())
with open("trace.json", "w") as outfile:
    json.dump(dict(time_call_dict), outfile)