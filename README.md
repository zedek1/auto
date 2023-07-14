# tool-kit
*making life easier*

1 place the folder in your users home directory named "auto"

2 make autogen executable
```bash
chmod +x autogen
```

3 add it to .bashrc or .zshrc
```bash
alias autogen="/home/$USER/auto/autogen"
```

usage
```
-c    -> compile basic binaries
-m    -> compile meterpreter binaries
-d    -> compile all binaries but don't list
-w    -> setup webshells and don't list
-g    -> generate powershell one liners
-s    -> don't start python http server
-h    -> help menu

-i [ip]    -> manually set LHOST
-p [port]  -> manually set LPORT
```

