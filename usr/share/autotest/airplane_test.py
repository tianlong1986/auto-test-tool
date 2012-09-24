#!/usr/bin/python
"""
written by jackson at 12/08/31 - 12/09/04
Use to check the machine type in order to find the keyboard layout
And test the LM's voice or airplane mode

1:The keyboard configuration file is saved in the /tmp/.machine.conf. Make sure about it.
2:The keyboard layout is output to /tmp/.machine_type.log
3:The message will be saved in /tmp/.autotest_LM_Hotkey.log

"""
import sys
sys.path.append("~")
from JKS_main import *


TEST_AIRPLANE(sys.argv[1])


