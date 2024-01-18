@echo off

for /f %%i in ('git describe --tags') do set VERSION=%%i

echo %VERSION% > version.txt

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
7z a BindControl-%VERSION%-windows.zip BindControl
rmdir /s /q BindControl
cd ..
