from cx_Freeze import setup, Executable

exe = Executable(
    script='main.pyw',
    base='Win32GUI',
    targetName='SteamMover.exe',
    includes=['atexit, PySide.QtNetwork, icons_rc'],
    shortcutName='SteamMover',
    shortcutDir='ProgramMenuFolder'
)

setup(
    name='SteamMover',
    version='0.9',
    packages=['ui', 'resources'],
    url='',
    license='',
    author='Robin L Siebler',
    author_email='',
    description='A utility to move Steam Games',
    options={"build_exe": {'icon': r'resources\Steam.ico',
                           'include_files': ('.\\imageformats', '.\\imageformats')}},
    executables=[exe]
)
