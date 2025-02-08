# This wraps PyRssReader into an executable file.
#
# This article was helpful:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/
#
# In particular, if building fails, or if the resulting executable does not execute, ensure that PyInstaller is up to date:
# pip install --upgrade PyInstaller pyinstaller-hooks-contrib

$arguments = 'cli.py',
             '-w',
             '--noconfirm',
						'--clean',
						'--name',
						'PyRSS',
						'--icon',
						'Resources/RssReader.ico',
						'--add-data',
						'./Resources/;Resources',
						'--add-data',
            './*.ui;.'


pyinstaller $arguments 2>&1 > .\pyinstaller-build.log

# Zip the output directory
# 7z a -tzip dist\pyrss.zip dist\pyrss