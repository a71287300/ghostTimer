import os
import sys
from PyInstaller.__main__ import run

if __name__ == '__main__':
    main_script = 'main.py'
    additional_files = ['config.ini', 'ghostAlert.mp3']

    sys.argv = [
        'pyinstaller',
        '--onefile',
        '--windowed',  # 如果你的应用是GUI应用
        f'--name=貓頭計時器',
        f'--add-data={main_script};.',  # 主Python文件
        *[f'--add-data={file};.' for file in additional_files]  # 其他文件
    ]

    run()
