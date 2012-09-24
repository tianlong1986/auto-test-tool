#!/bin/sh
# camera: AC to DC
rsFILE="/home/`whoami`/.cache/autotest.txt"
cheese &
sleep 1.5
zenity --question --text="now please remove the AC power \nthen press 'Next'" --ok-label="Next" --cancel-label="Cancel" --title="AC to DC"

OK_1=`echo $?`
if [ "X$OK_1" = "X0" ];then
	zenity --question --text="请检查画面清晰、没有卡顿延迟" --ok-label="Yes,it's OK" --cancel-label="No.it's NOT ok"
	OK_2=`echo $?`
	if [ "X$OK_2" = "X1" ];then
	COMMENT1=`zenity --text-info --editable --title='the problem is:'`
	fi
else
	exit 1
fi

sleep 1

#camera: DC to AC

zenity --question --text="now please plug in the AC power \nthen press 'Next'" --ok-label="Next" --cancel-label="Cancel" --title="DC to AC"
OK_3=`echo $?`
if [ "X$OK_3" = "X0" ];then
        zenity --question --text="请检查画面清晰、没有卡顿延迟" --ok-label="Yes,it's OK" --cancel-label="No.it's NOT ok"
	OK_4=`echo $?`
	if [ "X$OK_4" = "X1" ];then
        COMMENT2=`zenity --text-info --editable --title='the problem is:'`
        fi
else
	exit 1
fi

#comment:
if [ "X$COMMENT1" = "X" ] || [ "X$COMMENT2" = "X" ]; then
	echo "item_$1 = P" >> $rsFILE
	echo "item_$1_comment = Pass" >> $rsFILE
else
	echo "item_$1 = F" >> $rsFILE
	echo "item_$1_comment = $COMMENT1 ; $COMMENT2" >> $rsFILE
fi

zenity --info --text="This case Finish." --title="case finish"
