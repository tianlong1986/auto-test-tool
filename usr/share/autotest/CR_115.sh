#!/bin/sh

#camera: S3

rsFILE="/home/`whoami`/.cache/autotest.txt"
cheese &
sleep 2

zenity --question --title="camera: s3" --ok-label="OK" --cancel-label="Cancel" --text="press 'OK', system will goto S3 status.\n then press any button to wakeup"

OK_1=`echo $?`
if [ "X$OK_1" = "X0" ]; then
	sudo pm-suspend 
	zenity --question --text="请检查画面清晰、没有卡顿延迟" --ok-label="Yes,it's OK" --cancel-label="No.it's NOT ok"
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

zenity --info --text="This case Finish." --title="case finish"

