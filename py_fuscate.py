#!/usr/bin/env python
# coding: utf-8
# By Sandaru Ashen: https://github.com/Sl-Sanda-Ru,https://t.me/Sl_Sanda_Ru


import os
import pip
import argparse
import random
import time
import marshal,lzma,gzip,bz2,binascii,zlib
try:
    import requests
    import tqdm
    import colorama
    import pyfiglet
except ModuleNotFoundError:
    print('\x1b[1m\x1b[31m' + '[!] required dependencies aren\'t installed\ninstalling..'.title())
    pip.main(['install', 'pyfiglet','colorama','tqdm','requests'])
    exit('\x1b[1m\x1b[92m' + '[+] dependencies installed\nrun the program again'.title())
clear = 'cls' if os.name == 'nt' else 'clear'
color_list = (colorama.Style.BRIGHT+colorama.Fore.BLUE,colorama.Style.BRIGHT+colorama.Fore.CYAN,colorama.Style.BRIGHT+colorama.Fore.GREEN,colorama.Style.BRIGHT+colorama.Fore.YELLOW,colorama.Style.BRIGHT+colorama.Fore.RED,colorama.Style.BRIGHT+colorama.Fore.MAGENTA,colorama.Style.BRIGHT+colorama.Fore.LIGHTYELLOW_EX,colorama.Style.BRIGHT+colorama.Fore.LIGHTRED_EX,colorama.Style.BRIGHT+colorama.Fore.LIGHTMAGENTA_EX,colorama.Style.BRIGHT+colorama.Fore.LIGHTBLUE_EX,colorama.Style.BRIGHT+colorama.Fore.LIGHTCYAN_EX,colorama.Style.BRIGHT+colorama.Fore.LIGHTGREEN_EX)
fonts = ['basic','o8','cosmic','graffiti','gradient','chunky','epic','poison','doom','avatar']
colorama.init(autoreset=True)
def marsh_enc(**kwargs):
    '''argumets:
    source <- source code of python program that you want to obfuscate as a string'''
    if not(isinstance(kwargs['source'],str)):
        print('argumet source must be string'.title())
        return None
    sel_cyph = random.choice((lzma,gzip,bz2,binascii,zlib))
    source_marshal = marshal.dumps(compile(kwargs['source'],'Py-Encode','exec'))
    if sel_cyph is binascii:
        cyph_compressed = binascii.b2a_base64(source_marshal)
    else:
        cyph_compressed = sel_cyph.compress(source_marshal)
    if sel_cyph is lzma:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(lzma.decompress(%s)))'%cyph_compressed
    elif sel_cyph is bz2:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(bz2.decompress(%s)))'%cyph_compressed
    elif sel_cyph is gzip:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(gzip.decompress(%s)))'%cyph_compressed
    elif sel_cyph is zlib:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(zlib.decompress(%s)))'%cyph_compressed
    elif sel_cyph is binascii:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(binascii.a2b_base64(%s)))'%cyph_compressed
def logo():
    os.system(clear)
    font = random.choice(fonts)
    color1 = random.choice(color_list)
    color2 = random.choice(color_list)
    while color1 == color2:
        color2 = random.choice(color_list)
    print(color1 + '_' * os.get_terminal_size().columns,end='\n'*2)
    print(color2 + pyfiglet.figlet_format('Py\nFuscate',font=font,justify='center',width=os.get_terminal_size().columns),end='')
    print(color1 + '_' * os.get_terminal_size().columns,end='\n'*2)
def parse_args():
    parser = argparse.ArgumentParser(epilog='example: python3 py_fuscate.py -i myprogram.py -o pyprogram_encoded.py -s 100',description='obfuscate python programs'.title())
    parser._optionals.title = "syntax".title()
    parser.add_argument('-i','--input',type=str,help='input file name'.title(),required=True)
    parser.add_argument('-o','--output',type=str,help='output file name'.title(),required=True)
    parser.add_argument('-s','--strong',type=int,help='strengthness of obfuscation'.title(),required=True)
    return parser.parse_args()
def check_update():
    global latest_ver
    latest_ver = requests.get('https://raw.githubusercontent.com/Sl-Sanda-Ru/Py-Fuscate/main/.version').text.strip()
    with open('.version') as version:
        if version.read().strip() != latest_ver:
            return True
        else:
            return False
def update(latest_ver):
    if '.git' in os.listdir():
        os.system('git stash && git pull')
    else:
        latest_source = requests.get('https://raw.githubusercontent.com/Sl-Sanda-Ru/Py-Fuscate/main/py_fuscate.py').content
        with open('py_fuscate.py','wb') as file:
            file.write(latest_source)
        with open('.version','w') as file:
            file.write(latest_ver)
def main():
    args = parse_args()
    if check_update():
        print(colorama.Style.BRIGHT + colorama.Fore.RED + '\t[!] update available'.title())
        print(colorama.Style.BRIGHT + colorama.Fore.LIGHTGREEN_EX + '\t[+] updating...'.title())
        update(latest_ver)
        exit(colorama.Style.BRIGHT + colorama.Fore.LIGHTGREEN_EX + '\t[+] successfully updated...\n\t run the program again'.title())
    print(random.choice(color_list) + '\t[+] encoding '.title() + args.input)
    encoded_pro = ''
    with tqdm.tqdm(total=args.strong) as pbar:
        for i in range(args.strong):
            if i == 0:
                encoded_pro = marsh_enc(source=open(args.input).read())
            else:
                encoded_pro = marsh_enc(source=encoded_pro)
            time.sleep(0.1)
            pbar.update(1)
        with open(args.output,'w') as file:
            file.write(f'#Encoded By Py-Fuscate\n#https://github.com/Sl-Sanda-Ru/Py-Fuscate\n{encoded_pro}')
    print(colorama.Style.BRIGHT+colorama.Fore.LIGHTGREEN_EX + '\t[+] encoding successful!\n\tsaved as '.title() + args.output)
if __name__ == '__main__':
    logo()
    main()
