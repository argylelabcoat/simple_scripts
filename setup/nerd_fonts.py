#!/usr/bin/python3

import requests
import re, os, shlex, subprocess
from urllib.parse import urlparse
from zipfile import ZipFile
from pathlib import Path
home = str(Path.home())

def ensure_dir(dirpath):
    dirpath = os.path.join(home, dirpath)
    directory = os.path.dirname(dirpath)
    if not os.path.exists(dirpath):
        print("dir not found: %s"%dirpath)
        os.makedirs(dirpath)
    return dirpath

def runCmd(cmd, cwd=None, failhard = True):
    value = None
    cmdarr = shlex.split(cmd)
    if None != cwd:
        cwd = os.path.join(home, cwd)
    with subprocess.Popen(cmdarr, cwd=cwd) as proc:
        value = proc.wait()
    if failhard and value != 0:
        exit(value)
    return value

def InstallNerdFonts():
    url_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    font_regex = re.compile('/ryanoasis/nerd-fonts/releases/download/[a-zA-Z0-9_./]+.zip')

    url = 'https://github.com/ryanoasis/nerd-fonts/releases/latest'
    r = requests.get(url, allow_redirects=True)

    fontcache = ensure_dir('.fonts')
    fontlocalcache = ensure_dir('.local/share/fonts')

    for substr in font_regex.finditer(r.text):
        url ='https://github.com'+substr.group()
        parsed = urlparse(url)
        fname = os.path.basename(parsed.path)
        r = requests.get(url, allow_redirects=True)
        open(fname, 'wb').write(r.content)
        with ZipFile(fname, 'r') as zipObj:
            zipObj.extractall(fontcache)
        os.remove(fname)
        
    runCmd('fc-cache -fv')

if __name__ == '__main__':
    InstallNerdFonts()
