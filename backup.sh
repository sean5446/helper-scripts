#!/bin/bash

#set -x

# /home/pi/.kodi/userdata/
# /etc/fstab example:
# //APOLLO/Mirror /mnt/apollo-mirror cifs usermame=wolf,password=Passw0rd 0 0 

seperat='============================='
logfile=/root/log-backup.txt
lmirror=/media/styx/BACKUP/
rmirror=/mnt/apollo-mirror/
# trailing slash is important

running=$(ps aux | grep rsync | grep -v grep | wc -l)
if [ 0 -ne $running ] ; then
  /bin/date >> $logfile
  /bin/echo already running >> $logfile
  /bin/echo >> $logfile
  exit
fi

/bin/umount $rmirror &> /dev/null
/bin/sleep 2

/bin/mount $rmirror
mountret=$?
/bin/sleep 2

/bin/echo $seperat >> $logfile
/bin/date >> $logfile
/bin/echo "mount  $mountret" >> $logfile

if [ 0 -eq $mountret ] ; then
  /bin/echo "rsync starting" >> $logfile
  /usr/bin/rsync --exclude '$RECYCLE.BIN' --exclude 'System Volume Information' --exclude 'Recovery' --delete -az $rmirror $lmirror
  # can also use --delete-after
  /bin/echo "rsync  $?" >> $logfile
  /bin/umount $rmirror
  /bin/echo "umount $?" >> $logfile
fi

/bin/date >> $logfile
/bin/echo $seperat >> $logfile
/bin/echo >> $logfile
/bin/echo >> $logfile

