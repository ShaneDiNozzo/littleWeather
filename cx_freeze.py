import sys
from cx_Freeze import setup, Executable

setup(
    name = "Little Weather",
    version = "0.5",
    description = "A little app that show the Weather informations of a given city",
    executables = [Executable("idojaras_logic.py", base = "Win32GUI")])