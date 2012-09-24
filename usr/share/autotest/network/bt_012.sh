#!/bin/sh
rsFILE="/home/`whoami`/.cache/autotest.txt"

	sendFile="P"
	comment=""
echo "item_$1=$sendFile" >> $rsFILE
echo "item_$1_comment=$comment" >> $rsFILE
