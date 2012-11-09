#!/bin/sh
rsFILE="/home/`whoami`/.cache/autotest.txt"
WLAN_DEV=`iwconfig |grep ESSID |awk '{print $1}'`
LAN_DEV=`cat /proc/net/dev |grep :|awk '{print $1}'|grep -v lo |grep -v $WLAN_DEV |sed 's/:$//'`
rfkill unblock wifi
write_linpus_ap2_conf()
{
sudo bash -c "echo \"
ESSID=\"linpus-ap2\"
MODE=Managed
BSSID=F0:7D:68:7C:B5:FA
KEY_MGMT=WPA-PSK
TYPE=Wireless
BOOTPROTO=dhcp
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=yes
NAME=\"Wireless connection linpus-ap2\"
UUID=6de6816f-9b40-423c-943d-da40a8077acf
ONBOOT=yes
\" >/etc/sysconfig/network-scripts/ifcfg-wireless-linpus-ap2"

sudo bash -c "echo \"WPA_PSK=\"warrencoles\"\" > /etc/sysconfig/network-scripts/keys-wireless-linpus-ap2"
}
write_linpus_armtp_conf()
{
 sudo bash -c "echo \"
ESSID=\"Linpus-ArmTP\"
MODE=Managed
BSSID=00:26:5A:B0:C6:CA
SECURITYMODE=open
DEFAULTKEY=1
TYPE=Wireless
BOOTPROTO=dhcp
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=yes
NAME=Wireless-Linpus-ArmTP
UUID=9678925d-1ae5-4a37-9b68-28c8f9884698
ONBOOT=yes
\" >/etc/sysconfig/network-scripts/ifcfg-wireless-linpus-armtp"

sudo bash -c "echo \"KEY1=s:98765\" > /etc/sysconfig/network-scripts/keys-wireless-linpus-armtp"
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

ftp_download_file_test()
{
echo "now download wifi_test.img..."
wget ftp://olpc:olpc@192.168.1.200/autotest/wifi_test.img -o wget.log

if [ $? = 0 ]; then
        download_speed=`cat wget.log|grep saved | sed 's/.*(\(.*\)).*/\1/'`
        echo "FTP download speed:$download_speed"|tee -a wifi_result.log
        return 0
else
        echo "FTP download file test failed"|tee  -a wifi_result.log
        return 1
fi
}


sudo ifconfig $LAN_DEV down
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
	FAIL_REASON="$FAIL_REASON ap2 cannot ping www.baidu.com,"
	TEST_RESULT="F"
fi
ftp_download_file_test
if [ $? != 0 ];then
	TEST_RESULT="F"
	FAIL_REASON="ap2 ownload big buck from ftp200 fail,"
fi
rm -f wifi_test.img

sleep 1
echo "Begin to test linpus-ArmTp"
write_linpus_armtp_conf
sleep 3
echo "Connect linpus-ArmTp..."
TEST_RESULT="P"
nmcli con up uuid 9678925d-1ae5-4a37-9b68-28c8f9884698 --timeout 35
if [ $? != 0 ];then
        FAIL_REASON="$FAIL_REASON linpus-ArmTp connected fail,"
	TEST_RESULT="F"
fi
echo "linpus-ArmTp Connected."|tee -a wifi_result.log

ping_test
if [ $? != 0 ];then
	FAIL_REASON="$FAIL_REASON  ArmTp cannot ping www.baidu.com,"
	TEST_RESULT="F"
fi
ftp_download_file_test
if [ $? != 0 ];then
	TEST_RESULT="F"
	FAIL_REASON="$FAIL_REASON ArmTp download big buck from ftp200 fail,"
fi
echo "item_$1=$TEST_RESULT" >> $rsFILE
echo "item_$1_comment=$FAIL_REASON" >> $rsFILE
sudo ifconfig $LAN_DEV up
rm -f wifi_result.log
rm -f wget.log
exit 0
