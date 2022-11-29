#!/bin/bash
username="mathdesk"
i=192.168.137.122

sendfunc () {
    sftp -oPort=22 -b sftp_commands.txt -r mathdesk@192.168.137.122
}
#den pinger ip adressen og hvis der er connection kører den sendfunc
if ping -c 1 $192.168.137.122 &> /dev/null
then
    sendfunc
else 
    echo "den er ikke oppe"
fi

#DU SKAL HAVE sftp_commands.txt KONFIGURARET RIGTIGT!!! 
#DU SKAL HAVE sftp_commands.txt KONFIGURARET RIGTIGT!!! 
#DU SKAL HAVE sftp_commands.txt KONFIGURARET RIGTIGT!!! 
#DU SKAL HAVE sftp_commands.txt KONFIGURARET RIGTIGT!!! 
#DU SKAL HAVE sftp_commands.txt KONFIGURARET RIGTIGT!!! 

