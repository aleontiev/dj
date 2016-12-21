# -*- mode: python -*-
import os
block_cipher = None

ROOT = '/Users/ant/code/django-cli'
DATA_DIR = 'django_cli/blueprints'

def get_files(directory):
    for root, dirs, files in os.walk(directory):
        search = []
        for file in search:
            file = os.path.join(root, file)
            yield file

def mount_datas(root, data_dir):
    files = get_files(os.path.join(root, data_dir))
    result = []
    for file in files:
        dir = os.path.dirname(file).replace(root, '')
        file = file.replace(root, '')
        result.append((file, dir))

a = Analysis(['django-cli.py'],
             pathex=[ROOT],
             binaries=None,
             datas=mount_datas(ROOT, DATA_DIR),
             hiddenimports=['setuptools', 'inflection'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='django-cli',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='django-cli')
