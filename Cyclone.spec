# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['sol_rng_tracker/main.py'],
    pathex=['C:/Users/vanka/Documents/Cyclone'],
    binaries=[],
    datas=[
        ('sol_rng_tracker/config.json', '.'),
        ('sol_rng_tracker/accounts.json', '.'),
        ('sol_rng_tracker/biomes.json', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Cyclone',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:/Users/vanka/Documents/Cyclone/assets/cyclone.ico'],
)
