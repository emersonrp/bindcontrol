# --------------------------------------------------------------------------------- #
# FLATMENU wxPython IMPLEMENTATION
#
# Andrea Gavana, @ 03 Nov 2006
# Latest Revision: 27 Dec 2012, 21.00 GMT
#
# TODO List
#
# 1. Work is still in progress, so other functionalities may be added in the future;
# 2. No shadows under MAC, but it may be possible to create them using Carbon.
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@maerskoil.com
# andrea.gavana@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# Tags:     phoenix-port, py3-port, unittest, documented
# --------------------------------------------------------------------------------- #

__docformat__ = "epytext"
__version__ = "1.0"

import wx
import math
import html

import wx.lib.colourutils as colourutils

import io

from .artmanager import ArtManager, DCSaver
from .fmresources import *

# FlatMenu styles
FM_OPT_IS_LCD = 1
""" Use this style if your computer uses a LCD screen. """
FM_OPT_MINIBAR = 2
""" Use this if you plan to use the toolbar only. """
FM_OPT_SHOW_CUSTOMIZE = 4
""" Show "customize link" in the `More` menu, you will need to write your own handler. See demo. """
FM_OPT_SHOW_TOOLBAR = 8
""" Set this option is you are planning to use the toolbar. """

# Define a translation string
_ = wx.GetTranslation

wxEVT_FLAT_MENU_DISMISSED = wx.NewEventType()
wxEVT_FLAT_MENU_SELECTED = wx.wxEVT_COMMAND_MENU_SELECTED
wxEVT_FLAT_MENU_ITEM_MOUSE_OVER = wx.NewEventType()
wxEVT_FLAT_MENU_ITEM_MOUSE_OUT = wx.NewEventType()

EVT_FLAT_MENU_DISMISSED = wx.PyEventBinder(wxEVT_FLAT_MENU_DISMISSED, 1)
""" Used internally. """
EVT_FLAT_MENU_SELECTED = wx.PyEventBinder(wxEVT_FLAT_MENU_SELECTED, 2)
""" Fires the wx.EVT_MENU event for :class:`FlatMenu`. """
EVT_FLAT_MENU_RANGE = wx.PyEventBinder(wxEVT_FLAT_MENU_SELECTED, 2)
""" Fires the wx.EVT_MENU event for a series of :class:`FlatMenu`. """
EVT_FLAT_MENU_ITEM_MOUSE_OUT = wx.PyEventBinder(wxEVT_FLAT_MENU_ITEM_MOUSE_OUT, 1)
""" Fires an event when the mouse leaves a :class:`FlatMenuItem`. """
EVT_FLAT_MENU_ITEM_MOUSE_OVER = wx.PyEventBinder(wxEVT_FLAT_MENU_ITEM_MOUSE_OVER, 1)
""" Fires an event when the mouse enters a :class:`FlatMenuItem`. """


def GetAccelIndex(label):
    """
    Returns the mnemonic index of the label and the label stripped of the ampersand mnemonic
    (e.g. 'lab&el' ==> will result in 3 and labelOnly = label).

    :param string `label`: a string possibly containing an ampersand.
    """

    indexAccel = 0
    while True:
        indexAccel = label.find("&", indexAccel)
        if indexAccel == -1:
            return indexAccel, label
        if label[indexAccel:indexAccel+2] == "&&":
            label = label[0:indexAccel] + label[indexAccel+1:]
            indexAccel += 1
        else:
            break

    labelOnly = label[0:indexAccel] + label[indexAccel+1:]

    return indexAccel, labelOnly


# ---------------------------------------------------------------------------- #
# Class FMRendererMgr
# ---------------------------------------------------------------------------- #

class FMRendererMgr(object):

    def __new__(cls, *p, **k):
        if not '_instance' in cls.__dict__:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        """ Default class constructor. """

        # If we have already initialized don't do it again. There is only one
        # FMRendererMgr process-wide.

        if hasattr(self, '_alreadyInitialized'):
            return

        self._alreadyInitialized = True

        self._currentTheme = StyleDefault
        self._renderers = []
        self._renderers.append(FMRenderer())

    def GetRenderer(self):
        """ Returns the current theme's renderer. """

        return self._renderers[self._currentTheme]

# ---------------------------------------------------------------------------- #
# Class FMRenderer
# ---------------------------------------------------------------------------- #

class FMRenderer(object):
    """
    Base class for the :class:`FlatMenu` renderers. This class implements the common
    methods of all the renderers.
    """

    def __init__(self):
        """ Default class constructor. """

        self.separatorHeight = 5
        self.scrollBarButtons = False   # Display scrollbar buttons if the menu doesn't fit on the screen
                                        # otherwise default to up and down arrow menu items

        self.itemTextColourDisabled = ArtManager.Get().LightColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT), 30)

        # Background Colours
        self.menuFaceColour     = wx.WHITE
        self.menuBarFaceColour  = ArtManager.Get().LightColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE), 80)

        self.menuBarFocusFaceColour     = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.menuBarFocusBorderColour   = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.menuBarPressedFaceColour   = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.menuBarPressedBorderColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        self.menuFocusFaceColour     = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.menuFocusBorderColour   = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.menuPressedFaceColour   = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.menuPressedBorderColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        self.buttonFaceColour          = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.buttonBorderColour        = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.buttonFocusFaceColour     = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.buttonFocusBorderColour   = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.buttonPressedFaceColour   = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.buttonPressedBorderColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        self._bitmaps = {}
        bmp = self.ConvertToBitmap(arrow_down, alpha=None)
        bmp.SetMask(wx.Mask(bmp, wx.Colour(0, 128, 128)))
        self._bitmaps.update({"arrow_down": bmp})

        bmp = self.ConvertToBitmap(arrow_up, alpha=None)
        bmp.SetMask(wx.Mask(bmp, wx.Colour(0, 128, 128)))
        self._bitmaps.update({"arrow_up": bmp})

        self._toolbarSeparatorBitmap = wx.NullBitmap
        self.raiseToolbar = False


    def SetMenuHighlightColour(self,colour):
        """
        Set the colour to highlight focus on the menu.

        :param `colour`: a valid instance of :class:`wx.Colour`.
        """

        self.menuFocusFaceColour    = colour
        self.menuFocusBorderColour  = colour
        self.menuPressedFaceColour     = colour
        self.menuPressedBorderColour   = colour


    def GetColoursAccordingToState(self, state):
        """
        Returns a :class:`wx.Colour` according to the menu item state.

        :param integer `state`: one of the following bits:

         ==================== ======= ==========================
         Item State            Value  Description
         ==================== ======= ==========================
         ``ControlPressed``         0 The item is pressed
         ``ControlFocus``           1 The item is focused
         ``ControlDisabled``        2 The item is disabled
         ``ControlNormal``          3 Normal state
         ==================== ======= ==========================

        """

        # switch according to the status
        if state == ControlFocus:
            upperBoxTopPercent = 95
            upperBoxBottomPercent = 50
            lowerBoxTopPercent = 40
            lowerBoxBottomPercent = 90
            concaveUpperBox = True
            concaveLowerBox = True

        elif state == ControlPressed:
            upperBoxTopPercent = 75
            upperBoxBottomPercent = 90
            lowerBoxTopPercent = 90
            lowerBoxBottomPercent = 40
            concaveUpperBox = True
            concaveLowerBox = True

        elif state == ControlDisabled:
            upperBoxTopPercent = 100
            upperBoxBottomPercent = 100
            lowerBoxTopPercent = 70
            lowerBoxBottomPercent = 70
            concaveUpperBox = True
            concaveLowerBox = True

        else:
            upperBoxTopPercent = 90
            upperBoxBottomPercent = 50
            lowerBoxTopPercent = 30
            lowerBoxBottomPercent = 75
            concaveUpperBox = True
            concaveLowerBox = True

        return upperBoxTopPercent, upperBoxBottomPercent, lowerBoxTopPercent, lowerBoxBottomPercent, \
               concaveUpperBox, concaveLowerBox


    def ConvertToBitmap(self, xpm, alpha=None):
        """
        Convert the given image to a bitmap, optionally overlaying an alpha
        channel to it.

        :param `xpm`: a list of strings formatted as XPM;
        :param `alpha`: a list of alpha values, the same size as the xpm bitmap.
        """

        if alpha is not None:

            img = wx.Bitmap(xpm)
            img = img.ConvertToImage()
            x, y = img.GetWidth(), img.GetHeight()
            img.InitAlpha()
            for jj in range(y):
                for ii in range(x):
                    img.SetAlpha(ii, jj, alpha[jj*x+ii])

        else:

            stream = io.BytesIO(xpm)
            img = wx.Image(stream)

        return wx.Bitmap(img)

    def DrawSeparator(self, dc, xCoord, yCoord, textX, sepWidth):
        """
        Draws a separator inside a :class:`FlatMenu`.

        :param `dc`: an instance of :class:`wx.DC`;
        :param integer `xCoord`: the current x position where to draw the separator;
        :param integer `yCoord`: the current y position where to draw the separator;
        :param integer `textX`: the menu item label x position;
        :param integer `sepWidth`: the width of the separator, in pixels.
        """

        dcsaver = DCSaver(dc)
        sepRect1 = wx.Rect(xCoord + textX, yCoord + 1, sepWidth//2, 1)
        sepRect2 = wx.Rect(xCoord + textX + sepWidth//2, yCoord + 1, sepWidth//2-1, 1)

        artMgr = ArtManager.Get()
        backColour = artMgr.GetMenuFaceColour()
        lightColour = wx.Colour("LIGHT GREY")

        artMgr.PaintStraightGradientBox(dc, sepRect1, backColour, lightColour, False)
        artMgr.PaintStraightGradientBox(dc, sepRect2, lightColour, backColour, False)


    def DrawMenuItem(self, item, dc, xCoord, yCoord, imageMarginX, markerMarginX, textX, rightMarginX, selected=False, backgroundImage=None):
        """
        Draws the menu item.

        :param `item`: a :class:`FlatMenuItem` instance;
        :param `dc`: an instance of :class:`wx.DC`;
        :param integer `xCoord`: the current x position where to draw the menu;
        :param integer `yCoord`: the current y position where to draw the menu;
        :param integer `imageMarginX`: the spacing between the image and the menu border;
        :param integer `markerMarginX`: the spacing between the checkbox/radio marker and
         the menu border;
        :param integer `textX`: the menu item label x position;
        :param integer `rightMarginX`: the right margin between the text and the menu border;
        :param bool `selected`: ``True`` if this menu item is currently hovered by the mouse,
         ``False`` otherwise.
        :param `backgroundImage`: if not ``None``, an instance of :class:`wx.Bitmap` which will
         become the background image for this :class:`FlatMenu`.
        """

        borderXSize = item._parentMenu.GetBorderXWidth()
        itemHeight = item._parentMenu.GetItemHeight()
        menuWidth  = item._parentMenu.GetMenuWidth()

        # Define the item actual rectangle area
        itemRect = wx.Rect(xCoord, yCoord, menuWidth, itemHeight)

        # Define the drawing area
        rect = wx.Rect(xCoord+2, yCoord, menuWidth - 4, itemHeight)

        # Draw the background
        backColour = self.menuFaceColour
        penColour  = backColour
        backBrush = wx.Brush(backColour)
        leftMarginWidth = item._parentMenu.GetLeftMarginWidth()

        if backgroundImage is None:
            pen = wx.Pen(penColour)
            dc.SetPen(pen)
            dc.SetBrush(backBrush)
            dc.DrawRectangle(rect)

        # check if separator
        if item.IsSeparator():
            # Separator is a small grey line separating between menu items.
            sepWidth = xCoord + menuWidth - textX - 1
            self.DrawSeparator(dc, xCoord, yCoord, textX, sepWidth)
            return

        # Keep the item rect
        item._rect = itemRect

        # Get the bitmap base on the item state (disabled, selected ..)
        bmp = item.GetSuitableBitmap(selected)

        # First we draw the selection rectangle
        if selected:
            self.DrawMenuButton(dc, rect.Deflate(1,0), ControlFocus)
            #copy.Inflate(0, menubar._spacer)

        if bmp.IsOk():

            # Calculate the position to place the image
            imgHeight = bmp.GetHeight()
            imgWidth  = bmp.GetWidth()

            if imageMarginX == 0:
                xx = rect.x + (leftMarginWidth - imgWidth)//2
            else:
                xx = rect.x + ((leftMarginWidth - rect.height) - imgWidth)//2 + rect.height

            yy = rect.y + (rect.height - imgHeight)//2
            dc.DrawBitmap(bmp, xx, yy, True)

        # Draw text - without accelerators
        text = item.GetLabel()

        if text:

            font = item.GetFont()
            if font is None:
                font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

            if selected:
                enabledTxtColour = colourutils.BestLabelColour(self.menuFocusFaceColour, bw=True)
            else:
                enabledTxtColour = colourutils.BestLabelColour(self.menuFaceColour, bw=True)

            disabledTxtColour = self.itemTextColourDisabled
            textColour = (item.IsEnabled() and [enabledTxtColour] or [disabledTxtColour])[0]

            if item.IsEnabled() and item.GetTextColour():
                textColour = item.GetTextColour()

            dc.SetFont(font)
            w, h = dc.GetTextExtent(text)
            dc.SetTextForeground(textColour)

            if item._mnemonicIdx != wx.NOT_FOUND:

                # We divide the drawing to 3 parts
                text1 = text[0:item._mnemonicIdx]
                text2 = text[item._mnemonicIdx]
                text3 = text[item._mnemonicIdx+1:]

                w1, dummy = dc.GetTextExtent(text1)
                w2, dummy = dc.GetTextExtent(text2)
                w3, dummy = dc.GetTextExtent(text3)

                posx = xCoord + textX + borderXSize
                posy = (itemHeight - h)//2 + yCoord

                # Draw first part
                dc.DrawText(text1, posx, posy)

                # mnemonic
                if "__WXGTK__" not in wx.Platform:
                    font.SetUnderlined(True)
                    dc.SetFont(font)

                posx += w1
                dc.DrawText(text2, posx, posy)

                # last part
                font.SetUnderlined(False)
                dc.SetFont(font)
                posx += w2
                dc.DrawText(text3, posx, posy)

            else:

                w, h = dc.GetTextExtent(text)
                dc.DrawText(text, xCoord + textX + borderXSize, (itemHeight - h)//2 + yCoord)


        # Now draw accelerator
        # Accelerators are aligned to the right
        if item.GetAccelString():

            accelWidth, accelHeight = dc.GetTextExtent(item.GetAccelString())
            dc.DrawText(item.GetAccelString(), xCoord + rightMarginX - accelWidth, (itemHeight - accelHeight)//2 + yCoord)

        # Check if this item has sub-menu - if it does, draw
        # right arrow on the right margin
        if item.GetSubMenu():
            xx = xCoord + rightMarginX + borderXSize
            rr = wx.Rect(xx, rect.y + 1, rect.height-2, rect.height-2)
            dc.DrawText(html.unescape('&#9656;'), rr.x + 4, rr.y +(rr.height-16)//2)


    def DrawMenuBarButton(self, dc, rect, state):
        """
        Draws the highlight on a :class:`FlatMenuBar`.

        :param `dc`: an instance of :class:`wx.DC`;
        :param `rect`: an instance of :class:`wx.Rect`, representing the button client rectangle;
        :param integer `state`: the button state.
        """

        # switch according to the status
        if state == ControlFocus:
            penColour   = self.menuBarFocusBorderColour
            brushColour = self.menuBarFocusFaceColour
        elif state == ControlPressed:
            penColour   = self.menuBarPressedBorderColour
            brushColour = self.menuBarPressedFaceColour

        dcsaver = DCSaver(dc)
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRectangle(rect)


    def DrawMenuButton(self, dc, rect, state):
        """
        Draws the highlight on a FlatMenu

        :param `dc`: an instance of :class:`wx.DC`;
        :param `rect`: an instance of :class:`wx.Rect`, representing the button client rectangle;
        :param integer `state`: the button state.
        """

        # switch according to the status
        if state == ControlFocus:
            penColour   = self.menuFocusBorderColour
            brushColour = self.menuFocusFaceColour
        elif state == ControlPressed:
            penColour   = self.menuPressedBorderColour
            brushColour = self.menuPressedFaceColour

        dcsaver = DCSaver(dc)
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRectangle(rect)


    def DrawScrollButton(self, dc, rect, state):
        """
        Draws the scroll button

        :param `dc`: an instance of :class:`wx.DC`;
        :param `rect`: an instance of :class:`wx.Rect`, representing the button client rectangle;
        :param integer `state`: the button state.
        """

        if not self.scrollBarButtons:
            return

        colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        colour = ArtManager.Get().LightColour(colour, 30)

        artMgr = ArtManager.Get()

        # Keep old pen and brush
        dcsaver = DCSaver(dc)

        # Define the rounded rectangle base on the given rect
        # we need an array of 9 points for it
        baseColour = colour

        # Define the middle points
        leftPt = wx.Point(rect.x, rect.y + (rect.height / 2))
        rightPt = wx.Point(rect.x + rect.width-1, rect.y + (rect.height / 2))

        # Define the top region
        top = wx.Rect((rect.GetLeft(), rect.GetTop()), rightPt)
        bottom = wx.Rect(leftPt, (rect.GetRight(), rect.GetBottom()))

        upperBoxTopPercent, upperBoxBottomPercent, lowerBoxTopPercent, lowerBoxBottomPercent, \
                            concaveUpperBox, concaveLowerBox = self.GetColoursAccordingToState(state)

        topStartColour = artMgr.LightColour(baseColour, upperBoxTopPercent)
        topEndColour = artMgr.LightColour(baseColour, upperBoxBottomPercent)
        bottomStartColour = artMgr.LightColour(baseColour, lowerBoxTopPercent)
        bottomEndColour = artMgr.LightColour(baseColour, lowerBoxBottomPercent)

        artMgr.PaintStraightGradientBox(dc, top, topStartColour, topEndColour)
        artMgr.PaintStraightGradientBox(dc, bottom, bottomStartColour, bottomEndColour)

        rr = wx.Rect(rect.x, rect.y, rect.width, rect.height)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        frameColour = artMgr.LightColour(baseColour, 60)
        dc.SetPen(wx.Pen(frameColour))
        dc.DrawRectangle(rr)

        wc = artMgr.LightColour(baseColour, 80)
        dc.SetPen(wx.Pen(wc))
        rr.Deflate(1, 1)
        dc.DrawRectangle(rr)


    def DrawButton(self, dc, rect, state, colour=None):
        """
        Draws a button.

        :param `dc`: an instance of :class:`wx.DC`;
        :param `rect`: an instance of :class:`wx.Rect`, representing the button client rectangle;
        :param integer `state`: the button state;
        :param `colour`: if not ``None``, an instance of :class:`wx.Colour` to be used to draw
         the :class:`FlatMenuItem` background.
        """

        # switch according to the status
        if state == ControlFocus:
            if colour is None:
                penColour   = self.buttonFocusBorderColour
                brushColour = self.buttonFocusFaceColour
            else:
                penColour   = colour
                brushColour = ArtManager.Get().LightColour(colour, 75)

        elif state == ControlPressed:
            if colour is None:
                penColour   = self.buttonPressedBorderColour
                brushColour = self.buttonPressedFaceColour
            else:
                penColour   = colour
                brushColour = ArtManager.Get().LightColour(colour, 60)
        else:
            if colour is None:
                penColour   = self.buttonBorderColour
                brushColour = self.buttonFaceColour
            else:
                penColour   = colour
                brushColour = ArtManager.Get().LightColour(colour, 75)

        dcsaver = DCSaver(dc)
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRectangle(rect)

    def DrawMenu(self, flatmenu, dc):
        """
        Draws the menu.

        :param `flatmenu`: the :class:`FlatMenu` instance we need to paint;
        :param `dc`: an instance of :class:`wx.DC`.
        """

        menuRect = flatmenu.GetClientRect()
        menuBmp = wx.Bitmap(menuRect.width, menuRect.height)

        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(menuBmp)

        # colour the menu face with background colour
        backColour = self.menuFaceColour
        penColour  = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNSHADOW)

        backBrush = wx.Brush(backColour)
        pen = wx.Pen(penColour)

        mem_dc.SetPen(pen)
        mem_dc.SetBrush(backBrush)
        mem_dc.DrawRectangle(menuRect)

        backgroundImage = flatmenu._backgroundImage

        if backgroundImage:
            mem_dc.DrawBitmap(backgroundImage, flatmenu._leftMarginWidth, 0, True)

        # draw items
        posy = 3
        nItems = len(flatmenu._itemsArr)

        # make all items as non-visible first
        for item in flatmenu._itemsArr:
            item.Show(False)

        visibleItems = 0
        screenHeight = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        numCols = flatmenu.GetNumberColumns()
        switch, posx, index = 1e6, 0, 0
        if numCols > 1:
            switch = int(math.ceil((nItems - flatmenu._first)/float(numCols)))

        # If we have to scroll and are not using the scroll bar buttons we need to draw
        # the scroll up menu item at the top.
        if not self.scrollBarButtons and flatmenu._showScrollButtons:
            posy += flatmenu.GetItemHeight()

        for nCount in range(flatmenu._first, nItems):

            visibleItems += 1
            item = flatmenu._itemsArr[nCount]
            self.DrawMenuItem(item, mem_dc, posx, posy,
                              flatmenu._imgMarginX, flatmenu._markerMarginX,
                              flatmenu._textX, flatmenu._rightMarginPosX,
                              nCount == flatmenu._selectedItem,
                              backgroundImage=backgroundImage)
            posy += item.GetHeight()
            item.Show()

            if visibleItems >= switch:
                posy = 2
                index += 1
                posx = flatmenu._menuWidth*index
                visibleItems = 0

            # make sure we draw only visible items
            pp = flatmenu.ClientToScreen(wx.Point(0, posy))

            menuBottom = (self.scrollBarButtons and [pp.y] or [pp.y + flatmenu.GetItemHeight()*2])[0]

            if menuBottom > screenHeight:
                break

        if flatmenu._showScrollButtons:
            if flatmenu._upButton:
                flatmenu._upButton.Draw(mem_dc)
            if flatmenu._downButton:
                flatmenu._downButton.Draw(mem_dc)

        dc.Blit(0, 0, menuBmp.GetWidth(), menuBmp.GetHeight(), mem_dc, 0, 0)

# ---------------------------------------------------------------------------- #
# Class FlatMenuEvent
# ---------------------------------------------------------------------------- #

class FlatMenuEvent(wx.PyCommandEvent):
    """
    Event class that supports the :class:`FlatMenu`-compatible event called
    ``EVT_FLAT_MENU_SELECTED``.
    """

    def __init__(self, eventType, eventId=1):
        """
        Default class constructor.

        :param integer `eventType`: the event type;
        :param integer `eventId`: the event identifier.
        """

        wx.PyCommandEvent.__init__(self, eventType, eventId)
        self._eventType = eventType


# ---------------------------------------------------------------------------- #
# Class MenuEntryInfo
# ---------------------------------------------------------------------------- #

class MenuEntryInfo(object):
    """
    Internal class which holds information about a menu.
    """

    def __init__(self, titleOrMenu="", menu=None, state=ControlNormal, cmd=wx.ID_ANY):
        """
        Default class constructor.

        Used internally. Do not call it in your code!

        :param `titleOrMenu`: if it is a string, it represents the new menu label,
         otherwise it is another instance of :class:`wx.MenuEntryInfo` from which the attributes
         are copied;
        :param `menu`: the associated :class:`FlatMenu` object;
        :param integer `state`: the menu item state. This can be one of the following:

         ==================== ======= ==========================
         Item State            Value  Description
         ==================== ======= ==========================
         ``ControlPressed``         0 The item is pressed
         ``ControlFocus``           1 The item is focused
         ``ControlDisabled``        2 The item is disabled
         ``ControlNormal``          3 Normal state
         ==================== ======= ==========================

        :param integer `cmd`: the menu accelerator identifier.
        """

        if isinstance(titleOrMenu, str):

            self._title = titleOrMenu
            self._menu = menu

            self._rect = wx.Rect()
            self._state = state
            if cmd == wx.ID_ANY:
                cmd = wx.NewIdRef()

            self._cmd = cmd             # the menu itself accelerator id

        else:

            self._title = titleOrMenu._title
            self._menu = titleOrMenu._menu
            self._rect = titleOrMenu._rect
            self._state = titleOrMenu._state
            self._cmd = titleOrMenu._cmd

        self._textBmp = wx.NullBitmap
        self._textSelectedBmp = wx.NullBitmap


    def GetTitle(self):
        """ Returns the associated menu title. """

        return self._title


    def GetMenu(self):
        """ Returns the associated menu. """

        return self._menu


    def SetRect(self, rect):
        """
        Sets the associated menu client rectangle.

        :param `rect`: an instance of :class:`wx.Rect`, representing the menu client rectangle.
        """

        self._rect = rect


    def GetRect(self):
        """ Returns the associated menu client rectangle. """

        return self._rect


    def SetState(self, state):
        """
        Sets the associated menu state.

        :param integer `state`: the menu item state. This can be one of the following:

         ==================== ======= ==========================
         Item State            Value  Description
         ==================== ======= ==========================
         ``ControlPressed``         0 The item is pressed
         ``ControlFocus``           1 The item is focused
         ``ControlDisabled``        2 The item is disabled
         ``ControlNormal``          3 Normal state
         ==================== ======= ==========================
        """

        self._state = state


    def GetState(self):
        """
        Returns the associated menu state.

        :see: :meth:`~MenuEntryInfo.SetState` for a list of valid menu states.
        """

        return self._state

# ---------------------------------------------------------------------------- #
# Class ShadowPopupWindow
# ---------------------------------------------------------------------------- #

class ShadowPopupWindow(mcPopupWindow if wx.Platform == '__WXMAC__' else wx.PopupWindow):
    """ Base class for generic :class:`FlatMenu` derived from :class:`PopupWindow`. """

    def __init__(self, parent=None):
        """
        Default class constructor.

        :param `parent`: the :class:`ShadowPopupWindow` parent (typically your main frame).
        """

        if not parent:
            parent = wx.GetApp().GetTopWindow()

        if not parent:
            raise Exception("Can't create menu without parent!")

        wx.PopupWindow.__init__(self, parent)

        # popup windows are created hidden by default
        self.Hide()


#--------------------------------------------------------
# Class FlatMenuButton
#--------------------------------------------------------

class FlatMenuButton(object):
    """
    A nice small class that functions like :class:`wx.BitmapButton`, the reason I did
    not used :class:`wx.BitmapButton` is that on Linux, it has some extra margins that
    I can't seem to be able to remove.
    """

    def __init__(self, menu, up, normalBmp, disabledBmp=wx.NullBitmap, scrollOnHover=False):
        """
        Default class constructor.

        :param `menu`: the parent menu associated with this button, an instance of :class:`FlatMenu`;
        :param bool `up`: ``True`` for up arrow or ``False`` for down arrow;
        :param `normalBmp`: normal state bitmap, an instance of :class:`wx.Bitmap`;
        :param `disabledBmp`: disabled state bitmap, an instance of :class:`wx.Bitmap`.
        """

        self._normalBmp = normalBmp
        self._up = up
        self._parent = menu
        self._pos = wx.Point()
        self._size = wx.Size()
        self._timerID = wx.NewIdRef()
        self._scrollOnHover = scrollOnHover

        if not disabledBmp.IsOk():
            self._disabledBmp = wx.Bitmap(self._normalBmp.ConvertToImage().ConvertToGreyscale())
        else:
            self._disabledBmp = disabledBmp

        self._state = ControlNormal
        self._timer = wx.Timer(self._parent, self._timerID)
        self._timer.Stop()


    def __del__(self):
        """ Used internally. """

        if self._timer:
            if self._timer.IsRunning():
                self._timer.Stop()

            del self._timer


    def Contains(self, pt):
        """ Used internally. """

        rect = wx.Rect(self._pos, self._size)
        if not rect.Contains(pt):
            return False

        return True


    def Draw(self, dc):
        """
        Draws self at rect using dc.

        :param `dc`: an instance of :class:`wx.DC`.
        """

        rect = wx.Rect(self._pos, self._size)
        xx = rect.x + (rect.width - self._normalBmp.GetWidth())//2
        yy = rect.y + (rect.height - self._normalBmp.GetHeight())//2

        self._parent.GetRenderer().DrawScrollButton(dc, rect, self._state)
        dc.DrawBitmap(self._normalBmp, xx, yy, True)


    def ProcessLeftDown(self, pt):
        """
        Handles left down mouse events.

        :param `pt`: an instance of :class:`wx.Point` where the left mouse button was pressed.
        """

        if not self.Contains(pt):
            return False

        self._state = ControlPressed
        self._parent.Refresh()

        if self._up:
            self._parent.ScrollUp()
        else:
            self._parent.ScrollDown()

        self._timer.Start(100)
        return True


    def ProcessLeftUp(self, pt):
        """
        Handles left up mouse events.

        :param `pt`: an instance of :class:`wx.Point` where the left mouse button was released.
        """

        # always stop the timer
        self._timer.Stop()

        if not self.Contains(pt):
            return False

        self._state = ControlFocus
        self._parent.Refresh()

        return True


    def ProcessMouseMove(self, pt):
        """
        Handles mouse motion events. This is called any time the mouse moves in the parent menu,
        so we must check to see if the mouse is over the button.

        :param `pt`: an instance of :class:`wx.Point` where the mouse pointer was moved.
        """

        if not self.Contains(pt):

            self._timer.Stop()
            if self._state != ControlNormal:

                self._state = ControlNormal
                self._parent.Refresh()

            return False

        if self._scrollOnHover and not self._timer.IsRunning():
            self._timer.Start(100)

        # Process mouse move event
        if self._state != ControlFocus:
            if self._state != ControlPressed:
                self._state = ControlFocus
                self._parent.Refresh()

        return True


    def GetTimerId(self):
        """ Returns the timer object identifier. """

        return self._timerID


    def GetTimer(self):
        """ Returns the timer object. """

        return self._timer


    def Move(self, input1, input2=None):
        """
        Moves :class:`FlatMenuButton` to the specified position.

        :param `input1`: if it is an instance of :class:`wx.Point`, it represents the :class:`FlatMenuButton`
         position and the `input2` parameter is not used. Otherwise it is an integer representing
         the button `x` position;
        :param `input2`: if not ``None``, it is an integer representing the button `y` position.
        """

        if type(input1) == type(1):
            self._pos = wx.Point(input1, input2)
        else:
            self._pos = input1


    def SetSize(self, input1, input2=None):
        """
        Sets the size for :class:`FlatMenuButton`.

        :param `input1`: if it is an instance of :class:`wx.Size`, it represents the :class:`FlatMenuButton`
         size and the `input2` parameter is not used. Otherwise it is an integer representing
         the button width;
        :param `input2`: if not ``None``, it is an integer representing the button height.
        """

        if type(input1) == type(1):
            self._size = wx.Size(input1, input2)
        else:
            self._size = input1


    def GetClientRect(self):
        """ Returns the client rectangle for :class:`FlatMenuButton`. """

        return wx.Rect(self._pos, self._size)

#--------------------------------------------------------
# Class FlatMenuBase
#--------------------------------------------------------

class FlatMenuBase(ShadowPopupWindow):
    """
    Base class for generic flat menu derived from :class:`PopupWindow`.
    """

    def __init__(self, parent=None):
        """
        Default class constructor.

        :param `parent`: the :class:`ShadowPopupWindow` parent window.
        """

        self._rendererMgr = FMRendererMgr()
        self._parentMenu = parent
        self._openedSubMenu = None
        self._owner = None
        self._popupPtOffset = 0
        self._showScrollButtons = False
        self._upButton = None
        self._downButton = None
        self._is_dismiss = False

        ShadowPopupWindow.__init__(self, parent)


    def OnDismiss(self):
        """ Fires an event ``EVT_FLAT_MENU_DISMISSED`` and handle menu dismiss. """

        # Release mouse capture if needed
        if self.HasCapture():
            self.ReleaseMouse()

        self._is_dismiss = True

        # send an event about our dismissal to the parent (unless we are a sub menu)
        if self.IsShown() and not self._parentMenu:

            event = FlatMenuEvent(wxEVT_FLAT_MENU_DISMISSED, self.GetId())
            event.SetEventObject(self)

            # Send it
            if self.GetMenuOwner():
                self.GetMenuOwner().GetEventHandler().ProcessEvent(event)
            else:
                self.GetEventHandler().ProcessEvent(event)


    def Popup(self, pt, parent):
        """
        Popups menu at the specified point.

        :param `pt`: an instance of :class:`wx.Point`, assumed to be in screen coordinates. However,
         if `parent` is not ``None``, `pt` is translated into the screen coordinates using
         `parent.ClientToScreen()`;
        :param `parent`: if not ``None``, an instance of :class:`wx.Window`.
        """

        # some controls update themselves from OnIdle() call - let them do it
        if wx.GetApp().GetMainLoop():
            wx.GetApp().GetMainLoop().ProcessIdle()

        # The mouse was pressed in the parent coordinates,
        # e.g. pressing on the left top of a text ctrl
        # will result in (1, 1), these coordinates needs
        # to be converted into screen coords
        self._parentMenu = parent

        # If we are topmost menu, we use the given pt
        # else we use the logical
        # parent (second argument provided to this function)

        if self._parentMenu:
            pos = self._parentMenu.ClientToScreen(pt)
        else:
            pos = pt

        # Fit the menu into screen
        pos = self.AdjustPosition(pos)
        if self._showScrollButtons:

            sz = self.GetSize()
            # Get the screen height
            scrHeight = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)


            # position the scrollbar - If we are doing scroll bar buttons put them in the top right and
            # bottom right or else place them as menu items at the top and bottom.
            if self.GetRenderer().scrollBarButtons:
                if not self._upButton:
                    self._upButton = FlatMenuButton(self, True, ArtManager.Get().GetStockBitmap("arrow_up"))

                if not self._downButton:
                    self._downButton = FlatMenuButton(self, False, ArtManager.Get().GetStockBitmap("arrow_down"))

                self._upButton.SetSize((SCROLL_BTN_HEIGHT, SCROLL_BTN_HEIGHT))
                self._downButton.SetSize((SCROLL_BTN_HEIGHT, SCROLL_BTN_HEIGHT))

                self._upButton.Move((sz.x - SCROLL_BTN_HEIGHT - 4, 4))
                self._downButton.Move((sz.x - SCROLL_BTN_HEIGHT - 4, scrHeight - pos.y - 2 - SCROLL_BTN_HEIGHT))
            else:
                if not self._upButton:
                    self._upButton = FlatMenuButton(self, True, getMenuUpArrowBitmap(), scrollOnHover=True)

                if not self._downButton:
                    self._downButton = FlatMenuButton(self, False, getMenuDownArrowBitmap(), scrollOnHover=True)

                self._upButton.SetSize((sz.x-2, self.GetItemHeight()))
                self._downButton.SetSize((sz.x-2, self.GetItemHeight()))

                self._upButton.Move((1, 3))
                self._downButton.Move((1, scrHeight - pos.y - 3 - self.GetItemHeight()))

        self.Move(pos)
        self.Show()

        # Capture mouse event and direct them to us
        if not self.HasCapture():
            self.CaptureMouse()

        self._is_dismiss = False


    def AdjustPosition(self, pos):
        """
        Adjusts position so the menu will be fully visible on screen.

        :param `pos`: an instance of :class:`wx.Point` specifying the menu position.
        """

        # Check that the menu can fully appear in the screen
        scrWidth  = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        scrHeight = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        scrollBarButtons = self.GetRenderer().scrollBarButtons
        scrollBarMenuItems = not scrollBarButtons

        size = self.GetSize()
        if scrollBarMenuItems:
            size.y += self.GetItemHeight()*2

        # always assume that we have scrollbuttons on
        self._showScrollButtons = False
        pos.y += self._popupPtOffset

        if size.y + pos.y > scrHeight:
            # the menu will be truncated
            if self._parentMenu is None:
                # try to flip the menu
                flippedPosy = pos.y - size.y
                flippedPosy -= self._popupPtOffset

                if flippedPosy >= 0 and flippedPosy + size.y < scrHeight:
                    pos.y = flippedPosy
                    return pos
                else:
                    # We need to popup scrollbuttons!
                    self._showScrollButtons = True

            else:
                # we are a submenu
                # try to decrease the y value of the menu position
                newy = pos.y
                newy -= (size.y + pos.y) - scrHeight

                if newy + size.y > scrHeight:
                    # probably the menu size is too high to fit
                    # the screen, we need scrollbuttons
                    self._showScrollButtons = True
                else:
                    pos.y = newy

        menuMaxX = pos.x + size.x

        if menuMaxX > scrWidth and pos.x < scrWidth:

            if self._parentMenu:

                # We are submenu
                self._shiftePos = (size.x + self._parentMenu.GetSize().x)
                pos.x -= self._shiftePos
                pos.x += 10

            else:

                self._shiftePos  = ((size.x + pos.x) - scrWidth)
                pos.x -= self._shiftePos

        else:

            if self._parentMenu:
                pos.x += 5

        return pos


    def Dismiss(self, dismissParent, resetOwner):
        """
        Dismisses the popup window.

        :param bool `dismissParent`: whether to dismiss the parent menu or not;
        :param bool `resetOwner`: ``True`` to delete the link between this menu and the
         owner menu, ``False`` otherwise.
        """

        # Check if child menu is popped, if so, dismiss it
        if self._openedSubMenu:
            self._openedSubMenu.Dismiss(False, resetOwner)

        self.OnDismiss()

        # Reset menu owner
        if resetOwner:
            self._owner = None

        self.Show(False)

        if self._parentMenu and dismissParent:

            self._parentMenu.OnChildDismiss()
            self._parentMenu.Dismiss(dismissParent, resetOwner)

        self._parentMenu = None


    def OnChildDismiss(self):
        """ Handles children dismiss. """

        self._openedSubMenu = None


    def GetRenderer(self):
        """ Returns the renderer for this class. """

        return self._rendererMgr.GetRenderer()


    def GetRootMenu(self):
        """ Returns the top level menu. """

        root = self
        while root._parentMenu:
            root = root._parentMenu

        return root


    def SetOwnerHeight(self, height):
        """
        Sets the menu owner height, this will be used to position the menu below
        or above the owner.

        :param integer `height`: an integer representing the menu owner height.
        """

        self._popupPtOffset = height


    # by default do nothing
    def ScrollDown(self):
        """
        Scroll one unit down.
        By default this function is empty, let derived class do something.
        """

        pass


    # by default do nothing
    def ScrollUp(self):
        """
        Scroll one unit up.
        By default this function is empty, let derived class do something.
        """

        pass


    def GetMenuOwner(self):
        """
        Returns the menu logical owner, the owner does not necessarly mean the
        menu parent, it can also be the window that popped up it.
        """

        return self._owner

#--------------------------------------------------------
# Class FlatMenuItem
#--------------------------------------------------------

class FlatMenuItem(object):
    """
    A class that represents an item in a menu.
    """

    def __init__(self, parent, id=wx.ID_SEPARATOR, label="", helpString="",
                 kind=wx.ITEM_NORMAL, subMenu=None, normalBmp=wx.NullBitmap,
                 disabledBmp=wx.NullBitmap,
                 hotBmp=wx.NullBitmap):
        """
        Default class constructor.

        :param `parent`: menu that the menu item belongs to, an instance of :class:`FlatMenu`;
        :param integer `id`: the menu item identifier;
        :param string `label`: text for the menu item, as shown on the menu. An accelerator
         key can be specified using the ampersand '&' character. In order to embed
         an ampersand character in the menu item text, the ampersand must be doubled;
        :param string `helpString`: optional help string that will be shown on the status bar;
        :param integer `kind`: may be ``wx.ITEM_SEPARATOR``, ``wx.ITEM_NORMAL``
        :param `subMenu`: if not ``None``, the sub menu this item belongs to (an instance of :class:`FlatMenu`);
        :param `normalBmp`: normal bitmap to draw to the side of the text, this bitmap
         is used when the menu is enabled (an instance of :class:`wx.Bitmap`);
        :param `disabledBmp`: 'greyed' bitmap to draw to the side of the text, this
         bitmap is used when the menu is disabled, if none supplied normal is used (an instance of :class:`wx.Bitmap`);
        :param `hotBmp`: hot bitmap to draw to the side of the text, this bitmap is
         used when the menu is hovered, if non supplied, normal is used (an instance of :class:`wx.Bitmap`).
        """

        self._text = label
        self._kind = kind
        self._helpString = helpString

        if id == wx.ID_ANY:
            id = wx.NewIdRef()

        self._id = id
        self._parentMenu = parent
        self._subMenu = subMenu
        self._normalBmp = normalBmp
        self._disabledBmp = disabledBmp
        self._hotBmp = hotBmp
        self._bIsEnabled = True
        self._mnemonicIdx = wx.NOT_FOUND
        self._isAttachedToMenu = False
        self._accelStr = ""
        self._rect = wx.Rect()
        self._groupPtr = None
        self._visible = False
        self._contextMenu = None
        self._font = None
        self._textColour = None

        self.SetLabel(self._text)

    def SetLongHelp(self, help):
        """
        Sets the item long help string (displayed in the parent frame :class:`StatusBar`).

        :param string `help`: the new item long help string.
        """

        self._helpString = help


    def GetLongHelp(self):
        """ Returns the item long help string (displayed in the parent frame :class:`StatusBar`). """

        return self._helpString


    def GetShortHelp(self):
        """ Returns the item short help string (displayed in the tool's tooltip). """

        return ""


    def Enable(self, enable=True):
        """
        Enables or disables a menu item.

        :param bool `enable`: ``True`` to enable the menu item, ``False`` to disable it.
        """

        self._bIsEnabled = enable
        if self._parentMenu:
            self._parentMenu.UpdateItem(self)


    def GetBitmap(self):
        """
        Returns the normal bitmap associated to the menu item or :class:`NullBitmap` if
        none has been supplied.
        """

        return self._normalBmp


    def GetDisabledBitmap(self):
        """
        Returns the disabled bitmap associated to the menu item or :class:`NullBitmap`
        if none has been supplied.
        """

        return self._disabledBmp


    def GetHotBitmap(self):
        """
        Returns the hot bitmap associated to the menu item or :class:`NullBitmap` if
        none has been supplied.
        """

        return self._hotBmp


    def GetHelp(self):
        """ Returns the item help string. """

        return self._helpString


    def GetId(self):
        """ Returns the item id. """

        return self._id


    def GetKind(self):
        """
        Returns the menu item kind, can be one of ``wx.ITEM_SEPARATOR``, ``wx.ITEM_NORMAL``,
        """

        return self._kind


    def GetLabel(self):
        """ Returns the menu item label (without the accelerator if it is part of the string). """

        return self._label


    def GetMenu(self):
        """ Returns the parent menu. """

        return self._parentMenu


    def GetContextMenu(self):
        """ Returns the context menu associated with this item (if any). """

        return self._contextMenu


    def SetContextMenu(self, context_menu):
        """
        Assigns a context menu to this item.

        :param `context_menu`: an instance of :class:`FlatMenu`.
        """

        self._contextMenu = context_menu


    def GetText(self):
        """ Returns the text associated with the menu item including the accelerator. """

        return self._text


    def GetSubMenu(self):
        """ Returns the sub-menu of this menu item (if any). """

        return self._subMenu


    def IsEnabled(self):
        """ Returns whether an item is enabled or not. """

        return self._bIsEnabled


    def IsSeparator(self):
        """ Returns ``True`` if this item is of type ``wx.ITEM_SEPARATOR``, ``False`` otherwise. """

        return self._id == wx.ID_SEPARATOR


    def IsSubMenu(self):
        """ Returns whether an item is a sub-menu or not. """

        return self._subMenu is not None


    def SetNormalBitmap(self, bmp):
        """
        Sets the menu item normal bitmap.

        :param `bmp`: an instance of :class:`wx.Bitmap`.
        """

        self._normalBmp = bmp


    def SetDisabledBitmap(self, bmp):
        """
        Sets the menu item disabled bitmap.

        :param `bmp`: an instance of :class:`wx.Bitmap`.
        """

        self._disabledBmp = bmp


    def SetHotBitmap(self, bmp):
        """
        Sets the menu item hot bitmap.

        :param `bmp`: an instance of :class:`wx.Bitmap`.
        """

        self._hotBmp = bmp


    def SetHelp(self, helpString):
        """
        Sets the menu item help string.

        :param string `helpString`: the new menu item help string.
        """

        self._helpString = helpString


    def SetMenu(self, menu):
        """
        Sets the menu item parent menu.

        :param `menu`: an instance of :class:`FlatMenu`.
        """

        self._parentMenu = menu


    def SetSubMenu(self, menu):
        """
        Sets the menu item sub-menu.

        :param `menu`: an instance of :class:`FlatMenu`.
        """

        self._subMenu = menu

        # Fix toolbar update


    def GetAccelString(self):
        """ Returns the accelerator string. """

        return self._accelStr


    def SetRect(self, rect):
        """
        Sets the menu item client rectangle.

        :param `rect`: the menu item client rectangle, an instance of :class:`wx.Rect`.
        """

        self._rect = rect


    def GetRect(self):
        """ Returns the menu item client rectangle. """

        return self._rect


    def IsShown(self):
        """ Returns whether an item is shown or not. """

        return self._visible


    def Show(self, show=True):
        """
        Actually shows/hides the menu item.

        :param bool `show`: ``True`` to show the menu item, ``False`` to hide it.
        """

        self._visible = show


    def GetHeight(self):
        """ Returns the menu item height, in pixels. """

        if self.IsSeparator():
            return self._parentMenu.GetRenderer().separatorHeight
        else:
            return self._parentMenu._itemHeight


    def GetSuitableBitmap(self, selected):
        """
        Gets the bitmap that should be used based on the item state.

        :param bool `selected`: ``True`` if this menu item is currently hovered by the mouse,
         ``False`` otherwise.
        """

        normalBmp = self._normalBmp
        gBmp = (self._disabledBmp.IsOk() and [self._disabledBmp] or [self._normalBmp])[0]
        hotBmp = (self._hotBmp.IsOk() and [self._hotBmp] or [self._normalBmp])[0]

        if not self.IsEnabled():
            return gBmp
        elif selected:
            return hotBmp
        else:
            return normalBmp


    def SetLabel(self, text):
        """
        Sets the label text for this item from the text (excluding the accelerator).

        :param string `text`: the new item label (excluding the accelerator).
        """

        if text:

            indx = text.find("\t")
            if indx >= 0:
                self._accelStr = text[indx+1:]
                label = text[0:indx]
            else:
                self._accelStr = ""
                label = text

            self._mnemonicIdx, self._label = GetAccelIndex(label)

        else:

            self._mnemonicIdx = wx.NOT_FOUND
            self._label = ""

        if self._parentMenu:
            self._parentMenu.UpdateItem(self)


    def SetText(self, text):
        """
        Sets the text for this menu item (including accelerators).

        :param string `text`: the new item label (including the accelerator).
        """

        self._text = text
        self.SetLabel(self._text)


    def GetAcceleratorEntry(self):
        """ Returns the accelerator entry associated to this menu item. """

        if '\t' in self.GetText():
            accel = wx.AcceleratorEntry()
            accel.FromString(self.GetText())
            return accel
        elif self.GetAccelString():
            accel = wx.AcceleratorEntry()
            accel.FromString(self.GetAccelString())
            return accel
        else:
            return None


    def GetMnemonicChar(self):
        """ Returns the shortcut char for this menu item. """

        if self._mnemonicIdx == wx.NOT_FOUND:
            return 0

        mnemonic = self._label[self._mnemonicIdx]
        return mnemonic.lower()


    def SetFont(self, font=None):
        """
        Sets the :class:`FlatMenuItem` font.

        :param `font`: an instance of a valid :class:`wx.Font`.
        """

        self._font = font

        if self._parentMenu:
            self._parentMenu.UpdateItem(self)


    def GetFont(self):
        """ Returns this :class:`FlatMenuItem` font. """

        return self._font


    def SetTextColour(self, colour=None):
        """
        Sets the :class:`FlatMenuItem` foreground colour for the menu label.

        :param `colour`: an instance of a valid :class:`wx.Colour`.
        """

        self._textColour = colour


    def GetTextColour(self):
        """ Returns this :class:`FlatMenuItem` foreground text colour. """

        return self._textColour

#--------------------------------------------------------
# Class FlatMenu
#--------------------------------------------------------

class FlatMenu(FlatMenuBase):
    """
    A Flat popup menu generic implementation.
    """

    def __init__(self, parent=None):
        """
        Default class constructor.

        :param `parent`: the :class:`FlatMenu` parent window (used to initialize the
         underlying :class:`ShadowPopupWindow`).
        """

        self._menuWidth = 2*26
        self._leftMarginWidth = 26
        self._rightMarginWidth = 30
        self._borderXWidth = 1
        self._borderYWidth = 2
        self._activeWin = None
        self._focusWin = None
        self._imgMarginX = 0
        self._markerMarginX = 0
        self._textX = 26
        self._rightMarginPosX = -1
        self._itemHeight = 20
        self._selectedItem = -1
        self._clearCurrentSelection = True
        self._textPadding = 8
        self._marginHeight = 20
        self._marginWidth = 26
        self._accelWidth = 0
        self._mb = None
        self._itemsArr = []
        self._accelArray = []
        self._ptLast = wx.Point()
        self._resizeMenu = True
        self._shiftePos = 0
        self._first = 0
        self._mb_submenu = 0
        self._is_dismiss = False
        self._numCols = 1
        self._backgroundImage = None
        self._originalBackgroundImage = None

        FlatMenuBase.__init__(self, parent)

        self.SetSize(wx.Size(self._menuWidth, self._itemHeight+4))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeaveWindow)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_TIMER, self.OnTimer)


    def Destroy(self, *args, **kwargs):
        self.Clear()
        super().Destroy(*args, **kwargs)

    def Popup(self, pt, owner=None, parent=None):
        """
        Pops up the menu.

        :param `pt`: the point at which the menu should be popped up (an instance
         of :class:`wx.Point`);
        :param `owner`: the owner of the menu. The owner does not necessarly mean the
         menu parent, it can also be the window that popped up it;
        :param `parent`: the menu parent window.
        """

        if "__WXMSW__" in wx.Platform:
            self._mousePtAtStartup = wx.GetMousePosition()

        # each time we popup, need to reset the starting index
        self._first = 0

        # Loop over self menu and send update UI event for
        # every item in the menu
        numEvents = len(self._itemsArr)
        cc = 0
        self._shiftePos = 0

        # Set the owner of the menu. All events will be directed to it.
        # If owner is None, the Default GetParent() is used as the owner
        self._owner = owner

        for cc in range(numEvents):
            self.SendUIEvent(cc)

        # Adjust menu position and show it
        FlatMenuBase.Popup(self, pt, parent)

        # Replace the event handler of the active window to direct
        # all keyboard events to us and the focused window to direct char events to us
        self._activeWin = wx.GetActiveWindow()
        if self._activeWin:

            oldHandler = self._activeWin.GetEventHandler()
            newEvtHandler = MenuKbdRedirector(self, oldHandler)
            self._activeWin.PushEventHandler(newEvtHandler)

        if "__WXMSW__" in wx.Platform:
            self._focusWin = wx.Window.FindFocus()
        elif "__WXGTK__" in wx.Platform:
            self._focusWin = self
        else:
            self._focusWin = None

        if self._focusWin:
            newEvtHandler = FocusHandler(self)
            self._focusWin.PushEventHandler(newEvtHandler)


    def Append(self, id, item, helpString="", kind=wx.ITEM_NORMAL):
        """
        Appends an item to this menu.

        :param integer `id`: the menu item identifier;
        :param string `item`: the string to appear on the menu item;
        :param string `helpString`: an optional help string associated with the item. By default,
         the handler for the ``EVT_FLAT_MENU_ITEM_MOUSE_OVER`` event displays this string
         in the status line;
        :param integer `kind`: may be ``wx.ITEM_NORMAL`` for a normal button (default),
         ``wx.ITEM_CHECK`` for a checkable tool (such tool stays pressed after it had been
         toggled) or ``wx.ITEM_RADIO`` for a checkable tool which makes part of a radio
         group of tools each of which is automatically unchecked whenever another button
         in the group is checked;
        """

        newItem = FlatMenuItem(self, id, item, helpString, kind)
        return self.AppendItem(newItem)


    def Prepend(self, id, item, helpString="", kind=wx.ITEM_NORMAL):
        """
        Prepends an item to this menu.

        :param integer `id`: the menu item identifier;
        :param string `item`: the string to appear on the menu item;
        :param string `helpString`: an optional help string associated with the item. By default,
         the handler for the ``EVT_FLAT_MENU_ITEM_MOUSE_OVER`` event displays this string
         in the status line;
        :param integer `kind`: may be ``wx.ITEM_NORMAL`` for a normal button (default),
         ``wx.ITEM_CHECK`` for a checkable tool (such tool stays pressed after it had been
         toggled) or ``wx.ITEM_RADIO`` for a checkable tool which makes part of a radio
         group of tools each of which is automatically unchecked whenever another button
         in the group is checked;
        """

        newItem = FlatMenuItem(self, id, item, helpString, kind)
        return self.PrependItem(newItem)


    def AppendSubMenu(self, subMenu, item, helpString=""):
        """
        Adds a pull-right submenu to the end of the menu.

        This function is added to duplicate the API of :class:`wx.Menu`.

        :see: :meth:`~FlatMenu.AppendMenu` for an explanation of the input parameters.
        """

        return self.AppendMenu(wx.ID_ANY, item, subMenu, helpString)


    def AppendMenu(self, id, item, subMenu, helpString=""):
        """
        Adds a pull-right submenu to the end of the menu.

        :param integer `id`: the menu item identifier;
        :param string `item`: the string to appear on the menu item;
        :param `subMenu`: an instance of :class:`FlatMenu`, the submenu to append;
        :param string `helpString`: an optional help string associated with the item. By default,
         the handler for the ``EVT_FLAT_MENU_ITEM_MOUSE_OVER`` event displays this string
         in the status line.
        """

        newItem = FlatMenuItem(self, id, item, helpString, wx.ITEM_NORMAL, subMenu)
        return self.AppendItem(newItem)


    def AppendItem(self, menuItem):
        """
        Appends an item to this menu.

        :param `menuItem`: an instance of :class:`FlatMenuItem`.
        """

        self._itemsArr.append(menuItem)
        return self.AddItem(menuItem)


    def PrependItem(self, menuItem):
        """
        Prepends an item to this menu.

        :param `menuItem`: an instance of :class:`FlatMenuItem`.
        """

        self._itemsArr.insert(0,menuItem)
        return self.AddItem(menuItem)


    def AddItem(self, menuItem):
        """
        Internal function to add the item to this menu. The item must
        already be in the `self._itemsArr` attribute.

        :param `menuItem`: an instance of :class:`FlatMenuItem`.
        """

        if not menuItem:
            raise Exception("Adding None item?")

        # Reparent to us
        menuItem.SetMenu(self)
        menuItem._isAttachedToMenu = True

        # Update the menu width if necessary
        menuItemWidth = self.GetMenuItemWidth(menuItem)
        self._menuWidth = (self._menuWidth > menuItemWidth + self._accelWidth and \
                           [self._menuWidth] or [menuItemWidth + self._accelWidth])[0]

        menuHeight = 0
        switch = 1e6

        if self._numCols > 1:
            nItems = len(self._itemsArr)
            switch = int(math.ceil((nItems - self._first)/float(self._numCols)))

        for indx, item in enumerate(self._itemsArr):

            if indx >= switch:
                break

            if item.IsSeparator():
                menuHeight += self.GetRenderer().separatorHeight
            else:
                menuHeight += self._itemHeight

        self.SetSize(wx.Size(self._menuWidth*self._numCols, menuHeight+4))

        if self._originalBackgroundImage:
            img = self._originalBackgroundImage.ConvertToImage()
            img = img.Scale(self._menuWidth*self._numCols-2-self._leftMarginWidth, menuHeight, wx.IMAGE_QUALITY_HIGH)
            self._backgroundImage = img.ConvertToBitmap()

        # Add accelerator entry to the menu if needed
        accel = menuItem.GetAcceleratorEntry()

        if accel:
            accel.Set(accel.GetFlags(), accel.GetKeyCode(), menuItem.GetId())
            self._accelArray.append(accel)

        return menuItem


    def GetMenuItems(self):
        """ Returns the list of menu items in the menu. """

        return self._itemsArr


    def GetMenuItemWidth(self, menuItem):
        """
        Returns the width of a particular item.

        :param `menuItem`: an instance of :class:`FlatMenuItem`.
        """

        menuItemWidth = 0
        text = menuItem.GetLabel() # Without accelerator
        accel = menuItem.GetAccelString()

        dc = wx.ClientDC(self)

        font = menuItem.GetFont()
        if font is None:
            font = ArtManager.Get().GetFont()

        dc.SetFont(font)

        accelFiller = "XXXX"     # 4 spaces between text and accel column

        # Calc text length/height
        dummy, itemHeight = dc.GetTextExtent("Tp")
        width, height = dc.GetTextExtent(text)
        accelWidth, accelHeight = dc.GetTextExtent(accel)
        filler, dummy = dc.GetTextExtent(accelFiller)

        bmpHeight = bmpWidth = 0

        if menuItem.GetBitmap().IsOk():
            bmpHeight = menuItem.GetBitmap().GetHeight()
            bmpWidth  = menuItem.GetBitmap().GetWidth()

        if itemHeight < self._marginHeight:
            itemHeight = self._marginHeight

        itemHeight = (bmpHeight > self._itemHeight and [bmpHeight] or [itemHeight])[0]
        itemHeight += 2*self._borderYWidth

        # Update the global menu item height if needed
        self._itemHeight = (self._itemHeight > itemHeight and [self._itemHeight] or [itemHeight])[0]
        self._marginWidth = (self._marginWidth > bmpWidth and [self._marginWidth] or [bmpWidth])[0]

        # Update the accel width
        accelWidth += filler
        if accel:
            self._accelWidth = (self._accelWidth > accelWidth and [self._accelWidth] or [accelWidth])[0]

        # In case the item has image & is type radio or check, we need double size
        # left margin
        factor = 1

        if factor == 2:

            self._imgMarginX = self._marginWidth + 2*self._borderXWidth
            self._leftMarginWidth = 2 * self._marginWidth + 2*self._borderXWidth

        else:

            self._leftMarginWidth = ((self._leftMarginWidth > self._marginWidth + 2*self._borderXWidth) and \
                                    [self._leftMarginWidth] or [self._marginWidth + 2*self._borderXWidth])[0]

        menuItemWidth = self.GetLeftMarginWidth() + 2*self.GetBorderXWidth() + width + self.GetRightMarginWidth()
        self._textX = self._imgMarginX + self._marginWidth + self._textPadding

        # update the rightMargin X position
        self._rightMarginPosX = ((self._textX + width + self._accelWidth> self._rightMarginPosX) and \
                                 [self._textX + width + self._accelWidth] or [self._rightMarginPosX])[0]

        return menuItemWidth


    def GetMenuWidth(self):
        """ Returns the menu width in pixels. """

        return self._menuWidth


    def GetLeftMarginWidth(self):
        """ Returns the menu left margin width, in pixels. """

        return self._leftMarginWidth


    def GetRightMarginWidth(self):
        """ Returns the menu right margin width, in pixels. """

        return self._rightMarginWidth


    def GetBorderXWidth(self):
        """ Returns the menu border x-width, in pixels. """

        return self._borderXWidth


    def GetBorderYWidth(self):
        """ Returns the menu border y-width, in pixels. """

        return self._borderYWidth


    def GetItemHeight(self):
        """ Returns the height of a particular item, in pixels. """

        return self._itemHeight


    def AppendSeparator(self):
        """ Appends a separator item to the end of this menu. """

        newItem = FlatMenuItem(self)
        return self.AppendItem(newItem)


    def InsertSeparator(self, pos):
        """
        Inserts a separator at the given position.

        :param integer `pos`: the index at which we want to insert the separator.
        """

        newItem = FlatMenuItem(self)
        return self.InsertItem(pos, newItem)


    def Dismiss(self, dismissParent, resetOwner):
        """
        Dismisses the popup window.

        :param bool `dismissParent`: whether to dismiss the parent menu or not;
        :param bool `resetOwner`: ``True`` to delete the link between this menu and the
         owner menu, ``False`` otherwise.
        """

        if self._activeWin:

            self._activeWin.PopEventHandler(True)
            self._activeWin = None

        if self._focusWin:

            self._focusWin.PopEventHandler(True)
            self._focusWin = None

        self._selectedItem = -1

        if self._mb:
            self._mb.RemoveHelp()

        FlatMenuBase.Dismiss(self, dismissParent, resetOwner)


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`FlatMenu`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.PaintDC(self)
        self.GetRenderer().DrawMenu(self, dc)

        # We need to redraw all our child menus
        self.RefreshChilds()


    def UpdateItem(self, item):
        """
        Updates an item.

        :param `item`: an instance of :class:`FlatMenuItem`.
        """

        # notify menu bar that an item was modified directly
        if item and self._mb:
            self._mb.UpdateItem(item)


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`FlatMenu`.

        :param `event`: a :class:`EraseEvent` event to be processed.

        :note: This method is intentionally empty to avoid flicker.
        """

        pass


    def DrawSelection(self, dc, oldSelection=-1):
        """
        Redraws the menu.

        :param `dc`: an instance of :class:`wx.DC`;
        :param integer `oldSelection`: if non-negative, the index representing the previous selected
         menu item.
        """

        self.Refresh()


    def RefreshChilds(self):
        """
        In some cases, we need to perform a recursive refresh for all opened submenu
        from this.
        """

        # Draw all child menus of self menu as well
        child = self._openedSubMenu
        while child:
            dc = wx.ClientDC(child)
            self.GetRenderer().DrawMenu(child, dc)
            child = child._openedSubMenu


    def GetMenuRect(self):
        """ Returns the menu client rectangle. """

        clientRect = self.GetClientRect()
        return wx.Rect(clientRect.x, clientRect.y, clientRect.width, clientRect.height)


    def OnKeyDown(self, event):
        """
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`FlatMenu`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        self.OnChar(event.GetKeyCode())


    def OnChar(self, key):
        """
        Handles key events for :class:`FlatMenu`.

        :param `key`: the keyboard key integer code.
        """

        processed = True

        if key == wx.WXK_ESCAPE:

            if self._parentMenu:
                self._parentMenu.CloseSubMenu(-1)
            else:
                self.Dismiss(True, True)

        elif key == wx.WXK_LEFT:

            if self._parentMenu:
                # We are a submenu, dismiss us.
                self._parentMenu.CloseSubMenu(-1)
            else:
                # try to find our root menu, if we are attached to menubar,
                # let it try and open the previous menu
                root = self.GetRootMenu()
                if root:
                    if root._mb:
                        root._mb.ActivatePreviousMenu()

        elif key == wx.WXK_RIGHT:

            if not self.TryOpenSubMenu(self._selectedItem, True):
                # try to find our root menu, if we are attached to menubar,
                # let it try and open the previous menu
                root = self.GetRootMenu()
                if root:
                    if root._mb:
                        root._mb.ActivateNextMenu()

        elif key == wx.WXK_UP:
            self.AdvanceSelection(False)

        elif key == wx.WXK_DOWN:

            self.AdvanceSelection()

        elif key in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            self.DoAction(self._selectedItem)

        elif key == wx.WXK_HOME:

            # Select first item of the menu
            if self._selectedItem != 0:
                oldSel = self._selectedItem
                self._selectedItem = 0
                dc = wx.ClientDC(self)
                self.DrawSelection(dc, oldSel)

        elif key == wx.WXK_END:

            # Select last item of the menu
            if self._selectedItem != len(self._itemsArr)-1:
                oldSel = self._selectedItem
                self._selectedItem = len(self._itemsArr)-1
                dc = wx.ClientDC(self)
                self.DrawSelection(dc, oldSel)

        elif key in [wx.WXK_CONTROL, wx.WXK_ALT]:
            # Alt was pressed
            root = self.GetRootMenu()
            root.Dismiss(False, True)

        else:
            try:
                chrkey = chr(key)
            except:
                return processed

            if chrkey.isalnum():

                ch = chrkey.lower()

                # Iterate over all the menu items
                itemIdx = -1
                occur = 0

                for i in range(len(self._itemsArr)):

                    item = self._itemsArr[i]
                    mnemonic = item.GetMnemonicChar()

                    if mnemonic == ch:

                        if itemIdx == -1:

                            itemIdx = i
                            # We keep the index of only
                            # the first occurrence

                        occur += 1

                        # Keep on looping until no more items for self menu

                if itemIdx != -1:

                    if occur > 1:

                        # We select the first item
                        if self._selectedItem == itemIdx:
                            return processed

                        oldSel = self._selectedItem
                        self._selectedItem = itemIdx
                        dc = wx.ClientDC(self)
                        self.DrawSelection(dc, oldSel)

                    elif occur == 1:

                        # Activate the item, if self is a submenu item we first select it
                        item = self._itemsArr[itemIdx]
                        if item.IsSubMenu() and self._selectedItem != itemIdx:

                            oldSel = self._selectedItem
                            self._selectedItem = itemIdx
                            dc = wx.ClientDC(self)
                            self.DrawSelection(dc, oldSel)

                        self.DoAction(itemIdx)

                else:

                    processed = False

        return processed


    def AdvanceSelection(self, down=True):
        """
        Advance forward or backward the current selection.

        :param bool `down`: ``True`` to advance the selection forward, ``False`` otherwise.
        """

        # make sure we have at least two items in the menu (which are not
        # separators)
        num=0
        singleItemIdx = -1

        for i in range(len(self._itemsArr)):

            item = self._itemsArr[i]
            if item.IsSeparator():
                continue
            num += 1
            singleItemIdx = i

        if num < 1:
            return

        if num == 1:
            # Select the current one
            self._selectedItem = singleItemIdx
            dc = wx.ClientDC(self)
            self.DrawSelection(dc, -1)
            return

        oldSelection = self._selectedItem

        if not down:

            # find the next valid item
            while 1:

                self._selectedItem -= 1
                if self._selectedItem < 0:
                    self._selectedItem = len(self._itemsArr)-1
                if not self._itemsArr[self._selectedItem].IsSeparator():
                    break

        else:

            # find the next valid item
            while 1:

                self._selectedItem += 1
                if self._selectedItem > len(self._itemsArr)-1:
                    self._selectedItem = 0
                if not self._itemsArr[self._selectedItem].IsSeparator():
                    break

        dc = wx.ClientDC(self)
        self.DrawSelection(dc, oldSelection)


    def HitTest(self, pos):
        """
        HitTest method for :class:`FlatMenu`.

        :param `pos`: an instance of :class:`wx.Point`, a point to test for hits.

        :return: A tuple representing one of the following combinations:

         ========================= ==================================================
         Return Tuple              Description
         ========================= ==================================================
         (0, -1)                   The :meth:`~FlatMenu.HitTest` method didn't find any item with the specified input point `pt` (``MENU_HT_NONE`` = 0)
         (1, `integer`)            A menu item has been hit (``MENU_HT_ITEM`` = 1)
         (2, -1)                   The `Scroll Up` button has been hit (``MENU_HT_SCROLL_UP`` = 2)
         (3, -1)                   The `Scroll Down` button has been hit (``MENU_HT_SCROLL_DOWN`` = 3)
         ========================= ==================================================

        """

        if self._showScrollButtons:

            if self._upButton and self._upButton.GetClientRect().Contains(pos):
                return MENU_HT_SCROLL_UP, -1

            if self._downButton and self._downButton.GetClientRect().Contains(pos):
                return MENU_HT_SCROLL_DOWN, -1

        for ii, item in enumerate(self._itemsArr):

            if item.GetRect().Contains(pos) and item.IsEnabled() and item.IsShown():
                return MENU_HT_ITEM, ii

        return MENU_HT_NONE, -1


    def OnMouseMove(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`FlatMenu`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if "__WXMSW__" in wx.Platform:
            # Ignore dummy mouse move events
            pt = wx.GetMousePosition()
            if self._mousePtAtStartup == pt:
                return

        pos = event.GetPosition()

        # we need to ignore extra mouse events: example when this happens is when
        # the mouse is on the menu and we open a submenu from keyboard - Windows
        # then sends us a dummy mouse move event, we (correctly) determine that it
        # happens in the parent menu and so immediately close the just opened
        # submenunot

        if "__WXMSW__" in wx.Platform:

            ptCur = self.ClientToScreen(pos)
            if ptCur == self._ptLast:
                return

            self._ptLast = ptCur

        # first let the scrollbar handle it
        self.TryScrollButtons(event)
        self.ProcessMouseMove(pos)


    def OnMouseLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`FlatMenu`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self.TryScrollButtons(event):
            return

        pos = event.GetPosition()
        self.ProcessMouseLClick(pos)


    def OnMouseLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`FlatMenu`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self.TryScrollButtons(event):
            return

        pos = event.GetPosition()
        rect = self.GetClientRect()

        if not rect.Contains(pos):

            # The event is not in our coords,
            # so we try our parent
            win = self._parentMenu

            while win:

                # we need to translate our client coords to the client coords of the
                # window we forward this event to
                ptScreen = self.ClientToScreen(pos)
                p = win.ScreenToClient(ptScreen)

                if win.GetClientRect().Contains(p):

                    event.SetX(p.x)
                    event.SetY(p.y)
                    win.OnMouseLeftUp(event)
                    return

                else:
                    # try the grandparent
                    win = win._parentMenu

        else:
            self.ProcessMouseLClickEnd(pos)

        if self._showScrollButtons:

            if self._upButton:
                self._upButton.ProcessLeftUp(pos)
            if self._downButton:
                self._downButton.ProcessLeftUp(pos)


    def OnMouseRightDown(self, event):
        """
        Handles the ``wx.EVT_RIGHT_DOWN`` event for :class:`FlatMenu`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self.TryScrollButtons(event):
            return

        pos = event.GetPosition()
        self.ProcessMouseRClick(pos)


    def ProcessMouseRClick(self, pos):
        """
        Processes mouse right clicks.

        :param `pos`: the position at which the mouse right button was pressed,
         an instance of :class:`wx.Point`.
        """

        rect = self.GetClientRect()

        if not rect.Contains(pos):

            # The event is not in our coords,
            # so we try our parent

            win = self._parentMenu
            while win:

                # we need to translate our client coords to the client coords of the
                # window we forward self event to
                ptScreen = self.ClientToScreen(pos)
                p = win.ScreenToClient(ptScreen)

                if win.GetClientRect().Contains(p):
                    win.ProcessMouseRClick(p)
                    return

                else:
                    # try the grandparent
                    win = win._parentMenu

            # At this point we can assume that the event was not
            # processed, so we dismiss the menu and its children
            self.Dismiss(True, True)
            return

        # test if we are on a menu item
        res, itemIdx = self.HitTest(pos)
        if res == MENU_HT_ITEM:
            self.OpenItemContextMenu(itemIdx)


    def OpenItemContextMenu(self, itemIdx):
        """
        Open an item's context menu (if any).

        :param integer `itemIdx`: the index of the item for which we want to open the context menu.
        """

        item = self._itemsArr[itemIdx]
        context_menu = item.GetContextMenu()

        # If we have a context menu, close any opened submenu
        if context_menu:
            self.CloseSubMenu(itemIdx, True)

        if context_menu and not context_menu.IsShown():
            # Popup child menu
            pos = wx.Point()
            pos.x = item.GetRect().GetWidth() + item.GetRect().GetX() - 5
            pos.y = item.GetRect().GetY()
            self._clearCurrentSelection = False
            self._openedSubMenu = context_menu
            context_menu.Popup(self.ScreenToClient(wx.GetMousePosition()), self._owner, self)
            return True

        return False


    def ProcessMouseLClick(self, pos):
        """
        Processes mouse left clicks.

        :param `pos`: the position at which the mouse left button was pressed,
         an instance of :class:`wx.Point`.
        """

        rect = self.GetClientRect()

        if not rect.Contains(pos):

            # The event is not in our coords,
            # so we try our parent

            win = self._parentMenu
            while win:

                # we need to translate our client coords to the client coords of the
                # window we forward self event to
                ptScreen = self.ClientToScreen(pos)
                p = win.ScreenToClient(ptScreen)

                if win.GetClientRect().Contains(p):
                    win.ProcessMouseLClick(p)
                    return

                else:
                    # try the grandparent
                    win = win._parentMenu

            # At this point we can assume that the event was not
            # processed, so we dismiss the menu and its children
            self.Dismiss(True, True)
            return


    def ProcessMouseLClickEnd(self, pos):
        """
        Processes mouse left clicks.

        :param `pos`: the position at which the mouse left button was pressed,
         an instance of :class:`wx.Point`.
        """

        self.ProcessMouseLClick(pos)

        # test if we are on a menu item
        res, itemIdx = self.HitTest(pos)

        if res == MENU_HT_ITEM:
            self.DoAction(itemIdx)

        elif res == MENU_HT_SCROLL_UP:
            if self._upButton:
                self._upButton.ProcessLeftDown(pos)

        elif res == MENU_HT_SCROLL_DOWN:
            if self._downButton:
                self._downButton.ProcessLeftDown(pos)

        else:
            self._selectedItem = -1


    def ProcessMouseMove(self, pos):
        """
        Processes mouse movements.

        :param `pos`: the position at which the mouse was moved, an instance of :class:`wx.Point`.
        """

        rect = self.GetClientRect()

        if not rect.Contains(pos):

            # The event is not in our coords,
            # so we try our parent

            win = self._parentMenu
            while win:

                # we need to translate our client coords to the client coords of the
                # window we forward self event to
                ptScreen = self.ClientToScreen(pos)
                p = win.ScreenToClient(ptScreen)

                if win.GetClientRect().Contains(p):
                    win.ProcessMouseMove(p)
                    return

                else:
                    # try the grandparent
                    win = win._parentMenu

            # If we are attached to a menu bar,
            # let him process the event as well
            if self._mb:

                ptScreen = self.ClientToScreen(pos)
                p = self._mb.ScreenToClient(ptScreen)

                if self._mb.GetClientRect().Contains(p):

                    # let the menu bar process it
                    self._mb.ProcessMouseMoveFromMenu(p)
                    return

            if self._mb_submenu:
                ptScreen = self.ClientToScreen(pos)
                p = self._mb_submenu.ScreenToClient(ptScreen)
                if self._mb_submenu.GetClientRect().Contains(p):
                    # let the menu bar process it
                    self._mb_submenu.ProcessMouseMoveFromMenu(p)
                    return

            return

        # test if we are on a menu item
        res, itemIdx = self.HitTest(pos)

        if res == MENU_HT_SCROLL_DOWN:

            if self._downButton:
                self._downButton.ProcessMouseMove(pos)

        elif res == MENU_HT_SCROLL_UP:

            if self._upButton:
                self._upButton.ProcessMouseMove(pos)

        elif res == MENU_HT_ITEM:

            if self._downButton:
                self._downButton.ProcessMouseMove(pos)

            if self._upButton:
                self._upButton.ProcessMouseMove(pos)

            if self._selectedItem == itemIdx:
                return

            # Message to send when out of last selected item
            if self._selectedItem != -1:
                self.SendOverItem(self._selectedItem, False)
            self.SendOverItem(itemIdx, True)   # Message to send when over an item

            oldSelection = self._selectedItem
            self._selectedItem = itemIdx
            self.CloseSubMenu(self._selectedItem)

            dc = wx.ClientDC(self)
            self.DrawSelection(dc, oldSelection)

            self.TryOpenSubMenu(self._selectedItem)

            if self._mb:
                self._mb.RemoveHelp()
                if itemIdx >= 0:
                    self._mb.DoGiveHelp(self._itemsArr[itemIdx])

        else:

            # Message to send when out of last selected item
            if self._selectedItem != -1:
                item = self._itemsArr[self._selectedItem]
                if item.IsSubMenu() and item.GetSubMenu().IsShown():
                    return

                # Message to send when out of last selected item
                if self._selectedItem != -1:
                    self.SendOverItem(self._selectedItem, False)

            oldSelection = self._selectedItem
            self._selectedItem = -1
            dc = wx.ClientDC(self)
            self.DrawSelection(dc, oldSelection)


    def OnMouseLeaveWindow(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`FlatMenu`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self._mb:
            self._mb.RemoveHelp()

        if self._clearCurrentSelection:

            # Message to send when out of last selected item
            if self._selectedItem != -1:
                item = self._itemsArr[self._selectedItem]
                if item.IsSubMenu() and item.GetSubMenu().IsShown():
                    return

                # Message to send when out of last selected item
                if self._selectedItem != -1:
                    self.SendOverItem(self._selectedItem, False)

            oldSelection = self._selectedItem
            self._selectedItem = -1
            dc = wx.ClientDC(self)
            self.DrawSelection(dc, oldSelection)

        self._clearCurrentSelection = True

        if "__WXMSW__" in wx.Platform:
            self.SetCursor(self._oldCur)


    def OnMouseEnterWindow(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`FlatMenu`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if "__WXMSW__" in wx.Platform:
            self._oldCur = self.GetCursor()
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        event.Skip()


    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`FlatMenu`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        self.Dismiss(True, True)


    def CloseSubMenu(self, itemIdx, alwaysClose=False):
        """
        Closes a child sub-menu.

        :param integer `itemIdx`: the index of the item for which we want to close the submenu;
        :param bool `alwaysClose`: if ``True``, always close the submenu irrespectively of
         other conditions.
        """

        item = None
        subMenu = None

        if itemIdx >= 0 and itemIdx < len(self._itemsArr):
            item = self._itemsArr[itemIdx]

        # Close sub-menu first
        if item:
            subMenu = item.GetSubMenu()

        if self._openedSubMenu:
            if self._openedSubMenu != subMenu or alwaysClose:
                # We have another sub-menu open, close it
                self._openedSubMenu.Dismiss(False, True)
                self._openedSubMenu = None


    def DoAction(self, itemIdx):
        """
        Performs an action based on user selection.

        :param integer `itemIdx`: the index of the item for which we want to perform the action.
        """

        if itemIdx < 0 or itemIdx >= len(self._itemsArr):
            raise Exception("Invalid menu item")
            return

        item = self._itemsArr[itemIdx]

        if not item.IsEnabled() or item.IsSeparator():
            return

        # Close sub-menu if needed
        self.CloseSubMenu(itemIdx)

        if item.IsSubMenu() and not item.GetSubMenu().IsShown():

            # Popup child menu
            self.TryOpenSubMenu(itemIdx)
            return

        if not item.IsSubMenu():

            self.Dismiss(True, False)

            # Send command event
            self.SendCmdEvent(itemIdx)


    def TryOpenSubMenu(self, itemIdx, selectFirst=False):
        """
        If `itemIdx` is an item with submenu, open it.

        :param integer `itemIdx`: the index of the item for which we want to open the submenu;
        :param bool `selectFirst`: if ``True``, the first item of the submenu will be shown
         as selected.
        """

        if itemIdx < 0 or itemIdx >= len(self._itemsArr):
            return False

        item = self._itemsArr[itemIdx]
        if item.IsSubMenu() and not item.GetSubMenu().IsShown():

            pos = wx.Point()

            # Popup child menu
            pos.x = item.GetRect().GetWidth()+ item.GetRect().GetX()-5
            pos.y = item.GetRect().GetY()
            self._clearCurrentSelection = False
            self._openedSubMenu = item.GetSubMenu()
            item.GetSubMenu().Popup(pos, self._owner, self)

            # Select the first child
            if selectFirst:

                dc = wx.ClientDC(item.GetSubMenu())
                item.GetSubMenu()._selectedItem = 0
                item.GetSubMenu().DrawSelection(dc)

            return True

        return False


    def _RemoveById(self, id):
        """ Used internally. """

        # First we search for the menu item (recursively)
        menuParent = None
        item = None
        idx = wx.NOT_FOUND
        idx, menuParent = self.FindMenuItemPos(id)

        if idx != wx.NOT_FOUND:

            # Remove the menu item
            item = menuParent._itemsArr[idx]
            menuParent._itemsArr.pop(idx)

            # Resize the menu
            menuParent.ResizeMenu()

        return item


    def Remove(self, item):
        """
        Removes the menu item from the menu but doesn't delete the associated menu
        object. This allows to reuse the same item later by adding it back to the
        menu (especially useful with submenus).

        :param `item`: can be either a menu item identifier or a plain :class:`FlatMenuItem`.
        """

        if not isinstance(item, (wx.StandardID, int)):
            item = item.GetId()

        return self._RemoveById(item)

    Delete = Remove


    def _DestroyById(self, id):
        """ Used internally. """

        item = None
        item = self.Remove(id)

        if item:
            del item


    def DestroyItem(self, item):
        """
        Deletes the menu item from the menu. If the item is a submenu, it will be
        deleted. Use :meth:`~FlatMenu.Remove` if you want to keep the submenu (for example, to reuse
        it later).

        :param `item`: can be either a menu item identifier or a plain :class:`FlatMenuItem`.
        """

        if not isinstance(item, (wx.StandardID, int)):
            item = item.GetId()

        self._DestroyById(item)


    def Insert(self, pos, id, item, helpString="", kind=wx.ITEM_NORMAL):
        """
        Inserts the given `item` before the position `pos`.

        :param integer `pos`: the position at which to insert the new menu item;
        :param integer `id`: the menu item identifier;
        :param string `item`: the string to appear on the menu item;
        :param string `helpString`: an optional help string associated with the item. By default,
         the handler for the ``EVT_FLAT_MENU_ITEM_MOUSE_OVER`` event displays this string
         in the status line;
        :param integer `kind`: may be ``wx.ITEM_NORMAL`` for a normal button (default),
         ``wx.ITEM_CHECK`` for a checkable tool (such tool stays pressed after it had been
         toggled) or ``wx.ITEM_RADIO`` for a checkable tool which makes part of a radio
         group of tools each of which is automatically unchecked whenever another button
         in the group is checked;
        """

        newitem = FlatMenuItem(self, id, item, helpString, kind)
        return self.InsertItem(pos, newitem)


    def InsertItem(self, pos, item):
        """
        Inserts an item into the menu.

        :param integer `pos`: the position at which to insert the new menu item;
        :param `item`: an instance of :class:`FlatMenuItem`.
        """

        if pos == len(self._itemsArr):
            # Append it
            return self.AppendItem(item)

        # Insert the menu item
        self._itemsArr.insert(pos, item)
        item._isAttachedToMenu = True

        # Recalculate the menu geometry
        self.ResizeMenu()

        return item


    def ResizeMenu(self):
        """ Resizes the menu to the correct size. """

        # can we do the resize?
        if not self._resizeMenu:
            return

        items = self._itemsArr
        self._itemsArr = []

        # Clear accelerator table
        self._accelArray = []

        # Reset parameters and menu size
        self._menuWidth =  2*self._marginWidth
        self._imgMarginX = 0
        self._markerMarginX = 0
        self._textX = self._marginWidth
        self._rightMarginPosX = -1
        self._itemHeight = self._marginHeight
        self.SetSize(wx.Size(self._menuWidth*self._numCols, self._itemHeight+4))

        # Now we simply add the items
        for item in items:
            self.AppendItem(item)


    def SetNumberColumns(self, numCols):
        """
        Sets the number of columns for a menu window.

        :param integer `numCols`: the number of columns for this :class:`FlatMenu` window.
        """

        if self._numCols == numCols:
            return

        self._numCols = numCols
        self.ResizeMenu()
        self.Refresh()


    def GetNumberColumns(self):
        """ Returns the number of columns for a menu window. """

        return self._numCols


    def FindItem(self, itemId, menu=None):
        """
        Finds the menu item object associated with the given menu item identifier and,
        optionally, the (sub)menu it belongs to.

        :param integer `itemId`: menu item identifier;
        :param `menu`: if not ``None``, it will be filled with the item's parent menu
         (if the item was found).

        :return: The found menu item object, or ``None`` if one was not found.
        """

        idx = wx.NOT_FOUND

        if menu:

            idx, menu = self.FindMenuItemPos(itemId, menu)
            if idx != wx.NOT_FOUND:
                return menu._itemsArr[idx]
            else:
                return None

        else:

            idx, parentMenu = self.FindMenuItemPos(itemId, None)
            if idx != wx.NOT_FOUND:
                return parentMenu._itemsArr[idx]
            else:
                return None


    def SetItemFont(self, itemId, font=None):
        """
        Sets the :class:`FlatMenuItem` font.

        :param integer `itemId`: the menu item identifier;
        :param `font`: an instance of a valid :class:`wx.Font`.
        """

        item = self.FindItem(itemId)
        item.SetFont(font)


    def GetItemFont(self, itemId):
        """
        Returns this :class:`FlatMenuItem` font.

        :param integer `itemId`: the menu item identifier.
        """

        item = self.FindItem(itemId)
        return item.GetFont()


    def SetItemTextColour(self, itemId, colour=None):
        """
        Sets the :class:`FlatMenuItem` foreground text colour.

        :param integer `itemId`: the menu item identifier;
        :param `colour`: an instance of a valid :class:`wx.Colour`.
        """

        item = self.FindItem(itemId)
        item.SetTextColour(colour)


    def GetItemTextColour(self, itemId):
        """
        Returns this :class:`FlatMenuItem` foreground text colour.

        :param integer `itemId`: the menu item identifier.
        """

        item = self.FindItem(itemId)
        return item.GetTextColour()


    def SetLabel(self, itemId, label):
        """
        Sets the label of a :class:`FlatMenuItem`.

        :param integer `itemId`: the menu item identifier;
        :param string `label`: the menu item label to set.

        :see: :meth:`~FlatMenu.GetLabel`.
        """

        item = self.FindItem(itemId)
        item.SetLabel(label)
        item.SetText(label)

        self.ResizeMenu()


    def GetLabel(self, itemId):
        """
        Returns the label of a :class:`FlatMenuItem`.

        :param integer `id`: the menu item identifier;

        :see: :meth:`~FlatMenu.SetLabel`.
        """

        item = self.FindItem(itemId)
        return item.GetText()


    def FindMenuItemPos(self, itemId, menu=None):
        """
        Finds an item and its position inside the menu based on its id.

        :param integer `itemId`: menu item identifier;
        :param `menu`: if not ``None``, it will be filled with the item's parent menu
         (if the item was found).

        :return: The found menu item object, or ``None`` if one was not found.
        """

        menu = None
        item = None

        idx = wx.NOT_FOUND

        for i in range(len(self._itemsArr)):

            item = self._itemsArr[i]

            if item.GetId() == itemId:

                menu = self
                idx = i
                break

            elif item.IsSubMenu():

                idx, menu = item.GetSubMenu().FindMenuItemPos(itemId, menu)
                if idx != wx.NOT_FOUND:
                    break

            else:

                item = None

        return idx, menu


    def GetAccelTable(self):
        """ Returns the menu accelerator table, an instance of :class:`AcceleratorTable`. """

        n = len(self._accelArray)
        if n == 0:
            return wx.NullAcceleratorTable

        entries = [wx.AcceleratorEntry() for ii in range(n)]

        for counter in len(entries):
            entries[counter] = self._accelArray[counter]

        table = wx.AcceleratorTable(entries)
        del entries

        return table


    def GetMenuItemCount(self):
        """ Returns the number of items in the :class:`FlatMenu`. """

        return len(self._itemsArr)


    def GetAccelArray(self):
        """ Returns a list filled with the accelerator entries for the menu. """

        return self._accelArray


    # events
    def SendCmdEvent(self, itemIdx):
        """
        Actually sends menu command events.

        :param integer `itemIdx`: the menu item index for which we want to send a command event.
        """

        if itemIdx < 0 or itemIdx >= len(self._itemsArr):
            raise Exception("Invalid menu item")
            return

        item = self._itemsArr[itemIdx]

        # Create the event
        event = wx.CommandEvent(wxEVT_FLAT_MENU_SELECTED, item.GetId())

        event.SetEventObject(self)

        if self._owner:
            self._owner.GetEventHandler().ProcessEvent(event)
        else:
            self.GetEventHandler().ProcessEvent(event)


    def SendOverItem(self, itemIdx, over):
        """
        Sends the ``EVT_FLAT_MENU_ITEM_MOUSE_OVER`` and ``EVT_FLAT_MENU_ITEM_MOUSE_OUT``
        events.

        :param integer `itemIdx`: the menu item index for which we want to send an event;
        :param bool `over`: ``True`` to send a ``EVT_FLAT_MENU_ITEM_MOUSE_OVER`` event, ``False`` to
         send a ``EVT_FLAT_MENU_ITEM_MOUSE_OUT`` event.
        """

        item = self._itemsArr[itemIdx]

        # Create the event
        event = FlatMenuEvent((over and [wxEVT_FLAT_MENU_ITEM_MOUSE_OVER] or [wxEVT_FLAT_MENU_ITEM_MOUSE_OUT])[0], item.GetId())

        event.SetEventObject(self)

        if self._owner:
            self._owner.GetEventHandler().ProcessEvent(event)
        else:
            self.GetEventHandler().ProcessEvent(event)


    def SendUIEvent(self, itemIdx):
        """
        Actually sends menu UI events.

        :param integer `itemIdx`: the menu item index for which we want to send a UI event.
        """

        if itemIdx < 0 or itemIdx >= len(self._itemsArr):
            raise Exception("Invalid menu item")
            return

        item = self._itemsArr[itemIdx]
        event = wx.UpdateUIEvent(item.GetId())

        event.Enable(item.IsEnabled())
        event.SetText(item.GetText())
        event.SetEventObject(self)

        if self._owner:
            self._owner.GetEventHandler().ProcessEvent(event)
        else:
            self.GetEventHandler().ProcessEvent(event)

        item.SetLabel(event.GetText())
        item.Enable(event.GetEnabled())


    def Clear(self):
        """ Clears the menu items. """

        # since Destroy() call ResizeMenu(), we turn this flag on
        # to avoid resizing the menu for every item removed
        self._resizeMenu = False

        lenItems = len(self._itemsArr)
        for ii in range(lenItems):
            self.DestroyItem(self._itemsArr[0].GetId())

        # Now we can resize the menu
        self._resizeMenu = True
        self.ResizeMenu()


    def FindMenuItemPosSimple(self, item):
        """
        Finds an item and its position inside the menu based on its id.

        :param `item`: an instance of :class:`FlatMenuItem`.

        :return: An integer specifying the index found menu item object, or
         ``wx.NOT_FOUND`` if one was not found.
        """

        if item is None or len(self._itemsArr) == 0:
            return wx.NOT_FOUND

        for i in range(len(self._itemsArr)):
            if self._itemsArr[i] == item:
                return i

        return wx.NOT_FOUND


    def SetBackgroundBitmap(self, bitmap=None):
        """
        Sets a background bitmap for this particular :class:`FlatMenu`.

        :param `bitmap`: an instance of :class:`wx.Bitmap`. Set `bitmap` to ``None`` if you
         wish to remove the background bitmap altogether.

        :note: the bitmap is rescaled to fit the menu width and height.
        """

        self._originalBackgroundImage = bitmap
        # Now we can resize the menu
        self._resizeMenu = True
        self.ResizeMenu()


    def GetBackgroundBitmap(self):
        """ Returns the background bitmap for this particular :class:`FlatMenu`, if any. """

        return self._originalBackgroundImage


    def GetAllItems(self, menu=None, items=[]):
        """
        Internal function to help recurse through all the menu items.

        :param `menu`: the menu from which we start accumulating items;
        :param list `items`: the array which is recursively filled with menu items.

        :return: a list of :class:`FlatMenuItem`.
        """

        # first copy the current menu items
        newitems = [item for item in items]

        if not menu:
            return newitems

        # if any item in this menu has sub-menu, copy them as well
        for i in range(len(menu._itemsArr)):
            if menu._itemsArr[i].IsSubMenu():
                newitems = self.GetAllItems(menu._itemsArr[i].GetSubMenu(), newitems)

        return newitems


    def GetSiblingGroupItem(self, item):
        """
        Used internally.

        :param `item`: an instance of :class:`FlatMenuItem`.
        """

        pos = self.FindMenuItemPosSimple(item)
        if pos in [wx.NOT_FOUND, 0]:
            return None

        return None


    def ScrollDown(self):
        """ Scrolls the menu down (for very tall menus). """

        # increase the self._from index
        if not self._itemsArr[-1].IsShown():
            self._first += 1
            self.Refresh()

            return True

        else:
            if self._downButton:
                self._downButton.GetTimer().Stop()

            return False


    def ScrollUp(self):
        """ Scrolls the menu up (for very tall menus). """

        if self._first == 0:
            if self._upButton:
                self._upButton.GetTimer().Stop()

            return False

        else:

            self._first -= 1
            self.Refresh()
            return True


    # Not used anymore
    def TryScrollButtons(self, event):
        """ Used internally. """

        return False


    def OnTimer(self, event):
        """
        Handles the ``wx.EVT_TIMER`` event for :class:`FlatMenu`.

        :param `event`: a :class:`TimerEvent` event to be processed.
        """

        if self._upButton and self._upButton.GetTimerId() == event.GetId():

            self.ScrollUp()

        elif self._downButton and self._downButton.GetTimerId() == event.GetId():

            self.ScrollDown()

        else:

            event.Skip()

#--------------------------------------------------------
# Class MenuKbdRedirector
#--------------------------------------------------------

class MenuKbdRedirector(wx.EvtHandler):
    """ A keyboard event handler. """

    def __init__(self, menu, oldHandler):
        """
        Default class constructor.

        :param `menu`: an instance of :class:`FlatMenu` for which we want to redirect
         keyboard inputs;
        :param `oldHandler`: a previous (if any) :class:`EvtHandler` associated with
         the menu.
        """

        self._oldHandler = oldHandler
        self.SetMenu(menu)
        wx.EvtHandler.__init__(self)


    def SetMenu(self, menu):
        """
        Sets the listener menu.

        :param `menu`: an instance of :class:`FlatMenu`.
        """

        self._menu = menu


    def ProcessEvent(self, event):
        """
        Processes the inout event.

        :param `event`: any kind of keyboard-generated events.
        """

        if event.GetEventType() in [wx.EVT_KEY_DOWN, wx.EVT_CHAR, wx.EVT_CHAR_HOOK]:
            return self._menu.OnChar(event.GetKeyCode())
        else:
            return self._oldHandler.ProcessEvent(event)


#--------------------------------------------------------
# Class FocusHandler
#--------------------------------------------------------

class FocusHandler(wx.EvtHandler):
    """ A focus event handler. """

    def __init__(self, menu):
        """
        Default class constructor.

        :param `menu`: an instance of :class:`FlatMenu` for which we want to redirect
         focus inputs.
        """

        wx.EvtHandler.__init__(self)
        self.SetMenu(menu)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


    def SetMenu(self, menu):
        """
        Sets the listener menu.

        :param `menu`: an instance of :class:`FlatMenu`.
        """

        self._menu = menu


    def OnKeyDown(self, event):
        """
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`FocusHandler`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        # Let parent process it
        self._menu.OnKeyDown(event)


    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`FocusHandler`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        wx.PostEvent(self._menu, event)
