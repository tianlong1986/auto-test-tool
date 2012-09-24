#!/bin/sh
#Set the bluetooth device's name
rsFILE=/home/`whoami`/.cache/autotest.txt
sudo hciconfig hci0 name auto_bt

hciconfig hci0 get name |grep auto_bt

if [ $? = 0 ];then
	set_name="P"
	comment=""
else
	set_name="F"
	comment="Set the bluetooth'name to auto_bt fail"
fi
echo `pwd`
echo $rsFILE
echo "item_$1=$set_name" >> $rsFILE
echo "item_$1_comment=$comment" >> $rsFILE

