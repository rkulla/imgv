# setup.py
# usage: python setup.py py2exe --packages encodings --icon imgv-icon.ico -O2 --windows
from distutils.core import setup
import py2exe

setup(name="imgv",
      scripts=["imgv.py"],
)

