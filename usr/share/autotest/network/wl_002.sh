#!/bin/sh
rsFILE="/home/`whoami`/.cache/autotest.txt"
WIRED_DEV=`cat /proc/net/dev |grep :|awk '{print $1}'|grep -v [wlan,wwan,lo]|sed 's/:$//'`
write_linpus_ap2_conf()
{
echo "
ESSID="linpus-ap2"
MODE=Managed
BSSID=F0:7D:68:7C:B5:FA
KEY_MGMT=WPA-PSK
TYPE=Wireless
BOOTPROTO=dhcp
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=yes
NAME="Wireless connection linpus-ap2"
UUID=6de6816f-9b40-423c-943d-da40a8077acf
ONBOOT=yes
" >/etc/sysconfig/network-scripts/ifcfg-wireless-linpus-ap2

 echo "WPA_PSK=\"warrencoles\"" > /etc/sysconfig/network-scripts/keys-wireless-linpus-ap2
}

ping_test()
{
ping www.baidu.com -c 5
if [ $? = 0 ]; then
        echo "connection ping Baidu successful"|tee -a wifi_result.log
        return 0
else
        echo "connection ping Baidu failed"|tee  -a wifi_result.log
        return 1
fi
}

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


sudo ifconfig $WIRED_DEV down
sleep 1
echo "Begin to test linpus-ap2"
write_linpus_ap2_conf
sleep 3
echo "Connect linpus-ap2..."
TEST_RESULT="P"
nmcli con up uuid 6de6816f-9b40-423c-943d-da40a8077acf --timeout 35
if [ $? != 0 ];then
        FAIL_REASON="linpus-ap2 connected fail,"
	TEST_RESULT="F"
fi
echo "linpus-ap2 Connected."|tee -a wifi_result.log

ping_test
if [ $? != 0 ];then
	FAIL_REASON="$FAIL_REASON cannot ping www.baidu.com"
	TEST_RESULT="F"
fi
ftp_download_big_buck_test
if [ $? != 0 ];then
	TEST_RESULT="F"
	FAIL_REASON="Download big buck from ftp200 fail"
fi
echo "item_$1=$TEST_RESULT" >> $rsFILE
echo "item_$1_comment=$FAIL_REASON" >> $rsFILE
sudo ifconfig $WIRED_DEV down
sleep 1
echo "Begin to test linpus-ap2"
write_linpus_ap2_conf
sleep 3
echo "Connect linpus-ap2..."
TEST_RESULT="P"
nmcli con up uuid 6de6816f-9b40-423c-943d-da40a8077acf --timeout 35
if [ $? != 0 ];then
        FAIL_REASON="linpus-ap2 connected fail,"
	TEST_RESULT="F"
fi
echo "linpus-ap2 Connected."|tee -a wifi_result.log

ping_test
if [ $? != 0 ];then
	FAIL_REASON="$FAIL_REASON cannot ping www.baidu.com"
	TEST_RESULT="F"
fi
ftp_download_big_buck_test
if [ $? != 0 ];then
	TEST_RESULT="F"
	FAIL_REASON="Download big buck from ftp200 fail"
fi
echo "item_$1=$TEST_RESULT" >> $rsFILE
echo "item_$1_comment=$FAIL_REASON" >> $rsFILE
sudo ifconfig $WIRED_DEV up
exit 0
