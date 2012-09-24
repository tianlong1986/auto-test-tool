#!/bin/sh
rsFile="~/.cache/autotest.ini"
gconftool-2 -s /desktop/gnome/file_sharing/bluetooth_require_pairing --type=bool false
gconftool-2 -s /desktop/gnome/file_sharing/bluetooth_obexpush_enabled --type=bool true
gconftool-2 -s /desktop/gnome/file_sharing/bluetooth_accept_files --type=string always
gconftool-2 -s /desktop/gnome/file_sharing/require_password --type=string naver
gconftool-2 -s /desktop/gnome/file_sharing/bluetooth_notify --type=bool true
gconftool-2 -s /desktop/gnome/file_sharing/enabled --type=bool false
gconftool-2 -s /desktop/gnome/file_sharing/bluetooth_require_pairing --type=bool false
if [ $? = 0 ]; then
	echo "set accept file config success"
fi
sudo hciconfig hci0 name auto_bt

if [ $? = 0 ]; then
	echo "set bluetooth name success"
fi
#打开蓝牙的可见性，使其他机器可以搜索到
sudo hciconfig hci0 piscan
if [ $? = 0 ];then
	bt_scan="P"
else
	bt_scan="F"
fi

#搜索周围的蓝牙设备，只找名字叫auto_bt的，这是我们测试机器的命名
dest_bt=`hcitool scan |grep auto_bt | awk '{print $1}' |head -n 1`
echo "now will send 1.log to $dest_bt"
if [ "X$dest_bt" = "X" ]; then
	echo "Can not find the match bluetooth device"
	exit 1
fi
bluetooth-sendto  --device="$dest_bt" 1.log
if [ $? = 0 ];then
	bt_send="P"
else
	bt_send="F"
fi
#echo "[network]" >> /tmp/autotest.ini
echo "moudle_$1=$bt_scan" >> $rsFile
echo "moudle_$1_comment=$bt_scan" >> /tmp/autotest.ini
echo "bluetooth_sendfile=$bt_send" >> /tmp/autotest.ini
echo "send file success!"
