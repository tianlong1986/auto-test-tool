#!/usr/bin/python

"""
written by jackson at 12/08/31 - 12/09/05
Use to check the machine type in order to find the keyboard layout
And test the LM's voice or airplane mode

1:The keyboard configuration file is saved in the /tmp/.machine.conf. Make sure about it.
2:The keyboard layout is output to /tmp/.machine_type.log
3:The message will be saved in /tmp/.autotest_LM_Hotkey.log

"""

import os
import sys
import time
import thread

MESSAGE_UI_1 = " Watch the launch-manager's WIFI mode\n WIFI: 	OPEN 	, Airplane:	CLOSE \n Is this right?"
MESSAGE_UI_2 = " Watch the launch-manager's WIFI mode\n WIFI:	CLOSE 	, Airplane:	OPEN \n Is this right?"
MESSAGE_UI_3 = " Watch the launch-manager's WIFI mode\n BT:	OPEN 	, Airplane:	CLOSE \n Is this right?"
MESSAGE_UI_4 = " Watch the launch-manager's WIFI mode\n BT:	CLOSE	, Airplane:	OPEN \n Is this right?"
MESSAGE_UI_5 = " Watch the launch-manager's WIFI mode\n WIFI:	CLOSE	, BT:	CLOSE	, Airplane:	OPEN\n Is this right?"
MESSAGE_UI_6 = " Watch the launch-manager's WIFI mode\n WIFI:	OPEN	, BT:	CLOSE	, Airplane:	CLOSE\n Is this right?"
MESSAGE_UI_7 = " Watch the launch-manager's WIFI mode\n WIFI:	CLOSE	, BT:	OPEN	, Airplane:	CLOSE\n Is this right?"
MESSAGE_UI_8 = " Watch the launch-manager's WIFI mode\n WIFI:	OPEN	, BT:	OPEN	, Airplane:	CLOSE\n Is this right?"
MESSAGE_UI_9 = " Watch the launch-manager's VOICE mode\n The sound is up continue\n Is this right?"
MESSAGE_UI_10 = " Watch the launch-manager's VOICE mode\n The sound is down continue\n Is this right?"
MESSAGE_UI_11 = " Watch the launch-manager's VOICE mode\n The sound is zero , the sound icon become mute\n Is this right?"
MESSAGE_UI_12 = " Watch the launch-manager's VOICE mode\n The sound will up continue "
MESSAGE_UI_13 = " Watch the launch-manager's VOICE mode\n The sound will down continue "
MESSAGE_UI_14 = " Please press the icon 'Record sound' \n\n And keep on beating desktop for 30S\n\n Then press the 'icon Stop' sound\n Click 'ok' to start"
MESSAGE_UI_15 = " Watch the launch-manager's VOICE mode\n The MIC icon is mute\n Is this right?"
MESSAGE_UI_16 = " Please press the 'icon Play' sound... \n You will find:\n\n 1.Sound became big from mute in the beginning\n\n 2.and then it became small after 15 s\n\n Is this right?"

GET_DEVICE_WIRELESS_CMD = "sh /usr/lib/hotkey/others/script/get_wireless_dev.sh"
GET_DEVICE_3G_CMD = "sh /usr/lib/hotkey/others/script/get_3g_dev.sh"
GET_DEVICE_BLUETOOTH_CMD = "sh /usr/lib/hotkey/others/script/get_bt_dev.sh"
GET_STATUS_WIRELESS_CMD = "sh /usr/lib/hotkey/others/script/get_wireless_status.sh"
GET_STATUS_3G_CMD = "sh /usr/lib/hotkey/others/script/get_3g_status.sh"
GET_STATUS_BLUETOOTH_CMD = "sh /usr/lib/hotkey/others/script/get_bt_status.sh"
SET_WIRELESS_ON_CMD = "sudo sh /usr/lib/hotkey/others/script/set_wireless_on.sh"
SET_3G_ON_CMD = "sh /usr/lib/hotkey/others/script/set_3g_on.sh"
SET_BLUETOOTH_ON_CMD = "sh /usr/lib/hotkey/others/script/set_bt_on.sh"
SET_WIRELESS_OFF_CMD = "sudo sh /usr/lib/hotkey/others/script/set_wireless_off.sh"
SET_3G_OFF_CMD = "sh /usr/lib/hotkey/others/script/set_3g_off.sh"
SET_BLUETOOTH_OFF_CMD = "sh /usr/lib/hotkey/others/script/set_bt_off.sh"
SET_AIRPLANE_OFF_CMD = "sudo sh /usr/lib/hotkey/others/script/airplane_off.sh"
SET_AIRPLANE_ON_CMD = "sudo sh /usr/lib/hotkey/others/script/airplane_on.sh"
#VIDEO_PATH_CMD = "totem ~/big_buck_bunny_480p.ogv &"
VIDEO_PATH_CMD = "totem /tmp/Sample.ogg &"
FIND_TYPE_CMD = "sudo dmidecode -s system-version | grep "
CLOSE_VIDEO_CMD = "sudo killall totem"
MIC_PATH_CMD = "gnome-sound-recorder &"
CLOSE_MIC_CMD = "sudo killall gnome-sound-recorder"

NOTHING_IN_FILE_MESSAGES = " : [ERROR] There is nothing in /tmp/.machine.conf"
CAN_NOT_FIND_TYPE_MESSAGES = " :[ERROR]	There is no the type of the machine in the /tmp/.machine.conf"
WIRELESS_EXISTS = "rfkill list | grep -i wireless > /tmp/udevadm_wireless"
BLUETOOTH_EXISTS = "rfkill list | grep -i bluetooth > /tmp/udevadm_bluetooth"
UI_TEST = "zenity --question --text \""
UI_TEST_1 = "zenity --info --text \""
UI_TEXT = "\""

TEST_1_TITLE = "Airplane"
TEST_2_TITLE = "Voice"
MACHINE_CONFIG = "/tmp/.machine.conf"
NEXT_SWITCH_FLAG_FILE = "/tmp/.autotest_LM_Hotkey.log"
LM_TEST_MESSAGE_FILE = "/tmp/.autotest_LM_Hotkey.log"
MACHINE_TYPE_FILE = "/tmp/.machine_type.log"
BLUETOOTH_EXISTS_FILE = "/tmp/udevadm_bluetooth"
WIRELESS_EXISTS_FILE = "/tmp/udevadm_wireless"

LOCAL_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ECHO_CMD_1 = "echo \"%s %s \" >> %s"
ECHO_CMD_2 = "echo \"%s\" > %s"
TEST_BEGIN = ": [BEGIN] Test %s begin"
TEST_END = ": [END] Test %s end\n"
SET_VOLUME_SLIDER = "dbus-send --session --print-reply --dest=com.linpus.launchManager /com/linpus/volumeAdjust com.linpus.volumeAdjust.volumeadjust string:%d"
SET_MIC_SLIDER = "dbus-send --session --print-reply --dest=com.linpus.launchManager /com/linpus/volumeAdjust com.linpus.volumeAdjust.micvolumeadjust string:%d"
SAVED_MESSAGE = "echo "
SAVED_MESSAGE_1 = " >> ~/.cache/autotest.txt"

NUM_OF_RIGHT = 256
Flag_NUM_ZREO = "0\n"
Flag_NUM_MACHINETYPE = "1\n"
Flag_NUM_AIRPLANE = "2\n"
Flag_NUM_VOICE = "3\n"
Flag_NUM_EXIT = "4\n"
#ID_AIR = "LM_128"
#ID_VOICE = "LM_129"
WIRELESS_DEV = 0
BLUETOOTH_DEV = 1
AIRPLANE_DEV = 2
DEV_ON = 1
DEV_OFF = 2
flag_switch = 0
Flag_T_F = 0
		
#message: 	"xxxxxxx" the message you want to saved
#file:		"xxxxxxx" the message will saved in xxxxxxx
#test_message:	"" others	"XXXXXX". test name
#flag:  	0. test begin  1. test end  
def MESSAGE_RECORD(message, file, test_message, flag):

	if(test_message != ""):

		if flag == 0:

			message = TEST_BEGIN % test_message
		else:

			message = TEST_END % test_message

	Local_time = time.strftime(LOCAL_TIME_FORMAT, time.localtime(time.time()))
        CMD = ECHO_CMD_1 % (Local_time, message, file)
        os.system(CMD)

#num:		the steps in test
#message:	show on UI
#num_now:	the num of test
#num_next:	add for something maybe need
def WHETHER_NEXT(num, message, num_now, num_next):

        f_Flag_NUM = open(NEXT_SWITCH_FLAG_FILE, "r")
        Flag_NUM = f_Flag_NUM.readline()
	
	if message == "":

		while num != Flag_NUM:

        		f_Flag_NUM = open(NEXT_SWITCH_FLAG_FILE, "r")
        		Flag_NUM = f_Flag_NUM.readline()
        		f_Flag_NUM.close()
        		time.sleep(1)	
	else:

        	CMD = UI_TEST + message + UI_TEXT

        	if os.system(CMD) < NUM_OF_RIGHT:

                	MESSAGE_RECORD(": [PASSED] TEST: " + num_now + " is PASSED", LM_TEST_MESSAGE_FILE, "", 0)
#			os.system(SAVED_MESSAGE + "\"[" + num_now + "]" + " = T\"" + SAVED_MESSAGE_1)
#			os.system(SAVED_MESSAGE + "\"[" + num_now + "_comment]" + " = \"" + SAVED_MESSAGE_1)
			return 0
        	else:

                	MESSAGE_RECORD(": [FAILD] TEST: " + num_now + " is FAILD", LM_TEST_MESSAGE_FILE, "", 0)
               	 	MESSAGE_RECORD(": [FAILD MESSAGES]\n" + message, LM_TEST_MESSAGE_FILE, "", 0)
			#Flag_T_F = 1
#			os.system(SAVED_MESSAGE + "\"[" + num_now + "]" + " = F\"" + SAVED_MESSAGE_1)
#			os.system(SAVED_MESSAGE + "\"[" + num_now + "_comment]" + " = " + message + "\"" + SAVED_MESSAGE_1)
			return 1

def SWITCH_NEXT():

	f_Flag_NUM = open(NEXT_SWITCH_FLAG_FILE, "r")
        Flag_NUM = f_Flag_NUM.readline()

	while "0\n" == Flag_NUM:

        	f_Flag_NUM = open(NEXT_SWITCH_FLAG_FILE, "r")
        	Flag_NUM = f_Flag_NUM.readline()
        	f_Flag_NUM.close()
        	time.sleep(1)

	os.system("echo 0 > %s" % NEXT_SWITCH_FLAG_FILE)

	return Flag_NUM

#dev:		device type
#status:	now status
def CHANGE_DEV(dev, status):

	if dev == WIRELESS_DEV:

		if status == DEV_ON:

			os.system(SET_WIRELESS_ON_CMD)

		elif status == DEV_OFF:

			os.system(SET_WIRELESS_OFF_CMD)

	elif dev == BLUETOOTH_DEV:

		if status == DEV_ON:

			os.system(SET_BLUETOOTH_ON_CMD)

		elif status == DEV_OFF:

			os.system(SET_BLUETOOTH_OFF_CMD)

	elif dev == AIRPLANE_DEV:

		if status == DEV_ON:

			os.system(SET_AIRPLANE_ON_CMD)

		if status == DEV_OFF:

			os.system(SET_AIRPLANE_OFF_CMD)

def SET_VOLUME():

	volume = 1
	flag_icount = 0
	flag_up = 0
	flag = 0
	flag_1 = 0
	temp = 0
	temp_1 = 0

	CMD = UI_TEST_1 + MESSAGE_UI_12 + UI_TEXT
	os.system(CMD)

	while flag_icount < 200:

		if 0 < volume < 100 and flag_up == 0:

			os.system(SET_VOLUME_SLIDER % volume)
			volume += 1
			time.sleep(0.1)
			
		if 0 < volume < 100 and flag_up == 1:

			os.system(SET_VOLUME_SLIDER % volume)
			time.sleep(0.1)
			volume -= 1
			if volume == 1:

				temp_1 = WHETHER_NEXT("", MESSAGE_UI_10, "LM-VOICE-2", "")
				flag_1 = 1
				temp += temp_1
		if volume == 0:

			os.system(SET_VOLUME_SLIDER % volume)
			time.sleep(2)
			flag_up = 2
			volume = 1
			temp_1 = WHETHER_NEXT("", MESSAGE_UI_11, "LM-VOICE-3", "")
			temp += temp_1

		if volume == 100:

			os.system(SET_VOLUME_SLIDER % volume)
			time.sleep(2)
			volume = 99
			flag_up = 1
			temp_1 = WHETHER_NEXT("", MESSAGE_UI_9, "LM-VOICE-1", "")
			temp += temp_1

			CMD = UI_TEST_1 + MESSAGE_UI_13 + UI_TEXT
			os.system(CMD)
		
		flag_icount += 1

	return temp

def SET_MIC():

	temp = 0
	temp_1 = 0

	os.system(SET_VOLUME_SLIDER % 30) 
	
	CMD = UI_TEST_1 + MESSAGE_UI_14 + UI_TEXT
	os.system(CMD)

	flag = 0
	voice = 0

	while flag == 0:

		os.system(SET_MIC_SLIDER % voice)

		voice += 1	
		time.sleep(0.15)
		
		if voice == 100:
			flag = 1

	while flag == 1:

		os.system(SET_MIC_SLIDER % voice)

		voice -= 1
		time.sleep(0.15)
		
		if voice == 0:
			flag = 0

	temp_1 = WHETHER_NEXT("", MESSAGE_UI_16, "LM-VOICE-4", "")
	temp += temp_1

	os.system(SET_MIC_SLIDER % 0)

	temp_1 = WHETHER_NEXT("", MESSAGE_UI_15, "LM-VOICE-5", "")
	temp += temp_1

	return temp

def FIND_MACHINE_TYPE():

	f_machinetype = open(MACHINE_CONFIG, "r+")

	machineTypes = f_machinetype.readlines()

	f_machinetype.close()

	#if the /tmp/.machine.conf is none
	if len(machineTypes) == 0:

		MESSAGE_RECORD(NOTHING_IN_FILE_MESSAGES, LM_TEST_MESSAGE_FILE, "", 0)
		sys.exit(0)

	flag = 0
	iCound = 0

	while flag == 0:

		if len(machineTypes) >= iCound + 1:

			name_Machine_CMD = FIND_TYPE_CMD + machineTypes[iCound]
	
			#if os.system return right , the return must bigger than 0x100	
			if os.system(name_Machine_CMD) >= NUM_OF_RIGHT:

				iCound = iCound + 2
			elif os.system(name_Machine_CMD) < NUM_OF_RIGHT:

				flag = 1
				name_Machine = machineTypes[iCound]
		else:
			#can not find the machine type
			MESSAGE_RECORD(CAN_NOT_FIND_TYPE_MESSAGES, LM_TEST_MESSAGE_FILE, "", 0)
			sys.exit(0)
	

	NUM = machineTypes.index(name_Machine)
	type_Machine = machineTypes[NUM + 1]

	result = ECHO_CMD_2 % (type_Machine, MACHINE_TYPE_FILE)

	os.system(result)

def SAVE_RESULT(id, Flag_T_F):
	
	if Flag_T_F == 0:

		os.system(SAVED_MESSAGE + "\"[item_" + id + "] = P\"" + SAVED_MESSAGE_1)
		os.system(SAVED_MESSAGE + "\"[item_" + id + "_comment] = \"" + SAVED_MESSAGE_1)
	else:

		os.system(SAVED_MESSAGE + "\"[item_" + id + "] = F\"" + SAVED_MESSAGE_1)
		os.system(SAVED_MESSAGE + "\"[item_" + id + "_comment] = read the /tmp/.autotest_LM_Hotkey.log" + "\"" + SAVED_MESSAGE_1)

def TEST_AIRPLANE(ID_AIR):

	Flag_T_F = 0
	temp = 0

	MESSAGE_RECORD("", LM_TEST_MESSAGE_FILE, TEST_1_TITLE, 0)

	os.system(WIRELESS_EXISTS)
	os.system(BLUETOOTH_EXISTS)

	f_wireless =  open(WIRELESS_EXISTS_FILE, "r")
	f_bluetooth = open(BLUETOOTH_EXISTS_FILE, "r")

	flag_wireless_exists = 0
	flag_bluetooth_exists = 0

	if len(f_wireless.readlines()) != 0:
		flag_wireless_exists = 1
	if len(f_bluetooth.readlines()) != 0:
		flag_bluetooth_exists = 1

	if flag_wireless_exists == 1 and flag_bluetooth_exists == 1:

		CHANGE_DEV(WIRELESS_DEV, DEV_ON)
		CHANGE_DEV(BLUETOOTH_DEV, DEV_ON)
		temp = WHETHER_NEXT("", MESSAGE_UI_8, "LM-AIR-1", "")
		Flag_T_F += temp

		CHANGE_DEV(WIRELESS_DEV, DEV_OFF)
		temp = WHETHER_NEXT("", MESSAGE_UI_7, "LM-AIR-2", "")
		Flag_T_F += temp

		CHANGE_DEV(WIRELESS_DEV, DEV_ON)
		CHANGE_DEV(BLUETOOTH_DEV, DEV_OFF)
		temp = WHETHER_NEXT("", MESSAGE_UI_6, "LM-AIR-3", "")
		Flag_T_F += temp

		CHANGE_DEV(WIRELESS_DEV, DEV_OFF)
		temp = WHETHER_NEXT("", MESSAGE_UI_5, "LM-AIR-4", "")
		Flag_T_F += temp
	
		CHANGE_DEV(AIRPLANE_DEV, DEV_OFF)
		temp = WHETHER_NEXT("", MESSAGE_UI_6, "LM-AIR-5", "")
		Flag_T_F += temp
	
		CHANGE_DEV(AIRPLANE_DEV, DEV_ON)
       	 	temp = WHETHER_NEXT("", MESSAGE_UI_5, "LM-AIR-6", "")
		Flag_T_F += temp

		CHANGE_DEV(WIRELESS_DEV, DEV_ON)
        	CHANGE_DEV(BLUETOOTH_DEV, DEV_ON)
        	temp = WHETHER_NEXT("", MESSAGE_UI_8, "LM-AIR-7", "")
		Flag_T_F += temp

		CHANGE_DEV(AIRPLANE_DEV, DEV_ON)
       		temp = WHETHER_NEXT("", MESSAGE_UI_5, "LM-AIR-8", "")
		Flag_T_F += temp

        	CHANGE_DEV(AIRPLANE_DEV, DEV_OFF)
        	temp = WHETHER_NEXT("", MESSAGE_UI_8, "LM-AIR-9", "")
		Flag_T_F += temp

	elif  flag_wireless_exists == 0 and flag_bluetooth_exists == 1:

		CHANGE_DEV(BLUETOOTH_DEV, DEV_ON)
        	temp = WHETHER_NEXT("", MESSAGE_UI_3, "LM-AIR-10", "")	
		Flag_T_F += temp

		CHANGE_DEV(BLUETOOTH_DEV, DEV_OFF)
        	temp = WHETHER_NEXT("", MESSAGE_UI_4, "LM-AIR-11", "")
		Flag_T_F += temp

		CHANGE_DEV(AIRPLANE_DEV, DEV_OFF)
        	temp = WHETHER_NEXT("", MESSAGE_UI_3, "LM-AIR-12", "")
		Flag_T_F += temp

		CHANGE_DEV(AIRPLANE_DEV, DEV_ON)
		temp = WHETHER_NEXT("", MESSAGE_UI_4, "LM-AIR-13", "")
		Flag_T_F += temp

	elif  flag_wireless_exists == 1 and flag_bluetooth_exists == 0:

		CHANGE_DEV(WIRELESS_DEV, DEV_ON)
        	temp = WHETHER_NEXT("", MESSAGE_UI_1, "LM-AIR-14", "")	
		Flag_T_F += temp

		CHANGE_DEV(WIRELESS_DEV, DEV_OFF)
        	temp = WHETHER_NEXT("", MESSAGE_UI_2, "LM-AIR-15", "")
		Flag_T_F += temp

		CHANGE_DEV(AIRPLANE_DEV, DEV_OFF)
        	temp = WHETHER_NEXT("", MESSAGE_UI_1, "LM-AIR-16", "")
		Flag_T_F += temp

		CHANGE_DEV(AIRPLANE_DEV, DEV_ON)
		temp = WHETHER_NEXT("", MESSAGE_UI_2, "LM-AIR-17", "")
		Flag_T_F += temp
	
	SAVE_RESULT(ID_AIR, Flag_T_F)
		
	MESSAGE_RECORD("", LM_TEST_MESSAGE_FILE, TEST_1_TITLE, 1)

def TEST_VOICE(ID_VOICE):

	Flag_T_F = 0
	temp = 0

	MESSAGE_RECORD("", LM_TEST_MESSAGE_FILE, TEST_2_TITLE, 0)

	os.system(VIDEO_PATH_CMD)
	temp = SET_VOLUME()
	os.system(CLOSE_VIDEO_CMD)
	Flag_T_F += temp	

	os.system(MIC_PATH_CMD)
	temp = SET_MIC()
	os.system(CLOSE_MIC_CMD)
	Flag_T_F += temp

	SAVE_RESULT(ID_VOICE, Flag_T_F)

	MESSAGE_RECORD("", LM_TEST_MESSAGE_FILE, TEST_2_TITLE, 1)

def init():

	f_Flag_NUM = open(NEXT_SWITCH_FLAG_FILE, "w+")
	f_Flag_NUM.close()
	flag_switch = 0
#def func():
#
#	os.system(VIDEO_PATH_CMD)
#	
#	print 1
#	
#	f_Flag_NUM = open(NEXT_SWITCH_FLAG_FILE, "r")
#	Flag_NUM = f_Flag_NUM.readline()
#	f_Flag_NUM.close()
#
#   	while "2\n" != Flag_NUM:
#    		f_Flag_NUM = open(NEXT_SWITCH_FLAG_FILE, "r")
#		Flag_NUM = f_Flag_NUM.readline()
#		f_Flag_NUM.close()
#		time.sleep(1)
#
#	thread.exit()
			

#def SAVE_RESAVE_RESULTSSULTS(message, num, num_next):
#	CMD = UI_TEST + message + UI_TEXT
#	if os.system(CMD) < NUM_OF_RIGHT:
#		MESSAGE_RECORD(": [PASSED]TEST:" + num + " is PASSED", LM_TEST_MESSAGE_FILE, "", 0)
#		os.system("echo \"" + num_next + "\" >>" + LM_TEST_MESSAGE_FILE)
#	else:
#		MESSAGE_RECORD(": [FAILD]TEST:" + num + " is FAILD", LM_TEST_MESSAGE_FILE, "", 0)
#		MESSAGE_RECORD(": [MESSAGES]\n" + message, LM_TEST_MESSAGE_FILE, "", 0)
#		os.system("echo \"" + num_next + "\" >>" + LM_TEST_MESSAGE_FILE):
