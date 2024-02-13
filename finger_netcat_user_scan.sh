#!/usr/env python3
import subprocess as s
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("user_list_path", help="Each line from this list is being passed on to netcat directly.\
     So please be careful. You can even pass a single word to see the response from netcat.")
parser.add_argument("ip_address")
parser.add_argument("--port", help="If you don't specify ports, the cammands will run on all 65535 ports")
args = parser.parse_args()


def main_function():
    if args.port != None:
        ports = args.port
        ports = ports.split(",")
    else:
        input("Do you really want to run netcat on all 65535 ports? if not then press (ctrl + c)")
        ports = list(range(1,65535))

    users = str(args.user_list_path)
    ip_address = str(args.ip_address)

    with open(users, 'r') as users:
        users = users.readlines()
        for user in users:
        
            for port in ports:
                try:                    
                    print(f"[+] testing user: {user} for port: {port} ... \n")
                    user = user.strip("\n")
                    ps = s.Popen(("echo",user),
                                stdin=s.PIPE,
                                stdout=s.PIPE,
                                text=True)
                    
                    outs = s.check_output(("nc","-v","-w3",ip_address,str(port)), stdin=ps.stdout, timeout=3.5)
                    ps.wait()

                    print(outs.decode())
                except:
                    continue
                finally:
                    print("-"*40)

main_function()



