# @author: Bezmican Zehir | LinkedIn: bezmicanzehir | IG: @bayonuc
# This file converts .py scripts into Executeable file

from cx_Freeze import setup, Executable

base = None    

executables = [Executable("YourMainThreadHere.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "<Your Executeable Name Here>",
    options = options,
    version = "<1.1>",
    description = '',
    executables = executables
)