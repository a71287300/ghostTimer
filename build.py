import sys
from PyInstaller.__main__ import run

if __name__ == '__main__':
    main_script = 'main.py'
    sys.argv = [
        'pyinstaller',
        '-F',
        '-c',  # 如果你的应用是GUI应用
        f'--name=貓頭計時器',
        '--icon=cat.ico',
        '--noconsole',
        main_script
    ]

    run()
