#!/bin/bash
#critical battery level suspend test

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

POWER=DC
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
#click_level low 10
#click_level critical 5

xdotool windowactivate $wid

if [ $POWER = "DC" ];then
##########critical level suspend test begin
echo "=================================================="
LEVEL=`upower -d | grep percentage|awk '{print $2}'|awk -F. '{print $1}'`
echo "Begin critical battery level suspend test ($((LEVEL-1))%) ..."
click_level low $(($LEVEL+2))
LEVEL=`upower -d | grep percentage|awk '{print $2}'|awk -F. '{print $1}'`
click_level critical 

sudo rm -rf /var/log/pm-suspend.log
while true
do
	if [ ! -e /var/log/pm-suspend.log ];then
		LEVEL_CRITICAL=`gsettings get org.gnome.settings-daemon.plugins.power percentage-critical`
		LEVEL=`upower -d | grep percentage|awk '{print $2}'|awk -F. '{print $1}'`
		if [ $LEVEL -lt $LEVEL_CRITICAL ];then
			echo "Fail to action in critical level"
			echo "[item_$1]=F" >> $RESULT
			echo "[item_$1_comment]=Fail to suspend in critical level ($((LEVEL-1))%)" >> $RESULT
			break
		fi
		set_wakealarm "+$WAKETIME"
	else
                SUCCESS_LOG=`cat /var/log/pm-suspend.log|grep Finished`
                if [ "X${SUCCESS_LOG}" != "X" ];then
			echo "Critical battery level suspend test successful"
			echo "[item_$1]=P" >> $RESULT
			echo "[item_$1_comment]=Critical battery level ($((LEVEL-1))%) suspend test successful" >> $RESULT
			break
		fi
	fi
	sleep 1
done
##########critical level suspend test end
fi
click_level low 10
click_level critical 5
gsettings set org.gnome.settings-daemon.plugins.power critical-battery-action shutdown
