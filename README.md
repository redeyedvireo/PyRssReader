# pyrssreader
A Python RSS Reader

To run:
`python pyrssreader.py`


## Installing Dependencies

First, create a virtual environment:

`py -m venv venv`

Then, activate it:

`.\venv\Scripts\activate`

Then install dependencies.

#### Pyside6
`pip install Pyside6`

#### lxml
`pip install lxml`

#### Dateutil
`pip install python-dateutil`

#### Cachetools
`pip install cachetools`

#### Requests  (used in Pocket access):
`pip install requests`

#### Beautiful Soup 4
`pip install beautifulsoup4`

#### Feedparser
`pip install feedparser`

#### PyInstaller
`pip install pyinstaller`

#### Building an Executable
To build exe file, invoke the `build-exe.ps1` script, from a command-line or PowerShell terminal window, from the source directory.  Note that on Windows 11, it might be necessary to add an exclusion to Windows security, for the `build` and `dist` directories.  For more information, see: [the Microsoft documentation](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26#ID0EBF=Windows_11)