# pyinstaller cli.py --onefile -w --name pyrss.exe --add-data "TimeTracker.ui;TimeTracker.ui" --add-data "edit_charge_codes.ui;edit_charge_codes.ui"

$arguments = 'cli.py',
             '-w',
             '--noconfirm',
			 '--clean',
			 '--name',
			 'pyrss',
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
			 
#pyinstaller cli.py -w --name pyrss.exe ^
#    --add-data "ad_filter_dialog.ui;." ^
#    --add-data "FeedPropertiesDlg.ui;." ^
#    --add-data "filter_dialog.ui;." ^
#    --add-data "filter_manager_dialog.ui;." ^
#    --add-data "language_filter_dialog.ui;." ^
#    --add-data "NewFeedDlg.ui;." ^
#    --add-data "PrefsDlg.ui;." ^
#    --add-data "PurgeDlg.ui;." ^
#    --add-data "PyRssReaderWindow.ui;."

pyinstaller $arguments 2>&1 > .\pyinstaller-build.log
