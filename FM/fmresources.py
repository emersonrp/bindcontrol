import wx

# Overall menu styles
StyleDefault = 0
StyleXP      = 1

# Button styles
BU_EXT_XP_STYLE = 1
BU_EXT_LEFT_ALIGN_STYLE = 4
BU_EXT_CENTER_ALIGN_STYLE = 8
BU_EXT_RIGHT_ALIGN_STYLE = 16
BU_EXT_RIGHT_TO_LEFT_STYLE = 32

# Control state
ControlPressed = 0
ControlFocus = 1
ControlDisabled = 2
ControlNormal = 3

# FlatMenu styles
FM_OPT_IS_LCD = 1
""" Use this style if your computer uses a LCD screen. """
FM_OPT_MINIBAR = 2
""" Use this if you plan to use the toolbar only. """
FM_OPT_SHOW_CUSTOMIZE = 4
""" Show "customize link" in the `More` menu, you will need to write your own handler. See demo. """
FM_OPT_SHOW_TOOLBAR = 8
""" Set this option is you are planning to use the toolbar. """

# Control status
ControlStatusNoFocus = 0
ControlStatusFocus = 1
ControlStatusPressed = 2

# HitTest constants
NoWhere = 0
MenuItem = 1
ToolbarItem = 2
DropDownArrowButton = 3

MENU_HT_NONE = 0
MENU_HT_ITEM = 1
MENU_HT_SCROLL_UP = 2
MENU_HT_SCROLL_DOWN = 3

SPACER = 12
MARGIN = 3
SEPARATOR_WIDTH = 12
SCROLL_BTN_HEIGHT = 20

CS_DROPSHADOW = 0x00020000

# HitTest results
IMG_OVER_IMG = 0
IMG_OVER_PIN = 1
IMG_OVER_EW_BORDER = 2
IMG_NONE = 3

arrow_up = b'BM\xf6\x00\x00\x00\x00\x00\x00\x00v\x00\x00\x00(\x00\x00\x00\x10\x00\x00\
\x00\x10\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x80\x00\x00\x00\x12\x0b\x00\x00\x12\
\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x80\x80\x00\
\x00w\xfcM\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00""""""""""""""""""""""""""""""""""\x00\x00\x00\x02""""\x11\x11\
\x11\x12""""""""""""\x00\x00\x00\x02""""\x10\x00\x00\x12""""!\x00\x01""""""\x10\x12""""""!\
""""""""""""""""""""""""""""""""""""'


arrow_down = b'BM\xf6\x00\x00\x00\x00\x00\x00\x00v\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00\
\x10\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x0b\x00\x00\x12\x0b\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x80\x80\x00\x00w\
\xfcM\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00"""""""""""""""""""""""""""""""""""!"""""""\x10\x12"""""!\x00\x01\
"""""\x10\x00\x00\x12""""\x00\x00\x00\x02""""""""""""\x11\x11\x11\x12""""\x00\x00\x00\x02\
""""""""""""""""""""""""""""""""""'

menu_up_arrow_xpm = [b"16 16 2 1",
                  b". c Black",
                  b"  c White",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"       .        ",
                  b"      ...       ",
                  b"     .....      ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                "]


menu_down_arrow_xpm = [b"16 16 2 1",
                  b". c Black",
                  b"  c White",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"     .....      ",
                  b"      ...       ",
                  b"       .        ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                ",
                  b"                "]


def getMenuUpArrowBitmap():
    bmp = wx.Bitmap(menu_up_arrow_xpm)
    bmp.SetMask(wx.Mask(bmp, wx.WHITE))
    return bmp

def getMenuDownArrowBitmap():
    bmp = wx.Bitmap(menu_down_arrow_xpm)
    bmp.SetMask(wx.Mask(bmp, wx.WHITE))
    return bmp
