# -*- mode: python -*-
import os

ROOT = '/Users/ant/code/dj'
BLUEPRINTS = 'djay/blueprints'
HIDDEN_IMPORTS = ['setuptools', 'setuptools.msvc', 'inflection']

block_cipher = None

def get_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file = os.path.join(root, file)
            yield file

def mount_datas(root, dir):
    result = []
    files = get_files(dir)
    for file in files:
        file = file.replace(root, '')
        result.append((file, os.path.dirname(file)))
    return result


a = Analysis(['dj.exe.py'],
             pathex=[ROOT],
             binaries=None,
             datas=mount_datas(ROOT, BLUEPRINTS),
             hiddenimports=HIDDEN_IMPORTS,
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
          name='dj.exe',
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
               name='dj.exe')
