#!/bin/sh

ID=$1
MODULE="P"
MODULE_COMMENT=""

function set_wakealarm()
{
        sudo /sbin/hwclock --hctosys
        sleep 1
        sudo sh -c "echo 0 > /sys/class/rtc/rtc0/wakealarm"
        sudo sh -c "echo +10 > /sys/class/rtc/rtc0/wakealarm  "
        if [ "$?" != "0" ];then
                echo "set time to /sys/class/rtc/rtc0/wakealarm failed !!" 
                exit 1
        fi
        sudo /usr/sbin/pm-suspend
}

function time_out()
{
	sleep_sec=0
	while true
	do
		DEVICE="`cat /proc/mounts  | tail -1 | awk '{print $1}' | grep $2`"
		echo $DEVICE
		if [ "${DEVICE}a" != "a" ] ; then          # insert a XX disk  
			return 0 ;
		fi

		if [ $((sleep_sec)) -gt 15 ] ; then   # timeout handing
			return 1 ;
		fi
		sleep 1
		((sleep_sec++))
		echo $sleep_sec
	done
}


function XX_card_autotest()
{
	echo "autotest"  > $HOME/linpus_autotest
	zenity  --question  --text="please insert the $1 disk and then click \"yes\" button"
	if [ "$?" == "0" ];then

		time_out $1 $2
		if [ "$?" == "0" ];then 		# find a XX disk

			FORMAT="`cat /proc/mounts  | tail -1 | awk '{print $3}'`"
			if [ "${FORMAT}" != "vfat" ] ; then          # a U disk 
				zenity --info  --text="please format the disk as vfat"
				MODULE_COMMENT="$MODULE_COMMENT $1: need format the disk as vfat |"
				MODULE="F"
				return 0 ;
			fi

			MOUNT_PATH="`cat /proc/mounts  | tail -1 | awk '{print $2}'`"
			cp -rf  $HOME/linpus_autotest  $MOUNT_PATH 
			if [ "$?" != "0" ] ;then   #  copy  error
				MODULE_COMMENT="$MODULE_COMMENT $1: copy error |"
				MODULE="F"
				return 0 ;
			fi
			sleep 1

			mv $MOUNT_PATH/linpus_autotest  $MOUNT_PATH/linpus_autotest_bak
 			if [ "$?" != "0" ] ;then   #  mv  error
				MODULE_COMMENT="$MODULE_COMMENT $1: mv error | "
				MODULE="F"
				return 0 ;
			fi 
			sleep 1 

			rm -rf  $MOUNT_PATH/linpus_autotest_bak
 			if [ "$?" != "0" ] ;then   #  rm   error
				MODULE_COMMENT="$MODULE_COMMENT $1: rm error | "
				MODULE="F"
				return 0 ;
			fi
			sleep 1
			sudo umount $MOUNT_PATH

			if [ "$1" == "usb" ] ; then          # only u disk test
				echo "S3 test"
				sudo umount $MOUNT_PATH
				set_wakealarm 
#				zenity --question  --text="please reinsert the U disk and then click \"yes\" button"
#				if [ "$?" == "0" ];then
				sleep 4
				DEVICE="`cat /proc/mounts  | tail -1 | awk '{print $1}' | grep $2`"
				if [ "${DEVICE}a" == "a" ] ; then          # a  disk  and auto mount
					MODULE_COMMENT="$MODULE_COMMENT $1: can't auto mount after after resume from S3 |"
					MODULE="F"
					echo "can't auto mount after resume from S3"
					return 0 ;
				fi
				sudo umount $MOUNT_PATH
#				fi
			fi

			echo "reboot test "
			echo $1 > /tmp/media_reboot_test
			sleep 3 
			sudo reboot

		else
			echo "insert $1 disk error or can't auto mount" 
			return 2 ; 
		fi
	else
		MODULE_COMMENT="$MODULE_COMMENT $1: skip the $1 test |"
		MODULE="P"
		echo "skip the $1 test"
	fi
}

function usb_mouse_and_keyboard()
{
	zenity  --question  --text="please insert the usb mouse and then click \"yes\" button"
	if [ "$?" == "0" ];then
		sleep 3
		#time_out $1 $2
		DEVICE="` dmesg  | tail -5 | grep "USB Mouse" | grep devices `"
		echo $DEVICE
		if [ "${DEVICE}a" != "a" ] ; then   
			echo "S3 test"
			set_wakealarm 
			zenity --info  --text="please mobile usb mouse, and ensure that the use of normal"
		else
			echo  "can't find a usb mouse"
		fi
	else
		echo "skip the usb mouse test"
	fi

	zenity  --question  --text="please insert the usb keyboard and then click \"yes\" button"
	if [ "$?" == "0" ];then
		sleep 3
		#time_out $1 $2
		DEVICE="`dmesg | tail -5 | grep "USB Keyboard"  | grep devices `"
		echo $DEVICE
		if [ "${DEVICE}a" != "a" ] ; then   
			echo "S3 test"
			set_wakealarm 
			zenity --info  --text="please using the keyboard, and ensure that the use of normal"
		else
			echo  "can't find a USB Keyboard mouse"
		fi
	else
		echo "skip the usb keyboard test"
	fi

}

function insert_error_and_repeat_do()
{
	while true
	do
		XX_card_autotest  $1 $2
		if [ "$?" == "2" ];then
			zenity  --question  --text="insert $1 disk error or can't auto mount,\n\"yes\" repeat,  \"no\" cancel"
			if [ "$?" != "0" ];then
				MODULE_COMMENT="$MODULE_COMMENT $1: insert $1 disk error or can't auto mount |"
				MODULE="F"
				break
			fi
		else 
			break
		fi
	done
	echo "item_$ID=$MODULE"  >> $HOME/.cache/autotest.txt
	echo "item_$ID_comment=$MODULE_COMMENT"  >> $HOME/.cache/autotest.txt
	MODULE_COMMENT=""
	MODULE="P"

}


function reboot_check()
{
	DEVICE="`cat /proc/mounts  | tail -1 | awk '{print $1}' | grep $2`"
	if [ "${DEVICE}a" != "a" ] ; then          # insert a XX disk 
		echo "$1 card reboot test OK " 
	else
		MODULE_COMMENT="$MODULE_COMMENT $1: can't auto mount after reboot |"
		MODULE="F"
		echo "$1 can't auto mount after reboot "
	fi
	sudo umount /media/*
	echo "a" > /tmp/media_reboot_test

	echo "item_$ID=$MODULE"  >> $HOME/.cache/autotest.txt
	echo "item_$ID_comment=$MODULE_COMMENT"  >> $HOME/.cache/autotest.txt
	MODULE_COMMENT=""
	MODULE="P"

}


FLAG="` cat /tmp/media_reboot_test `a"

if [ "${FLAG}" != "usba" -a "${FLAG}" != "MMCa" -a "${FLAG}" != "SDa" -a "${FLAG}" != "MSa" -a "${FLAG}" != "XDa" ] ; then  
	insert_error_and_repeat_do  usb sd
fi
if [ "${FLAG}" == "usba" ] ; then  
	reboot_check  usb sd
fi

#if [ "`dmesg  | grep Realtek | grep card | grep reader `a" != "a" ] ; then          # realtek  card reader support
#	if [ "${FLAG}" != "MMCa" -a "${FLAG}" != "SDa" ] ; then  
#		insert_error_and_repeat_do  MMC  sd
#	fi
#	if [ "${FLAG}" == "MMCa" ] ; then  
#		reboot_check  MMC sd
#	fi


#	if [ "${FLAG}" != "SDa" ] ; then  
#		insert_error_and_repeat_do  SD  sd

#	fi
#	if [ "${FLAG}" == "SDa" ] ; then  
#		reboot_check  SD sd
#	fi


#elif [ "`lspci | grep JMicron `a" != "a" ] ; then  				 # JMicron card reader support
#	DEVICE_SUP="`lspci  | grep  \"MS Host\" `"
#	if [ "${DEVICE_SUP}a" != "a" ] ; then          # ms support
#		if [ "${FLAG}" != "MMCa" -a "${FLAG}" != "SDa" -a "${FLAG}" != "MSa" -a "${FLAG}" != "XDa" ] ; then  
#			insert_error_and_repeat_do  MS msp
#		fi
#		if [ "${FLAG}" == "MSa" ] ; then  
#			reboot_check  MS msp
#		fi
#	fi
#
#	DEVICE_SUP="`lspci  | grep  \"xD Host\" `"
#	if [ "${DEVICE_SUP}a" != "a" ] ; then          # xd support
#		if [ "${FLAG}" != "MMCa" -a "${FLAG}" != "SDa" -a "${FLAG}" != "XDa" ] ; then  
#			insert_error_and_repeat_do  XD xd_card
#		fi
#		if [ "${FLAG}" == "XDa" ] ; then  
#			reboot_check  XD xd_card
#		fi
#	fi
#
#	DEVICE_SUP="`lspci  | grep  \"MMC Host\" `"
#	if [ "${DEVICE_SUP}a" != "a" ] ; then          # mmc support
#		if [ "${FLAG}" != "MMCa" -a "${FLAG}" != "SDa" ] ; then  
#			insert_error_and_repeat_do   MMC mmc
#		fi
#		if [ "${FLAG}" == "MMCa" ] ; then  
#			reboot_check  MMC mmc
#		fi
#	fi
#
#	DEVICE_SUP="`lspci  | grep  \"SD Host\" `"
#	if [ "${DEVICE_SUP}a" != "a" ] ; then          # sd support
#		if [ "${FLAG}" != "SDa" ] ; then  
#			insert_error_and_repeat_do   SD mmc
#		fi
#		if [ "${FLAG}" == "SDa" ] ; then  
#			reboot_check  SD mmc
#		fi
#
#	fi
#fi

usb_mouse_and_keyboard


