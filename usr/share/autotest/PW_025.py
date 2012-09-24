#!/usr/bin/python
#low battery level suspend test
import os
import sys
cmd="".join("/usr/share/autotest/power/power5_low_battery_action.sh  %s" % (sys.argv[1]))
os.system(cmd)
