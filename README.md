# autogen
*making life easier*

Stop wasting time compiling, typing, and finding payloads

### Features
1. Automatically detects interface for compiling and delivering payloads. default port is 4444 (chanage in script)
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
1. download and make the "autogen" shell script executable
```bash
git clone https://github.com/zedek1/autogen.git
chmod +x autogen/autogen
```
2. add autogen to .bashrc or .zshrc
```bash
alias autogen="path/to/autogen/autogen"
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

![image](https://github.com/zedek1/autogen/assets/45067032/b117e27e-7711-4fc2-992c-f442aa5a5071)


**output -d**

![image](https://github.com/zedek1/autogen/assets/45067032/3f205d34-1a7c-44ed-9d86-bf214a14d227)


**output -l**

![image](https://github.com/zedek1/autogen/assets/45067032/358c6305-da1a-4bae-82d0-1b2e25c8ab1f)
