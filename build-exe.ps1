# This wraps PyRssReader into an executable file.
#
# This article was helpful:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/
#
# In particular, if building fails, or if the resulting executable does not execute, ensure that PyInstaller is up to date:
# pip install --upgrade PyInstaller pyinstaller-hooks-contrib
#
# If the application has strange problems, like the UI is empty, try adding the --console flag, which will show the console window,
# which allows Python errors to be shown.

$arguments = 'cli.py',
             '-w',
             '--noconfirm',
						'--clean',
						'--name',
						'PyRSSReader',
						'--icon',
						'Resources/RssReader.ico',
						'--add-data',
						'./Resources/;Resources'


pyinstaller $arguments 2>&1 > .\pyinstaller-build.log

# Zip the output directory
# 7z a -tzip dist\pyrss.zip dist\pyrss