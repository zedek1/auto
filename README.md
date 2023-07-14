# tool-kit
*making life easier*


first make autogen executable
```bash
chmod +x autogen
```

then add it to .bashrc or .zshrc
```bash
alias autogen="/[LOCATION]/autogen"
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

