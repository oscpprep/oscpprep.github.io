#!/bin/bash
echo "usage ./samba_enum.sh <ip_address> optionally check this in the script:<share_name>"
ip=$1
if [ ! -z $ip ]; then
	nmblookup -A $ip
	echo exit | smbclient -L \\\\$ip
	nmap --script smb-enum-shares -p 139,445 $ip
	smbmap -H $ip
	rpcclient -U "" -N $ip
	#smbclient \\\\$ip\\[share name]
	nmap --script smb-vuln* -p 139,445 $ip
	enum4linux -a $ip
	smbver.sh $ip "(139,445)"
	nmblookup -A $ip
	smbmap -H $ip

	echo "[*] for manually exploiting:
		ngrep/
		is a neat tool to grep on network data. Running something like ngrep -i -d tap0 's.?a.?m.?b.?a.*[[:digit:]]' port 139/
		in one terminal and then echo exit | smbclient -L <ip>
		wireshark/
		will give a bunch of information about the  connection. We can filter on ntlmssp.ntlmv2_response/
		"
fi

if [ $? -eq 0 ]; then 
	echo "[+] Success!"
else
	echo "[-] FAILED"
fi
