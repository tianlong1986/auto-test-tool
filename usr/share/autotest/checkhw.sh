#!/bin/sh
wlan=`lspci -nn | grep Network | cut -d":" -f3- `
wlan=`echo "$wlan" | sed "s@\(.*\)\(\[.*\]\)@ \2\1@"`
[ "$wlan" == "" ] && wlan=" No"

#bluetooth
bluetooth=`lsusb -vvv | grep -i "Bluetooth Module" -B13 | head -n1 | cut -d":" -f2- | sed -s "s@ID @[@" | sed -s "s@\(\w\) @\1] @"`
[ "$bluetooth" == "" ] && bluetooth=`lsusb -vvv | grep -i "BCM" -B13 | head -n1 | cut -d":" -f2- | sed -s "s@ID @[@" | sed -s "s@\(\w\) @\1] @"`
bluetooth_id=`lsusb -vvv | grep -i "Bluetooth" -B13 |grep "ID" |awk '{print $6}'`
bluetooth_desc=`lsusb -vvv | grep -i "Bluetooth" -B13 |grep "ID"`
if [  -z "$bluetooth_id" ];then
bluetooth_id=`lsusb -vvv | grep -i "BCM" -B13 |grep "ID" |awk '{print $6}'`
bluetooth_desc=`lsusb -vvv | grep -i "BCM" -B13 |grep "ID"`
fi
if [  -z "$bluetooth_id" ];then
bluetooth_id="No"
bluetooth_desc="No"
fi

show_no="NO"
echo "Now begin hotkey test,this machine " > /tmp/.hotkey_tip
if [ "$wlan" = "No" ];then
	wifi="No wireless device"
	echo "no wireless device," >> /tmp/.hotkey_tip
	show_no="YES"
else
	wifi="wireless device"
	echo "has a wireless device," >> /tmp/.hotkey_tip
fi

if [ "$bluetooth_desc" = "No" ]; then
	bt="no bluetooth device"
	echo "no bluetooth device." >> /tmp/.hotkey_tip
	show_no="YES"
else
	bt="bluetooth device"
	echo "has a bluetooth device." >> /tmp/.hotkey_tip
fi
if [ "$show_no" = "YES" ];then
	echo "You should skip these no device test items." >> /tmp/.hotkey_tip
fi

