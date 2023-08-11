# autogen
*making life easier*

Stop wasting time compiling, typing, and finding payloads

### Features
1. Automatically detects interface for compiling and delivering payloads. default port is 4444 (chanage at top of script)
2. Edits and/or compiles web shells, msfvenom meterpreter commands, and custom shell payloads
3. Generates one-liners including base64-encoded powershell reverse shells and url-encoded shells
4. Comes with a variety of tools for Active Directory, Pivoting, Windows & Linux privilege escalation

**listed below are automatically edited/compiled with LHOST and LPORT (-d for all)**

**custom payloads (-c)**
1. winshell.exe
2. dllshell.dll
3. rs_service.exe

**web shells (-w)**
1. phpshell.php | pentestmonkey
3. wpshell-pm.zip
4. shell.aspx

**meterpreter shells (-m)**
1. mettcp.exe
2. methttps.exe
3. linmettcp.elf

### Installation
1. put the folder in your users home directory and make sure it's named "auto"
```bash
cd ~
git clone https://github.com/zedek1/auto.git
```
2. make the "autogen" shell script executable
```bash
cd auto
chmod +x autogen
```
3. add autogen to .bashrc or .zshrc
```bash
alias autogen="/home/$USER/auto/autogen"
```

### Usage
```
usage: autogen <options>

-i [ip]    -> manually set LHOST
-p [port]  -> manually set LPORT

--- main options
-r    -> only show reverse shell one-liners and don't start http server (default: all = -rl)
-l    -> only show payload list (default: all = -rl)

--- payload options
-c    -> compile basic binaries
-m    -> compile meterpreter binaries
-w    -> setup webshells
-d    -> setup all

--- other
-s    -> don't start python http server
-h    -> help menu
```

### Screenshots

**output -r**

![image](https://github.com/zedek1/auto/assets/45067032/1affc255-e7c5-43f8-8566-c6daa60bdb40)

**output -d**

![image](https://github.com/zedek1/auto/assets/45067032/ec0d99ff-ca65-4eb3-a9d9-b950f282a388)

**output -l**

![image](https://github.com/zedek1/auto/assets/45067032/2bb68255-63e0-4ed6-95c7-4d1935a6046d)

### Full -l List
```text
├── enum
│   ├── lin
│   │   ├── LinEnum.sh
│   │   ├── linpeas.sh
│   │   ├── pspy64
│   │   ├── traitor
│   │   └── unix-privesc-check
│   └── win
│       ├── PowerUp.ps1
│       ├── PowerView.ps1
│       ├── PsExec64.exe
│       ├── PsLoggedon64.exe
│       ├── SharpHound.exe
│       ├── SharpHound.ps1
│       └── winPEASx64.exe
├── exploits
│   ├── lin
│   │   ├── chocobo_root.c
│   │   ├── dirty
│   │   ├── dirty.c
│   │   ├── dirtycow.c
│   │   ├── ebpf_verifier.c
│   │   ├── exp
│   │   ├── exp_file_credential.c
│   │   ├── exploit_nss
│   │   ├── perf_swevent.c
│   │   ├── polkit3560.sh
│   │   ├── ptrace.c
│   │   ├── PwnKit
│   │   └── pwnkit4034.c
│   └── win
│       └── PrintSpoofer64.exe
└── payloads
    ├── lin
    │   ├── chisel
    │   ├── linmettcp.elf
    │   ├── ncat
    │   ├── nmap
    │   └── socat
    ├── web
    │   ├── phpshell.php
    │   ├── powny.php
    │   ├── shell.aspx
    │   ├── simple-backdoor.php
    │   ├── wpshell-basic.php
    │   ├── wpshell-pm.php
    │   └── wpshell-pm.zip
    └── win
        ├── adduser.exe
        ├── dllshell.dll
        ├── dlluseradd.dll
        ├── kerbrute_windows_amd64.exe
        ├── methttps.exe
        ├── mettcp.exe
        ├── mimikatz.exe
        ├── nc.exe
        ├── nmap.exe
        ├── plink.exe
        ├── powercat.ps1
        ├── rs_service.exe
        ├── Rubeus.exe
        ├── SharpChisel.exe
        ├── socat
        └── winshell.exe
```
