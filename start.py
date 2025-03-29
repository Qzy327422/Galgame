import os
import runpy

pages_path = os.path.join('settings', 'pages.ini')

if os.path.exists(pages_path):
    with open(os.path.join('settings', 'pages.ini'), 'r', encoding='utf-8') as pages:
        pages1 = pages.readline()
        if '1' in pages1:
            print('启动模式1')
            runpy.run_path(os.path.join('galgame.py'))
        if '2' in pages1:
            print('启动模式2')
            runpy.run_path(os.path.join('galgame_pages_mode2.py'))

else:
    pages_path_return = 1
    print('no pages path')
    with open(os.path.join('settings', 'pages.ini'), 'w', encoding='utf-8') as no_pages_path:
        no_pages_path.write(str(1))
        runpy.run_path(os.path.join('galgame.py'))



