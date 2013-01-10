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
    py_modules=['imgv', 'buttons', 'cfg', 'confirm', 'cursor', 'dir_nav',
                'downloader', 'edit', 'effect_melt', 'error_box',
                'error_screen', 'exif', 'file_master', 'filter_files', 'four',
                'gl', 'handle_keyboard', 'help', 'hide', 'img_screen',
                'img_surf', 'input_box', 'list_images', 'load_img',
                'main_menu', 'movie_player', 'open_url', 'pan', 'playlist',
                'randomizer', 'refresh', 'res', 'rm_img', 'rotate',
                'screensaver', 'show_message', 'slideshow', 'status_bar',
                'thumb', 'transitional', 'usr_event', 'verbose', 'wallpaper',
                'zoom'],
    url='https://github.com/rkulla/imgv',
    license='LICENSE.txt',
    description='Cross-platform Image Viewer',
    entry_points={
        'console_scripts': ['imgv = imgv:main'],
    },
)
