pyinstaller ^
	-i icons\BindControl.ico ^
	--onefile ^
	--noconsole ^
	--noconfirm ^
	--clean ^
	--add-data icons;icons ^
	--add-data Help;Help ^
	--exclude-module _bz2 ^
	--exclude-module _ctypes ^
	--exclude-module _decimal ^
	--exclude-module _hashlib ^
	--exclude-module _lzma ^
	--exclude-module _socket ^
	--exclude-module _ssl ^
	BindControl.py
