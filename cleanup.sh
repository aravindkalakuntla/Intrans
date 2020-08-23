#!/bin/sh
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin
folder=/data/datadrive5/waze/
find $folder -type d   -mtime +7 -exec rm -rf {} \;

folder=/data/datadrive5/iadot/
find $folder -type d -mtime +7 -exec rm -rf {} \;

folder=/data/datadrive5/bluetooth/
find $folder -type d -mtime +7 -exec rm -rf {} \;

folder=/data/datadrive5/inrix/
find $folder -type d -mtime +7 -exec rm -rf {} \;
