
import os
from pathlib import Path


icon_file = "📄"
icon_folder = "📁"
icon_openfolder = "📂"
icon_lowerleftcorner = "└"
icon_teeright = "├"
icon_vertical = "│"
icon_horizontal = "─"



def print_tree(d, indent=0, prefix=""):
    indentStr = ""
    pathicon = ""
    indenticon = ""
    for idx in range(len(d)):
        item = d[idx]
        if indent > 0:
            if idx < len(d) - 1:
                pathicon = icon_teeright
                indenticon = icon_vertical
            else:
                pathicon = icon_lowerleftcorner
                indenticon = " "
        indentStr = prefix + pathicon + icon_horizontal * indent
        indentPrefix = prefix + indenticon + " " * indent 
        entry = item.popitem()
        print(f"{indentStr}{icon_folder} {entry[0]}")
        print_tree(entry[1], indent+1, indentPrefix)


def print_dir(path=".", indent=0, prefix=""):
    d = os.listdir(path)
    indentStr = ""
    pathicon = ""
    indenticon = ""
    for idx in range(len(d)):
        item = d[idx]
        fname = os.path.join(path, item)
        isdir = os.path.isdir(fname)

        if isdir:
            if indent > 0:
                icon = icon_folder
            else:
                icon = icon_openfolder
        else:
            icon = icon_file

        if indent > 0:
            if idx < len(d) - 1:
                pathicon = icon_teeright
                indenticon = icon_vertical
            else:
                pathicon = icon_lowerleftcorner
                indenticon = " "

        indentStr = prefix + pathicon + icon_horizontal * indent
        indentPrefix = prefix + indenticon + " " * indent 
        print(f"{indentStr}{icon} {item}")
        
        if isdir:
            print_dir(fname, indent+2, indentPrefix)




tree=[{
    "dirA":[
        {"dirB":[
            {"dir1":[
                {"dir4":[]}
                 ]},
            {"dir3":[]}
            ]},
        {"dirC":[
            {"dirD":[]}
            ]},
        {"dirE":[
            {"dir2":[]}
            ]}
        ]},
    ]

print_tree(tree)
print_dir()
