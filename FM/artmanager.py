"""
This module contains drawing routines and customizations for the AGW widgets
:class:`~wx.lib.agw.labelbook.LabelBook` and :class:`~wx.lib.agw.flatmenu.FlatMenu`.
"""

import wx
import random

from io import BytesIO

from .fmresources import *

# ---------------------------------------------------------------------------- #
# Class DCSaver
# ---------------------------------------------------------------------------- #

_ = wx.GetTranslation

class DCSaver(object):
    """
    Construct a DC saver. The dc is copied as-is.
    """

    def __init__(self, pdc):
        """
        Default class constructor.

        :param `pdc`: an instance of :class:`wx.DC`.
        """

        self._pdc = pdc
        self._pen = pdc.GetPen()
        self._brush = pdc.GetBrush()


    def __del__(self):
        """ While destructing, restores the dc pen and brush. """

        if self._pdc:
            self._pdc.SetPen(self._pen)
            self._pdc.SetBrush(self._brush)


# ---------------------------------------------------------------------------- #
# Class RendererBase
# ---------------------------------------------------------------------------- #

class RendererBase(object):
    """ Base class for all theme renderers. """

    def __init__(self):
        """ Default class constructor. Intentionally empty. """

        pass


    def DrawButtonBorders(self, dc, rect, penColour, brushColour):
        """
        Draws borders for buttons.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button's client rectangle;
        :param `penColour`: a valid :class:`wx.Colour` for the pen border;
        :param `brushColour`: a valid :class:`wx.Colour` for the brush.
        """

        # Keep old pen and brush
        dcsaver = DCSaver(dc)
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRectangle(rect)


    def DrawBitmapArea(self, dc, xpm_name, rect, baseColour, flipSide):
        """
        Draws the area below a bitmap and the bitmap itself using a gradient shading.

        :param `dc`: an instance of :class:`wx.DC`;
        :param string `xpm_name`: a name of a XPM bitmap;
        :param wx.Rect `rect`: the bitmap client rectangle;
        :param `baseColour`: a valid :class:`wx.Colour` for the bitmap background;
        :param bool `flipSide`: ``True`` to flip the gradient direction, ``False`` otherwise.
        """

        # draw the gradient area
        if not flipSide:
            ArtManager.Get().PaintDiagonalGradientBox(dc, rect, wx.WHITE,
                                                      ArtManager.Get().LightColour(baseColour, 20),
                                                      True, False)
        else:
            ArtManager.Get().PaintDiagonalGradientBox(dc, rect, ArtManager.Get().LightColour(baseColour, 20),
                                                      wx.WHITE, True, False)

        # draw arrow
        arrowDown = wx.Bitmap(xpm_name)
        arrowDown.SetMask(wx.Mask(arrowDown, wx.WHITE))
        dc.DrawBitmap(arrowDown, rect.x + 1 , rect.y + 1, True)


    def DrawBitmapBorders(self, dc, rect, penColour, bitmapBorderUpperLeftPen):
        """
        Draws borders for a bitmap.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button's client rectangle;
        :param `penColour`: a valid :class:`wx.Colour` for the pen border;
        :param `bitmapBorderUpperLeftPen`: a valid :class:`wx.Colour` for the pen upper
         left border.
        """

        # Keep old pen and brush
        dcsaver = DCSaver(dc)

        # lower right size
        dc.SetPen(wx.Pen(penColour))
        dc.DrawLine(rect.x, rect.y + rect.height - 1, rect.x + rect.width, rect.y + rect.height - 1)
        dc.DrawLine(rect.x + rect.width - 1, rect.y, rect.x + rect.width - 1, rect.y + rect.height)

        # upper left side
        dc.SetPen(wx.Pen(bitmapBorderUpperLeftPen))
        dc.DrawLine(rect.x, rect.y, rect.x + rect.width, rect.y)
        dc.DrawLine(rect.x, rect.y, rect.x, rect.y + rect.height)


    def GetMenuFaceColour(self):
        """
        Returns the foreground colour for the menu.

        :return: An instance of :class:`wx.Colour`.
        """

        return ArtManager.Get().LightColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE), 80)


    def GetTextColourEnable(self):
        """
        Returns the colour used for text colour when enabled.

        :return: An instance of :class:`wx.Colour`.
        """

        return wx.BLACK


    def GetTextColourDisable(self):
        """
        Returns the colour used for text colour when disabled.

        :return: An instance of :class:`wx.Colour`.
        """

        return ArtManager.Get().LightColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT), 30)


    def GetFont(self):
        """
        Returns the font used for text.

        :return: An instance of :class:`wx.Font`.
        """

        return wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)


# ---------------------------------------------------------------------------- #
# Class RendererXP
# ---------------------------------------------------------------------------- #

class RendererXP(RendererBase):
    """ Xp-Style renderer. """

    def __init__(self):
        """ Default class constructor. """

        RendererBase.__init__(self)


    def DrawButton(self, dc, rect, state, input=None):
        """
        Draws a button using the XP theme.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button's client rectangle;
        :param integer `state`: the button state;
        :param `input`: a flag used to call the right method.
        """

        if input is None or type(input) == type(False):
            self.DrawButtonTheme(dc, rect, state, input)
        else:
            self.DrawButtonColour(dc, rect, state, input)


    def DrawButtonTheme(self, dc, rect, state, useLightColours=None):
        """
        Draws a button using the XP theme.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button's client rectangle;
        :param integer `state`: the button state;
        :param bool `useLightColours`: ``True`` to use light colours, ``False`` otherwise.
        """

        # switch according to the status
        if state == ControlFocus:
            penColour = ArtManager.Get().FrameColour()
            brushColour = ArtManager.Get().BackgroundColour()
        elif state == ControlPressed:
            penColour = ArtManager.Get().FrameColour()
            brushColour = ArtManager.Get().HighlightBackgroundColour()
        else:
            penColour = ArtManager.Get().FrameColour()
            brushColour = ArtManager.Get().BackgroundColour()

        # Draw the button borders
        self.DrawButtonBorders(dc, rect, penColour, brushColour)


    def DrawButtonColour(self, dc, rect, state, colour):
        """
        Draws a button using the XP theme.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button's client rectangle;
        :param integer `state`: the button state;
        :param `colour`: a valid :class:`wx.Colour` instance.
        """

        # switch according to the status
        if statet == ControlFocus:
            penColour = colour
            brushColour = ArtManager.Get().LightColour(colour, 75)
        elif state == ControlPressed:
            penColour = colour
            brushColour = ArtManager.Get().LightColour(colour, 60)
        else:
            penColour = colour
            brushColour = ArtManager.Get().LightColour(colour, 75)

        # Draw the button borders
        self.DrawButtonBorders(dc, rect, penColour, brushColour)


    def GetTextColourEnable(self):
        """
        Returns the colour used for text colour when enabled.

        :return: An instance of :class:`wx.Colour`.
        """

        return wx.BLACK


# ---------------------------------------------------------------------------- #
# Class ArtManager
# ---------------------------------------------------------------------------- #

class ArtManager(wx.EvtHandler):

    """
    This class provides various art utilities, such as creating shadow, providing
    lighter / darker colours for a given colour, etc...
    """

    _alignmentBuffer = 7
    _menuTheme = StyleXP
    _verticalGradient = False
    _renderers = {StyleXP: None,}
    _bmpShadowEnabled = False
    _drowMBBorder = True
    _menuBgFactor = 5
    _menuBarColourScheme = _("Default")
    _raiseTB = True
    _bitmaps = {}
    _transparency = 255

    def __init__(self):
        """ Default class constructor. """

        wx.EvtHandler.__init__(self)
        self._menuBarBgColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        # connect an event handler to the system colour change event
        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSysColourChange)


    def ConvertToBitmap(self, xpm, alpha=None):
        """
        Convert the given image to a bitmap, optionally overlaying an alpha
        channel to it.

        :param `xpm`: a list of strings formatted as XPM;
        :type `xpm`: list of strings
        :param `alpha`: a list of alpha values, the same size as the xpm bitmap.
        :type `alpha`: list of integers

        :return: An instance of :class:`wx.Bitmap`.
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

            stream = BytesIO(xpm)
            img = wx.Image(stream)

        return wx.Bitmap(img)


    def Initialize(self):
        """ Initializes the bitmaps and colours. """

        # initialise the colour map
        self.InitColours()

        # Create common bitmaps
        self.FillStockBitmaps()


    def FillStockBitmaps(self):
        """ Initializes few standard bitmaps. """

        bmp = self.ConvertToBitmap(arrow_down, alpha=None)
        bmp.SetMask(wx.Mask(bmp, wx.Colour(0, 128, 128)))
        self._bitmaps.update({"arrow_down": bmp})

        bmp = self.ConvertToBitmap(arrow_up, alpha=None)
        bmp.SetMask(wx.Mask(bmp, wx.Colour(0, 128, 128)))
        self._bitmaps.update({"arrow_up": bmp})


    def GetStockBitmap(self, name):
        """
        Returns a bitmap from a stock.

        :param string `name`: the bitmap name.

        :return: The stock bitmap, if `name` was found in the stock bitmap dictionary.
         Otherwise, :class:`NullBitmap` is returned.
        """

        return self._bitmaps.get(name, wx.NullBitmap)


    def Get(self):
        """
        Accessor to the unique art manager object.

        :return: A unique instance of :class:`ArtManager`.
        """

        if not hasattr(self, "_instance"):

            self._instance = ArtManager()
            self._instance.Initialize()

            # Initialize the renderers map
            self._renderers[StyleXP] = RendererXP()

        return self._instance

    Get = classmethod(Get)

    def Free(self):
        """ Destructor for the unique art manager object. """

        if hasattr(self, "_instance"):

            del self._instance

    Free = classmethod(Free)


    def OnSysColourChange(self, event):
        """
        Handles the ``wx.EVT_SYS_COLOUR_CHANGED`` event for :class:`ArtManager`.

        :param `event`: a :class:`SysColourChangedEvent` event to be processed.
        """

        # reinitialise the colour map
        self.InitColours()


    def LightColour(self, colour, percent):
        """
        Return light contrast of `colour`. The colour returned is from the scale of
        `colour` ==> white.

        :param `colour`: the input colour to be brightened, an instance of :class:`wx.Colour`;
        :param integer `percent`: determines how light the colour will be. `percent` = ``100``
         returns white, `percent` = ``0`` returns `colour`.

        :return: A light contrast of the input `colour`, an instance of :class:`wx.Colour`.
        """

        end_colour = wx.WHITE
        rd = end_colour.Red() - colour.Red()
        gd = end_colour.Green() - colour.Green()
        bd = end_colour.Blue() - colour.Blue()
        high = 100

        # We take the percent way of the colour from colour -. white
        i = percent
        r = colour.Red() + ((i*rd*100)/high)/100
        g = colour.Green() + ((i*gd*100)/high)/100
        b = colour.Blue() + ((i*bd*100)/high)/100
        a = colour.Alpha()

        return wx.Colour(int(r), int(g), int(b), int(a))


    def PaintStraightGradientBox(self, dc, rect, startColour, endColour, vertical=True):
        """
        Paint the rectangle with gradient colouring; the gradient lines are either
        horizontal or vertical.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the rectangle to be filled with gradient shading;
        :param wx.Colour `startColour`: the first colour of the gradient shading;
        :param wx.Colour `endColour`: the second colour of the gradient shading;
        :param bool `vertical`: ``True`` for gradient colouring in the vertical direction,
         ``False`` for horizontal shading.
        """

        dcsaver = DCSaver(dc)

        if vertical:
            high = rect.GetHeight()-1
            direction = wx.SOUTH
        else:
            high = rect.GetWidth()-1
            direction = wx.EAST

        if high < 1:
            return

        dc.GradientFillLinear(rect, startColour, endColour, direction)


    def PaintDiagonalGradientBox(self, dc, rect, startColour, endColour,
                                 startAtUpperLeft=True, trimToSquare=True):
        """
        Paint rectangle with gradient colouring; the gradient lines are diagonal
        and may start from the upper left corner or from the upper right corner.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the rectangle to be filled with gradient shading;
        :param wx.Colour `startColour`: the first colour of the gradient shading;
        :param wx.Colour `endColour`: the second colour of the gradient shading;
        :param bool `startAtUpperLeft`: ``True`` to start the gradient lines at the upper
         left corner of the rectangle, ``False`` to start at the upper right corner;
        :param bool `trimToSquare`: ``True`` to trim the gradient lines in a square.
        """

        # Save the current pen and brush
        savedPen = dc.GetPen()
        savedBrush = dc.GetBrush()

        # gradient fill from colour 1 to colour 2 with top to bottom
        if rect.height < 1 or rect.width < 1:
            return

        # calculate some basic numbers
        size = rect.width
        sizeX = sizeY = 0
        proportion = 1

        if rect.width > rect.height:

            if trimToSquare:

                size = rect.height
                sizeX = sizeY = rect.height - 1

            else:

                proportion = float(rect.height)/float(rect.width)
                size = rect.width
                sizeX = rect.width - 1
                sizeY = rect.height -1

        else:

            if trimToSquare:

                size = rect.width
                sizeX = sizeY = rect.width - 1

            else:

                sizeX = rect.width - 1
                size = rect.height
                sizeY = rect.height - 1
                proportion = float(rect.width)/float(rect.height)

        # calculate gradient coefficients
        col2 = endColour
        col1 = startColour

        rf, gf, bf = 0, 0, 0
        rstep = float(col2.Red() - col1.Red())/float(size)
        gstep = float(col2.Green() - col1.Green())/float(size)
        bstep = float(col2.Blue() - col1.Blue())/float(size)

        # draw the upper triangle
        for i in range(size):

            currCol = wx.Colour(col1.Red() + rf, col1.Green() + gf, col1.Blue() + bf)
            dc.SetBrush(wx.Brush(currCol, wx.BRUSHSTYLE_SOLID))
            dc.SetPen(wx.Pen(currCol))

            if startAtUpperLeft:

                if rect.width > rect.height:

                    dc.DrawLine(rect.x + i, rect.y, rect.x, int(rect.y + proportion*i))
                    dc.DrawPoint(rect.x, int(rect.y + proportion*i))

                else:

                    dc.DrawLine(int(rect.x + proportion*i), rect.y, rect.x, rect.y + i)
                    dc.DrawPoint(rect.x, rect.y + i)

            else:

                if rect.width > rect.height:

                    dc.DrawLine(rect.x + sizeX - i, rect.y, rect.x + sizeX, int(rect.y + proportion*i))
                    dc.DrawPoint(rect.x + sizeX, int(rect.y + proportion*i))

                else:

                    xTo = (int(rect.x + sizeX - proportion * i) > rect.x and [int(rect.x + sizeX - proportion*i)] or [rect.x])[0]
                    dc.DrawLine(xTo, rect.y, rect.x + sizeX, rect.y + i)
                    dc.DrawPoint(rect.x + sizeX, rect.y + i)

            rf += rstep/2
            gf += gstep/2
            bf += bstep/2

        # draw the lower triangle
        for i in range(size):

            currCol = wx.Colour(col1.Red() + rf, col1.Green() + gf, col1.Blue() + bf)
            dc.SetBrush(wx.Brush(currCol, wx.BRUSHSTYLE_SOLID))
            dc.SetPen(wx.Pen(currCol))

            if startAtUpperLeft:

                if rect.width > rect.height:

                    dc.DrawLine(rect.x + i, rect.y + sizeY, rect.x + sizeX, int(rect.y + proportion * i))
                    dc.DrawPoint(rect.x + sizeX, int(rect.y + proportion * i))

                else:

                    dc.DrawLine(int(rect.x + proportion * i), rect.y + sizeY, rect.x + sizeX, rect.y + i)
                    dc.DrawPoint(rect.x + sizeX, rect.y + i)

            else:

                if rect.width > rect.height:

                    dc.DrawLine(rect.x, (int)(rect.y + proportion * i), rect.x + sizeX - i, rect.y + sizeY)
                    dc.DrawPoint(rect.x + sizeX - i, rect.y + sizeY)

                else:

                    xTo = (int(rect.x + sizeX - proportion*i) > rect.x and [int(rect.x + sizeX - proportion*i)] or [rect.x])[0]
                    dc.DrawLine(rect.x, rect.y + i, xTo, rect.y + sizeY)
                    dc.DrawPoint(xTo, rect.y + sizeY)

            rf += rstep/2
            gf += gstep/2
            bf += bstep/2


        # Restore the pen and brush
        dc.SetPen( savedPen )
        dc.SetBrush( savedBrush )


    def FrameColour(self):
        """
        Return the surrounding colour for a control.

        :return: An instance of :class:`wx.Colour`.
        """

        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)


    def BackgroundColour(self):
        """
        Returns the background colour of a control when not in focus.

        :return: An instance of :class:`wx.Colour`.
        """

        return self.LightColour(self.FrameColour(), 75)


    def HighlightBackgroundColour(self):
        """
        Returns the background colour of a control when it is in focus.

        :return: An instance of :class:`wx.Colour`.
        """

        return self.LightColour(self.FrameColour(), 60)


    def IsDark(self, colour):
        """
        Returns whether a colour is dark or light.

        :param `colour`: an instance of :class:`wx.Colour`.

        :return: ``True`` if the average RGB values are dark, ``False`` otherwise.
        """

        evg = (colour.Red() + colour.Green() + colour.Blue())/3

        if evg < 127:
            return True

        return False


    def TruncateText(self, dc, text, maxWidth):
        """
        Truncates a given string to fit given width size. if the text does not fit
        into the given width it is truncated to fit. The format of the fixed text
        is ``truncate text ...``.

        :param `dc`: an instance of :class:`wx.DC`;
        :param string `text`: the text to be (eventually) truncated;
        :param integer `maxWidth`: the maximum width allowed for the text.

        :return: A new string containing the (possibly) truncated text.
        """

        textLen = len(text)
        tempText = text
        rectSize = maxWidth

        fixedText = ""

        textW, textH = dc.GetTextExtent(text)

        if rectSize >= textW:
            return text

        # The text does not fit in the designated area,
        # so we need to truncate it a bit
        suffix = ".."
        w, h = dc.GetTextExtent(suffix)
        rectSize -= w

        for i in range(textLen, -1, -1):

            textW, textH = dc.GetTextExtent(tempText)
            if rectSize >= textW:
                fixedText = tempText
                fixedText += ".."
                return fixedText

            tempText = tempText[:-1]


    def DrawButton(self, dc, rect, theme, state, input=None):
        """
        Colour rectangle according to the theme.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the rectangle to be filled with gradient shading;
        :param string `theme`: the theme to use to draw the button;
        :param integer `state`: the button state;
        :param `input`: a flag used to call the right method.
        """

        if input is None or type(input) == type(False):
            self.DrawButtonTheme(dc, rect, theme, state, input)
        else:
            self.DrawButtonColour(dc, rect, theme, state, input)


    def DrawButtonTheme(self, dc, rect, theme, state, useLightColours=True):
        """
        Draws a button using the appropriate theme.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button's client rectangle;
        :param string `theme`: the theme to use to draw the button;
        :param integer `state`: the button state;
        :param bool  `useLightColours`: ``True`` to use light colours, ``False`` otherwise.
        """

        renderer = self._renderers[theme]

        # Set background colour if non given by caller
        renderer.DrawButton(dc, rect, state, useLightColours)


    def DrawButtonColour(self, dc, rect, theme, state, colour):
        """
        Draws a button using the appropriate theme.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the button's client rectangle;
        :param string `theme`: the theme to use to draw the button;
        :param integer `state`: the button state;
        :param `colour`: a valid :class:`wx.Colour` instance.
        """

        renderer = self._renderers[theme]
        renderer.DrawButton(dc, rect, state, colour)


    def GetBitmapStartLocation(self, dc, rect, bitmap, text="", style=0):
        """
        Returns the top left `x` and `y` coordinates of the bitmap drawing.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the bitmap's client rectangle;
        :param wx.Bitmap `bitmap`: the bitmap associated with the button;
        :param string `text`: the button label;
        :param integer `style`: the button style. This can be one of the following bits:

         ============================== ======= ================================
         Button style                    Value  Description
         ============================== ======= ================================
         ``BU_EXT_XP_STYLE``               1    A button with a XP style
         ``BU_EXT_LEFT_ALIGN_STYLE``       4    A left-aligned button
         ``BU_EXT_CENTER_ALIGN_STYLE``     8    A center-aligned button
         ``BU_EXT_RIGHT_ALIGN_STYLE``      16   A right-aligned button
         ``BU_EXT_RIGHT_TO_LEFT_STYLE``    32   A button suitable for right-to-left languages
         ============================== ======= ================================

        :return: A tuple containing the top left `x` and `y` coordinates of the bitmap drawing.
        """

        alignmentBuffer = self.GetAlignBuffer()

        # get the startLocationY
        fixedTextWidth = fixedTextHeight = 0

        if not text:
            fixedTextHeight = bitmap.GetHeight()
        else:
            fixedTextWidth, fixedTextHeight = dc.GetTextExtent(text)

        startLocationY = rect.y + (rect.height - fixedTextHeight)/2

        # get the startLocationX
        if style & BU_EXT_RIGHT_TO_LEFT_STYLE:

            startLocationX = rect.x + rect.width - alignmentBuffer - bitmap.GetWidth()

        else:

            if style & BU_EXT_RIGHT_ALIGN_STYLE:

                maxWidth = rect.x + rect.width - (2 * alignmentBuffer) - bitmap.GetWidth() # the alignment is for both sides

                # get the truncated text. The text may stay as is, it is not a must that is will be trancated
                fixedText = self.TruncateText(dc, text, maxWidth)

                # get the fixed text dimensions
                fixedTextWidth, fixedTextHeight = dc.GetTextExtent(fixedText)

                # calculate the start location
                startLocationX = maxWidth - fixedTextWidth

            elif style & BU_EXT_LEFT_ALIGN_STYLE:

                # calculate the start location
                startLocationX = alignmentBuffer

            else: # meaning BU_EXT_CENTER_ALIGN_STYLE

                maxWidth = rect.x + rect.width - (2 * alignmentBuffer) - bitmap.GetWidth() # the alignment is for both sides

                # get the truncated text. The text may stay as is, it is not a must that is will be trancated
                fixedText = self.TruncateText(dc, text, maxWidth)

                # get the fixed text dimensions
                fixedTextWidth, fixedTextHeight = dc.GetTextExtent(fixedText)

                if maxWidth > fixedTextWidth:

                    # calculate the start location
                    startLocationX = (maxWidth - fixedTextWidth) / 2

                else:

                    # calculate the start location
                    startLocationX = maxWidth - fixedTextWidth

        # it is very important to validate that the start location is not less than the alignment buffer
        if startLocationX < alignmentBuffer:
            startLocationX = alignmentBuffer

        return startLocationX, startLocationY


    def GetTextStartLocation(self, dc, rect, bitmap, text, style=0):
        """
        Returns the top left `x` and `y` coordinates of the text drawing.
        In case the text is too long, the text is being fixed (the text is cut and
        a '...' mark is added in the end).

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the text's client rectangle;
        :param wx.Bitmap `bitmap`: the bitmap associated with the button;
        :param string `text`: the button label;
        :param integer `style`: the button style.

        :return: A tuple containing the top left `x` and `y` coordinates of the text drawing, plus
         the truncated version of the input `text`.

        :see: :meth:`~ArtManager.GetBitmapStartLocation` for a list of valid button styles.
        """

        alignmentBuffer = self.GetAlignBuffer()

        # get the bitmap offset
        bitmapOffset = 0
        if bitmap != wx.NullBitmap:
            bitmapOffset = bitmap.GetWidth()

        # get the truncated text. The text may stay as is, it is not a must that is will be trancated
        maxWidth = rect.x + rect.width - (2 * alignmentBuffer) - bitmapOffset # the alignment is for both sides

        fixedText = self.TruncateText(dc, text, maxWidth)

        # get the fixed text dimensions
        fixedTextWidth, fixedTextHeight = dc.GetTextExtent(fixedText)
        startLocationY = (rect.height - fixedTextHeight) / 2 + rect.y

        # get the startLocationX
        if style & BU_EXT_RIGHT_TO_LEFT_STYLE:

            startLocationX = maxWidth - fixedTextWidth + alignmentBuffer

        else:

            if style & BU_EXT_LEFT_ALIGN_STYLE:

                # calculate the start location
                startLocationX = bitmapOffset + alignmentBuffer

            elif style & BU_EXT_RIGHT_ALIGN_STYLE:

                # calculate the start location
                startLocationX = maxWidth - fixedTextWidth + bitmapOffset + alignmentBuffer

            else: # meaning wxBU_EXT_CENTER_ALIGN_STYLE

                # calculate the start location
                startLocationX = (maxWidth - fixedTextWidth) / 2 + bitmapOffset + alignmentBuffer


        # it is very important to validate that the start location is not less than the alignment buffer
        if startLocationX < alignmentBuffer:
            startLocationX = alignmentBuffer

        return startLocationX, startLocationY, fixedText


    def GetMenuFaceColour(self):
        """
        Returns the colour used for the menu foreground.

        :return: An instance of :class:`wx.Colour`.
        """

        renderer = self._renderers[self.GetMenuTheme()]
        return renderer.GetMenuFaceColour()


    def GetTextColourEnable(self):
        """
        Returns the colour used for enabled menu items.

        :return: An instance of :class:`wx.Colour`.
        """

        renderer = self._renderers[self.GetMenuTheme()]
        return renderer.GetTextColourEnable()


    def GetTextColourDisable(self):
        """
        Returns the colour used for disabled menu items.

        :return: An instance of :class:`wx.Colour`.
        """

        renderer = self._renderers[self.GetMenuTheme()]
        return renderer.GetTextColourDisable()


    def GetFont(self):
        """
        Returns the font used by this theme.

        :return: An instance of :class:`wx.Font`.
        """

        renderer = self._renderers[self.GetMenuTheme()]
        return renderer.GetFont()


    def GetAccelIndex(self, label):
        """
        Returns the mnemonic index of the label and the label stripped of the ampersand mnemonic
        (e.g. 'lab&el' ==> will result in 3 and labelOnly = label).

        :param string `label`: a string containing an ampersand.

        :return: A tuple containing the mnemonic index of the label and the label
         stripped of the ampersand mnemonic.
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


    def GetAlignBuffer(self):
        """
        Return the padding buffer for a text or bitmap.

        :return: An integer representing the padding buffer.
        """

        return self._alignmentBuffer


    def GetMenuTheme(self):
        """
        Returns the currently used menu theme.

        :return: A string containing the currently used theme for the menu.
        """

        return self._menuTheme


    def InitColours(self):
        """ Initialise the colour map. """

        self._colourSchemeMap = {_("Default"): wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE),
                                 _("Dark"): wx.BLACK,
                                 _("Dark Olive Green"): wx.Colour("DARK OLIVE GREEN"),
                                 _("Generic"): wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)}
