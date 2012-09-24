#!/usr/bin/python
#critical battery level suspend test
import os
import sys
cmd="".join("/usr/share/autotest/power/power6_critical_battery_action.sh %s" % (sys.argv[1]))
os.system(cmd)
