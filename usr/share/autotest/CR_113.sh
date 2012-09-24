#!/bin/sh

# basic function
rsFILE="/home/`whoami`/.cache/autotest.txt"
zenity --warning --text="将打开webcam，请注意打开时是否有蓝影"
OK_1=`echo $?`
if [ "X$OK_1" = "X0" ]; then
	cheese &
	sleep 2
	zenity --question --text="请检查蓝影、画面清晰、没有卡顿延迟" --ok-label="Yes,it's OK" --cancel-label="No.it's NOT ok"
	OK_2=`echo $?`
	if [ "X$OK_2" = "X0" ];then 
		echo "item_$1 = P" >> $rsFILE
		echo "item_$1_comment = 没有蓝影、画面清晰、没有卡顿延迟" >> $rsFILE
	elif [ "X$OK_2" = "X1" ]; then
		COMMENT=`zenity --text-info --editable`
		echo "item_$1 = F" >> rsFILE
		echo "item_$1_comment = $COMMENT" >> rsFILE
	fi
else exit 1
fi

zenity --info --text="Please press 'Take a Photo' button \n\nThen press 'OK'" --title="cheese"
gthumb ~/Pictures/Webcam/`ls ~/Pictures/Webcam/ | sort -d | tail -1` &
OK_3=`echo $?`
sleep 2
if [ "X$OK_3" = "X0" ]; then
	zenity --question --text="Picture is fine?"
	OK_4=`echo $?`
	if [ "X$OK_4" = "X0" ];then
		echo "item_$1 = P" >> $rsFILE
		echo "item_$1_comment = basic function works well" >> $rsFILE
	elif [ "X$OK_4" = "X1" ];then
		COMMENT=`zenity --text-info --editable`
		echo "item_$1 = F" >> $rsFILE
		echo "item_$1_comment = $COMMENT" >> $rsFILE
	fi
fi

zenity --info --text="This case Finish." --title="case finish"






