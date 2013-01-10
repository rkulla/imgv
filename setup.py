from setuptools import setup
from glob import glob
import os

pjoin = os.path.join

setup(
    name='imgv',
    version='3.1.8',
    author='Ryan Kulla',
    author_email='rkulla@gmail.com',
    package_dir={'': 'imgv'},
    data_files=[('data', glob(pjoin('data', '*'))),
                ('', ['imgv.conf'])],
    py_modules=[os.path.basename(os.path.splitext(i)[0])
                for i in glob(pjoin('imgv', '*.py'))],
    url='https://github.com/rkulla/imgv',
    license='LICENSE.txt',
    description='Cross-platform Image Viewer',
    entry_points={
        'console_scripts': ['imgv = imgv:main'],
    },
)
