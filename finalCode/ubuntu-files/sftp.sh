#!/bin/bash


#angiv stig

username="g4py"
i=192.168.137.217


sendfunc () {

    sftp -oPort=22 -b sftp_commands.txt -r g4py@192.168.137.217
}

if oing -c 1 $i &> /dev/null
then
    sendfunc

else
    echo "den er ikke oppe"

fi
