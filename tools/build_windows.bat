@echo off

for /f %%i in ('git describe --tags') do set VERSION=%%i

echo %VERSION% > version.txt

py tools\zip_icons.py

pyinstaller ^
	-i icons\BindControl.ico ^
	--noconsole ^
	--noconfirm ^
	--clean ^
	--add-data=icons/Icons.zip;icons/ ^
	--add-data=icons/BindControl.ico;icons/ ^
	--add-data=Help;Help ^
	--add-data=version.txt;. ^
	--add-data=UI/PowerBinderCommand;PowerBinderCommand ^
	--add-data=UI/BindWizard;BindWizard ^
	--exclude-module _bz2 ^
	--exclude-module _ctypes ^
	--exclude-module _decimal ^
	--exclude-module _hashlib ^
	--exclude-module _lzma ^
	--exclude-module _ssl ^
	--hidden-import UI.IncarnateBox ^
	BindControl.py

cd dist
7z a BindControl-%VERSION%-windows.zip BindControl
rmdir /s /q BindControl
cd ..
