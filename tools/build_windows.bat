@echo off

for /f %%i in ('git describe --tags') do set VERSION=%%i

echo %VERSION% > version.txt

pyinstaller ^
	-i icons\BindControl.ico ^
	--noconsole ^
	--noconfirm ^
	--clean ^
	--add-data icons;icons ^
	--add-data Help;Help ^
	--add-data version.txt;. ^
	--exclude-module _bz2 ^
	--exclude-module _ctypes ^
	--exclude-module _decimal ^
	--exclude-module _hashlib ^
	--exclude-module _lzma ^
	--exclude-module _socket ^
	--exclude-module _ssl ^
	BindControl.py

cd dist
7z a BindControl-%VERSION%-windows.zip BindControl
rmdir /s /q BindControl
cd ..
