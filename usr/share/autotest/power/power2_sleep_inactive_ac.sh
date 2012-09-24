#!/bin/bash
#test sleep_inactive_ac

set_wakealarm()
{
        if [ "X$1" = "X" ];then
                echo "Please give the setting time for wakealarm !!"
                return 1
        fi
        sudo /sbin/hwclock --hctosys
        sleep 1
	sudo chmod o+w /sys/class/rtc/rtc0/wakealarm
	echo 0 > /sys/class/rtc/rtc0/wakealarm
	echo "$1" > /sys/class/rtc/rtc0/wakealarm
	sudo chmod o-w /sys/class/rtc/rtc0/wakealarm
        if [ "$?" != "0" ];then
                zenity --error --text="set time to /sys/class/rtc/rtc0/wakealarm failed !!"
                echo -e "set time to /sys/class/rtc/rtc0/wakealarm failed !!" | tee -a $DO_LOG
                exit 1
        fi
}

click_idle()
{
check=`gsettings get org.gnome.settings-daemon.plugins.power sleep-$1-$2`
if $check;then
	if $3;then
		return
	fi
else
	if ! $3;then
		return
	fi
fi
case $1_$2 in
	display_ac)
		cor=$display_ac;;
	display_battery)
		cor=$display_battery;;
	inactive_ac)
		cor=$inactive_ac;;
	inactive_battery)
		cor=$inactive_battery;;
esac
xx=$(($x0 + `echo $cor|awk '{print $1}'`))
yy=$(($y0 + `echo $cor|awk '{print $2}'`))
xdotool mousemove $xx $yy
xdotool click 1
sleep 1
}

click_percentage()
{
xdotool mousemove $(($x0 + $1)) $(($y0 + $2))
xdotool click 1
}

click_level()
{
while true
do
LEVEL_CUR=`upower -d | grep percentage|awk '{print $2}'|awk -F. '{print $1}'`
percentage=`gsettings get org.gnome.settings-daemon.plugins.power percentage-$1`
if [ "X$2" != "X" ];then
                LEVEL_CUR=$(($2+1))
fi
#echo "per=$percentage"

if [ $percentage -lt $(($LEVEL_CUR-1)) ];then
        if [ "X$1" = "Xlow" ];then
                click_percentage $low_up
        else
                click_percentage $critical_up
        fi
elif [ $percentage -gt $(($LEVEL_CUR-1)) ];then
        if [ "X$1" = "Xlow" ];then
                click_percentage $low_down
        else
                click_percentage $critical_down
        fi
else
        break
fi
sync
done
}

icon_x=1265
icon_y=16

power_settings_x1=$icon_x
power_settings_y1=$(($icon_y + 90))
power_settings_x2=$icon_x
power_settings_y2=$(($icon_y + 120))

display_ac="61 114"
display_battery="61 145"
inactive_ac="61 208"
inactive_battery="61 238"

low_up="205 297"
low_down="205 310"
critical_up="205 327"
critical_down="205 340"
gsettings set org.gnome.settings-daemon.plugins.power critical-battery-action suspend
gsettings set org.gnome.desktop.screensaver lock-enabled false
sync

POWER=AC
if [ "X$POWER" = "XAC" ];then
	while upower -d|grep 'state'|grep 'discharging' >/dev/null
	do
#		echo "Please plug in the AC power, then press enter to continue"
#		read
		zenity --info --text="Please plug in the AC power,\n\n then press OK"
	done
else
	until upower -d|grep 'state'|grep 'discharging' >/dev/null
	do
#		echo "Please plug out the AC power, then press enter to continue"
#		read
		zenity --info --text="Please plug out the AC power,\n\n then press OK"
	done
fi

for power_settings_y in $power_settings_y1 $power_settings_y2
do
xdotool mousemove $icon_x $icon_y
xdotool click 1
sleep 2
xdotool mousemove $icon_x ${power_settings_y}
xdotool click 1
sleep 2
wid=$(xdotool search --name "Power")

if [ "X${wid}" = "X" ];then
	xdotool mousemove $icon_x $icon_y
	xdotool click 1
	continue
fi
break
done

if [ "X${wid}" = "X" ];then
exit
fi

xdotool windowactivate $wid
sleep 3
x0=`xwininfo -id $wid|grep "Absolute upper-left X"|awk '{print $4}'`
y0=`xwininfo -id $wid|grep "Absolute upper-left Y"|awk '{print $4}'`
xdotool mousemove $x0 $y0
xdotool click 1

#time to wake up after suspend
WAKETIME=10

RESULT="$HOME/.cache/autotest.txt"

#acceptable time deviation
TIME_RANGE=50

click_idle display ac false
click_idle display battery false
click_idle inactive ac false
click_idle inactive battery false
click_level low 10
click_level critical 5

xdotool windowactivate $wid
############################################idle test begin
###########################suspend computer test begin
if [ $POWER = "DC" ]; then
	click_idle inactive battery true
	TIMEOUT=`gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout`
else
	click_idle inactive ac true
	TIMEOUT=`gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout`
fi
echo "=================================================="
echo "$POWER: suspend test begin (${TIMEOUT}s)..."

BEFORE_S3_TIME=`awk '{print int($1)}' /proc/uptime`
sudo rm -rf /var/log/pm-suspend.log

while true
do
	sleep 1
	NOW_TIME=`awk '{print int($1)}' /proc/uptime`
	if [ ! -e /var/log/pm-suspend.log ];then
		REAL_ENTER_S3_TIME=$(($NOW_TIME - $BEFORE_S3_TIME))
		if [ ${REAL_ENTER_S3_TIME} -gt $(($TIMEOUT + $TIME_RANGE + $WAKETIME)) ];then
			echo "$POWER: failed to suspend"
			echo "[item_$1]=F" >> $RESULT
			echo "[item_$1_comment]=$POWER: idle ${TIMEOUT}s failed to suspend" >> $RESULT
			break
		fi
		set_wakealarm "+$WAKETIME"
	else
		SUCCESS_LOG=`cat /var/log/pm-suspend.log|grep Finished`
		if [ "X${SUCCESS_LOG}" != "X" ];then
			if [ $REAL_ENTER_S3_TIME -ge $(($TIMEOUT - $TIME_RANGE)) ] && [ $REAL_ENTER_S3_TIME -le $(($TIMEOUT + $TIME_RANGE)) ];then
				echo "$POWER: suspend test succeed, actual time ${REAL_ENTER_S3_TIME}s"
				echo "[item_$1]=P" >> $RESULT
				echo "[item_$1_comment]=$POWER: idle ${TIMEOUT}s suspend test succeed, actual time ${REAL_ENTER_S3_TIME}s" >> $RESULT
				break
			else
				echo "$POWER: enter suspend but not in $TIMEOUT s"
				echo "Actual time to suspend: ${REAL_ENTER_S3_TIME}s"
				echo "[item_$1]=F" >> $RESULT
				echo "[item_$1_comment]=$POWER: enter suspend but not in ${TIMEOUT}s, actual time ${REAL_ENTER_S3_TIME}s" >> $RESULT
				break
			fi
		fi
	fi
done
sleep 1
click_idle inactive ac false
click_idle inactive battery false
###########################suspend computer test end
############################################idle test end
