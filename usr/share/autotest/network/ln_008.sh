#!/bin/sh
rsFILE="/home/`whoami`/.cache/autotest.txt"
WLAN_DEV=`iwconfig |grep ESSID |awk '{print $1}'`
LAN_DEV=`cat /proc/net/dev |grep :|awk '{print $1}'|grep -v lo |grep -v $WLAN_DEV |sed 's/:$//'`
ftp_download_big_buck_test()
{
echo "now download big-buck-bunny.ogv..."
wget ftp://olpc:olpc@192.168.1.200/QA/test_samples/Video/big-buck-bunny.ogv -o wget.log

if [ $? = 0 ]; then
        download_speed=`cat wget.log|grep saved | sed 's/.*(\(.*\)).*/\1/'`
        echo "FTP download speed:$download_speed"|tee -a wifi_result.log
        return 0
else
        echo "FTP download file test failed"|tee  -a wifi_result.log
        return 1
fi
}
sudo ifconfig $LAN_DEV up

rfkill block wifi
sleep 2
ftp_download_big_buck_test
if [ $? = 0 ];then
        GET_FTP="P"
	comment=""
else
        GET_FTP="F"
	comment="Download big buck from ftp200 fail"
fi
echo "item_$1=$GET_FTP" >> $rsFILE
echo "item_$1_comment=$comment" >> $rsFILE
rfkill unblock wifi
