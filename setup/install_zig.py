#!/usr/bin/env python3
import os
import requests
import platform
import subprocess


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename


def install(fname):
    dirname = '/usr/local/zig/'+fname.split('.tar')[0]
    if not os.path.exists("/usr/local/zig"):
        os.makedirs("/usr/local/zig")
    subprocess.run(["sudo", "tar", "-C", "/usr/local/zig", "-xf", fname])
    if os.path.exists('/usr/local/zig/current'):
        subprocess.run(["sudo", "rm", "/usr/local/zig/current"])
    subprocess.run(["sudo", "ln", "-s", dirname, "/usr/local/zig/current"])

def get_url(target_version='master'):
    platstr = f'{platform.machine()}-{platform.system().lower()}'
    r = requests.get('https://ziglang.org/download/index.json')

    zigs = r.json()

    for k in zigs.keys():
        v = zigs[k]
        if platstr in v:
            print(k)
            if 'version' in v:
                print('\t'+v['version'])
            print('\t'+v['date'])
            print('\t'+v[platstr]['tarball'])
            if k == target_version:
                return v[platstr]['tarball']


url = get_url()
local_f = download_file(url)
install(local_f)
os.remove(local_f)

