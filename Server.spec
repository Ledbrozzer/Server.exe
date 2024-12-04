# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app\\model\\Server.py'],
    pathex=[],
    binaries=[],
    datas=[('app/view/index.html', 'view'), ('app/view/css', 'view/css'), ('app/view/js', 'view/js'), ('app/model/armazenamento', 'armazenamento')],
    hiddenimports=['pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.timestamps', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.tslibs.nattype', 'pandas._libs.tslibs.timezones'],
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
    name='Server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
