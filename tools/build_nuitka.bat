python -m nuitka ^
	--standalone ^
	--remove-output ^
	--windows-icon-from-ico=icons\BindControl.ico ^
	--disable-console ^
	--include-data-dir=icons=icons ^
	--include-data-dir=Help=Help ^
	--output-filename=BindControl.exe ^
	--output-dir=dist ^
	BindControl.py

cd dist
ren BindControl.dist BindControl
7z a BindControl.zip BindControl
cd ..
