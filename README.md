# tool-kit
*making life easier*


first make autogen executable
```bash
chmod 777 autogen
```

then add the path to .bashrc or .zshrc
```bash
export PATH=$PATH:~/auto
```

options
```
-c    -> compile basic binaries
-m    -> compile meterpreter binaries
-d    -> compile all binaries but don't list
-g    -> generate powershell one liners
-s    -> don't start python http server
-h    -> help menu

-i [ip]    -> manually set LHOST
-p [port]  -> manually set LPORT
```

