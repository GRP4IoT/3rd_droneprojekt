#!/bin/bash

#angiv stig til mathias
username="mathdesk"
password="abemad69"
i=192.168.137.122
x=1
pingfunc () {
    ping -c 1 $1 $i > /dev/null
    #[ $? -eq 0 ] && echo Node with IP: $i is up.
    #let x=x+1
    #hvis vi skal upload en file
    ftp-upload -h $i -u $username --password $password -d /srv/ftp /home/g4py/SFTP/1234.txt
    #hvis vi skal upload et directory
    ncftpput -R -v -u $username -p $password $i /srv/ftp /home/g4py/SFTP/testmappe3
}
pingfunc
