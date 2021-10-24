#!/usr/bin/env python
# coding: utf-8
# By Sandaru Ashen: https://github.com/Sl-Sanda-Ru,https://t.me/Sl_Sanda_Ru


import os
import sys
import subprocess
import argparse
import random
import time
import marshal
import lzma
import gzip
import bz2
import binascii
import zlib
try:
    import requests
    import tqdm
    import colorama
    import pyfiglet
except ModuleNotFoundError:
    if os.name == 'nt':
        tmp = 'python'
    else:
        tmp = 'python' + '.'.join(str(i) for i in sys.version_info[:2])
    if subprocess.run([tmp, '-m', 'pip', 'install', '-r', 'requirements.txt']).returncode == 0:
        sys.exit('\x1b[1m\x1b[92m' + '[+] dependencies installed\nrun the program again'.title().center(os.get_terminal_size().columns))
    elif subprocess.run(['pip3', 'install', '-r', 'requirements.txt']).returncode == 0:
        sys.exit('\x1b[1m\x1b[92m' + '[+] dependencies installed\nrun the program again'.title().center(os.get_terminal_size().columns))
    else:
        sys.exit('\x1b[1m\x1b[31m' + '[!] something error occured while installing dependencies\n maybe pip isn\'t installed or requirements.txt file not available?'.title().center(os.get_terminal_size().columns))
PY_VER = 'python' + '.'.join(str(i) for i in sys.version_info[:2])
BLU = colorama.Style.BRIGHT + colorama.Fore.BLUE
CYA = colorama.Style.BRIGHT + colorama.Fore.CYAN
GRE = colorama.Style.BRIGHT + colorama.Fore.GREEN
YEL = colorama.Style.BRIGHT + colorama.Fore.YELLOW
RED = colorama.Style.BRIGHT + colorama.Fore.RED
MAG = colorama.Style.BRIGHT + colorama.Fore.MAGENTA
LIYEL = colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX
LIRED = colorama.Style.BRIGHT + colorama.Fore.LIGHTRED_EX
LIMAG = colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX
LIBLU = colorama.Style.BRIGHT + colorama.Fore.LIGHTBLUE_EX
LICYA = colorama.Style.BRIGHT + colorama.Fore.LIGHTCYAN_EX
LIGRE = colorama.Style.BRIGHT + colorama.Fore.LIGHTGREEN_EX
CLEAR = 'cls' if os.name == 'nt' else 'clear'
COLORS = BLU, CYA, GRE, YEL, RED, MAG, LIYEL, LIRED, LIMAG, LIBLU, LICYA, LIGRE
fonts = ['basic', 'o8', 'cosmic', 'graffiti', 'chunky', 'epic', 'poison', 'doom', 'avatar']
colorama.init(autoreset=True)

def marsh_enc(**kwargs):
    sel_cyph = random.choice((lzma, gzip, bz2, binascii, zlib))
    source_marshal = marshal.dumps(compile(kwargs['source'], 'Py-Fuscate', 'exec'))
    if sel_cyph is binascii:
        cyph_compressed = binascii.b2a_base64(source_marshal)
    else:
        cyph_compressed = sel_cyph.compress(source_marshal)
    if sel_cyph is binascii:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(binascii.a2b_base64(%s)))'%cyph_compressed
    else:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(%s.decompress(%s)))'%(sel_cyph.__name__, cyph_compressed)

def logo():
    os.system(CLEAR)
    font = random.choice(fonts)
    color1 = random.choice(COLORS)
    color2 = random.choice(COLORS)
    while color1 == color2:
        color2 = random.choice(COLORS)
    print(color1 + '_' * os.get_terminal_size().columns, end='\n'*2)
    print(color2 + pyfiglet.figlet_format('Py\nFuscate', font=font, justify='center', width=os.get_terminal_size().columns), end='')
    print(color1 + '_' * os.get_terminal_size().columns, end='\n'*2)

def parse_args():
    parser = argparse.ArgumentParser(epilog='example: python3 py_fuscate.py -i myprogram.py -o pyprogram_encoded.py -s 100',
                                     description='obfuscate python programs'.title())
    parser._optionals.title = "syntax".title()
    parser.add_argument('-i', '--input', type=str, help='input file name'.title(), required=True)
    parser.add_argument('-o', '--output', type=str, help='output file name'.title(), required=True)
    parser.add_argument('-s', '--strong', type=int,
                        help='strengthness of obfuscation. 100 recomended'.title(), required=True)
    return parser.parse_args()

def check_update():
    global LATEST_VER
    LATEST_VER = requests.get('https://raw.githubusercontent.com/Sl-Sanda-Ru/Py-Fuscate/main/.version').text.strip()
    with open('.version') as version:
        if version.read().strip() != LATEST_VER:
            return True
        else:
            return False

def update(latest_ver):
    if '.git' in os.listdir():
        subprocess.run(['git', 'stash', '&&', 'git', 'pull'])
    else:
        latest_source = requests.get('https://raw.githubusercontent.com/Sl-Sanda-Ru/Py-Fuscate/main/py_fuscate.py').content
        with open('py_fuscate.py', 'wb') as file:
            file.write(latest_source)
        with open('.version', 'w') as file:
            file.write(LATEST_VER)

def main():
    args = parse_args()
    if check_update():
        print(RED + '\t[!] update available'.title().center(os.get_terminal_size().columns))
        print(LIGRE + '\t[+] updating...'.title().center(os.get_terminal_size().columns))
        update(latest_ver)
        sys.exit(LIGRE + '\t[+] successfully updated...\n\t run the program again'.title().center(os.get_terminal_size().columns))
    print(random.choice(COLORS) + '\t[+] encoding '.title() + args.input)
    encoded_pro = ''
    with tqdm.tqdm(total=args.strong) as pbar:
        for i in range(args.strong):
            if i == 0:
                encoded_pro = marsh_enc(source=open(args.input).read())
            else:
                encoded_pro = marsh_enc(source=marsh_enc(source=encoded_pro))
            time.sleep(0.1)
            pbar.update(1)
    with open(args.output, 'w') as file:
        file.write(f'# Encoded By Py-Fuscate\n# https://github.com/Sl-Sanda-Ru/Py-Fuscate\n# Make Sure You\'re Running The Program With {PY_VER} Otherwise It May Crash\n# To Check Your Python Version Run "python -V" Command\ntry:\n\t{encoded_pro}\nexcept KeyboardInterrupt:\n\tpass')
    print(LIGRE + '\t[+] encoding successful!\n\tsaved as '.title() + args.output)
if __name__ == '__main__':
    logo()
    main()
