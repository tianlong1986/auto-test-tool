#!/bin/sh

# audio play:
rsFILE="/home/`whoami`/.cache/autotest.txt"
COUNT=100
cd /home/user/
if [ -e big-buck-bunny.ogv ]; then 
	totem big-buck-bunny.ogv &--volume-up
	for ((i=0 ; i<=$COUNT ; i++))
	do
		dbus-send --session --print-reply --dest=com.linpus.launchManager /com/linpus/volumeAdjust com.linpus.volumeAdjust.volumeadjust string:$i
		sleep 0.1
	done
	for ((j=$COUNT ; j>=0 ; j--)) 
	do
		dbus-send --session --print-reply --dest=com.linpus.launchManager /com/linpus/volumeAdjust com.linpus.volumeAdjust.volumeadjust string:$j
		sleep 0.1
	done

	dbus-send --session --print-reply --dest=com.linpus.launchManager /com/linpus/volumeAdjust com.linpus.volumeAdjust.volumeadjust string:25

	OK_1=`echo $?`
	if [ "X$OK_1" = "X0" ]; then
	        zenity --question --text="请检查：声音播放正常，音量调节正常，视频显示正常，没有花屏。" --ok-label="Yes,it's OK" --cancel-label="No.it's NOT ok"
	        OK_2=`echo $?`
	        if [ "X$OK_2" = "X1" ];then
	        COMMENT1=`zenity --text-info --editable --title='the problem is:'`
	        fi
	else
        exit 1
fi

#comment:
if [ "X$COMMENT1" = "X" ]; then
        echo "item_$1 = P" >> $rsFILE
        echo "item_$1_comment = Pass" >> $rsFILE
else
        echo "item_$1 = F" >> $rsFILE
        echo "item_$1_comment = $COMMENT1 ; $COMMENT2" >> $rsFILE
fi


else
	echo "Cannot find video file."
fi
