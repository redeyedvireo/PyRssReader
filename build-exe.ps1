# This wraps PyRssReader into an executable file.

$arguments = 'cli.py',
             '-w',
             '--noconfirm',
			 '--clean',
			 '--name',
			 'pyrss',
			 '--icon',
			 'Resources/RssReader.ico',
			 '--add-data',
			 'ad_filter_dialog.ui;.',
			 '--add-data',
			 'FeedPropertiesDlg.ui;.',
			 '--add-data',
			 'filter_dialog.ui;.',
			 '--add-data',
			 'filter_manager_dialog.ui;.',
			 '--add-data',
			 'language_filter_dialog.ui;.',
			 '--add-data',
			 'NewFeedDlg.ui;.',
			 '--add-data',
			 'PrefsDlg.ui;.',
			 '--add-data',
			 'PurgeDlg.ui;.',
			 '--add-data',
			 'PyRssReaderWindow.ui;.',
			 '--add-binary',
			 'Resources/AppIcon.png;Resources',
			 '--add-data',
			 'Resources/AppIcon.svg;Resources',
			 '--add-binary',
			 'Resources/Audio Enclosure.png;Resources',
			 '--add-data',
			 'Resources/completeHtmlDocument.html;Resources',
			 '--add-binary',
			 'Resources/edit.png;Resources',
			 '--add-data',
			 'Resources/feedHeader.html;Resources',
			 '--add-binary',
			 'Resources/hourglass.png;Resources',
			 '--add-binary',
			 'Resources/minus.png;Resources',
			 '--add-data',
			 'Resources/pagestyle.css;Resources',
			 '--add-binary',
			 'Resources/Paper Clip.png;Resources',
			 '--add-data',
			 'Resources/Paper Clip.svg;Resources',
			 '--add-binary',
			 'Resources/plus.png;Resources',
			 '--add-binary',
			 'Resources/pocket.png;Resources',
			 '--add-binary',
			 'Resources/RssReader.ico;Resources',
			 '--add-binary',
			 'Resources/star.png;Resources'
			 

pyinstaller $arguments 2>&1 > .\pyinstaller-build.log

# Zip the output directory
7z a -tzip dist\pyrss.zip dist\pyrss