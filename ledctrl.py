#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# $LastChangedRevision: 8 $
# $HeadURL: http://svn.jasonantman.com/pyOBD/pyOBD_Meters_RPM.py $

"""
Pure Python rewrite of the wxCode.gadgets.ledctrl class
"""

import wx
from SpeedMeter import BufferedWindow as BufferedWindow
import wx.gizmos as gizmos

class ledctrl(BufferedWindow):
    """
    Creates a LEDctrl object
    """

    DEBUG = True

    LINE1 = 1
    LINE2 = 2
    LINE3 = 4
    LINE4 = 8
    LINE5 = 16
    LINE6 = 32
    LINE7 = 64
    DECIMALSIGN = 128

    DIGIT0 = LINE1 | LINE2 | LINE3 | LINE4 | LINE5 | LINE6
    DIGIT1 = LINE2 | LINE3
    DIGIT2 = LINE1 | LINE2 | LINE4 | LINE5 | LINE7
    DIGIT3 = LINE1 | LINE2 | LINE3 | LINE4 | LINE7
    DIGIT4 = LINE2 | LINE3 | LINE6 | LINE7
    DIGIT5 = LINE1 | LINE3 | LINE4 | LINE6 | LINE7
    DIGIT6 = LINE1 | LINE3 | LINE4 | LINE5 | LINE6 | LINE7
    DIGIT7 = LINE1 | LINE2 | LINE3
    DIGIT8 = LINE1 | LINE2 | LINE3 | LINE4 | LINE5 | LINE6 | LINE7
    DIGIT9 = LINE1 | LINE2 | LINE3 | LINE6 | LINE7
    DASH   = LINE7

    DIGITALL = -1

    SM_NORMAL_DC = 0
    SM_BUFFERED_DC = 1

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, bufferedstyle=SM_BUFFERED_DC):
        """
        Default Class Constructor.

        """

        self._bufferedstyle = bufferedstyle
        self.SetBackgroundColour()
        self.SetValue()
        self.SetAlignment()
        self.SetDrawFaded()
        self.InitInternals()

        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                bufferedstyle=bufferedstyle)


    def SetAlignment(self, Alignment=None, Redraw=False):
        """
        Sets LED digit alignment.
        
        @param Alignment
        @type Alignment: wxLEDValueAlign
        @type Redraw: C{boolean}
        """
        if Alignment is None:
            self._Alignment = Alignment

        if Alignment != self._Alignment:
            self._Alignment = Alignment
            RecalcInternals(self.GetClientSize())
            if Redraw:
                Refresh(false)
                
    def SetDrawFaded(self, DrawFaded=None, Redraw=False):
        """
        @type DrawFaded: C{boolean}
        @type Redraw: C{boolean}
        """

        if DrawFaded is None:
            self._DrawFaded = DrawFaded

        if DrawFaded != self._DrawFaded:
            self._DrawFaded = DrawFaded
            if Redraw:
                Refresh(False)

    def SetValue(self, value=None):
        """ Sets The Current Value For SpeedMeter. """

        print value
        if value is None:
            self._value = ""
        elif value != self._value:
            self._value = value
            self.RecalcInternals(self.GetClientSize())
            try:
                self.UpdateDrawing()
            except:
                pass

    def SetBackgroundColour(self, colour=None):
        """ Sets The Background Colour Outside The SpeedMeter Control."""
        
        if colour is None:
            colour = wx.SystemSettings_GetColour(0)

        self._backgroundcolour = colour

    def GetBackgroundColour(self):
        """ Gets The Background Colour Outside The SpeedMeter Control."""

        return self._backgroundcolour

    def Draw(self, dc):
        """ Draws Everything On The Empty Bitmap.

        Here All The Chosen Styles Are Applied. """

        size = self.GetClientSize()
        Width = size.x
        Height = size.y

        self.RecalcInternals(size)

        new_dim = size.Get()
        
        if not hasattr(self, "dim"):
            self.dim = new_dim

        self.faceBitmap = wx.EmptyBitmap(size.width, size.height)
        
        dc.BeginDrawing()

        #wxBitmap *pMemoryBitmap = new wxBitmap(Width, Height);
        #wxMemoryDC MemDc;
        #MemDc.SelectObject(*pMemoryBitmap);

        
        # Draw background.

        #background = self.GetBackgroundColour()
        #dc.SetBackground(wx.Brush(background))
        # BEGIN SEBUG
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255), wx.TRANSPARENT))
        # END DEBUG
        dc.Clear()

        #c.SetBrush(wxBrush(GetBackgroundColour(), wxSOLID));
        #MemDc.DrawRectangle(wxRect(0, 0, size.width, size.height));
        #MemDc.SetBrush(wxNullBrush);

        # Iterate each digit in the value, and draw.
        for i in range(len(self._value)):
            c = self._value[i]

            if self.DEBUG:
                print "Digit Number: " + str(i)
                print "Drawing Digit: " + c

            # Draw faded lines if wanted.
            if self._DrawFaded and (c != '.'):
                self.DrawDigit(dc, self.DIGITALL, i)
                
            # Draw the digits.
            if c == '0':
                self.DrawDigit(dc, self.DIGIT0, i)
            elif c == '1':
                self.DrawDigit(dc, self.DIGIT1, i)
            elif c == '2':
                self.DrawDigit(dc, self.DIGIT2, i)
            elif c == '3':
                self.DrawDigit(dc, self.DIGIT3, i)
            elif c == '4':
                self.DrawDigit(dc, self.DIGIT4, i)
            elif c == '5':
                self.DrawDigit(dc, self.DIGIT5, i)
            elif c == '6':
                self.DrawDigit(dc, self.DIGIT6, i)
            elif c == '7':
                self.DrawDigit(dc, self.DIGIT7, i)
            elif c == '8':
                self.DrawDigit(dc, self.DIGIT8, i)
            elif c == '9':
                self.DrawDigit(dc, self.DIGIT9, i)
            elif c == '-':
                self.DrawDigit(dc, self.DASH, i)
            elif c == '.':
                self.DrawDigit(dc, self.DECIMALSIGN, (i-1))
            elif c == ' ':
                # skip this
                pass
            else:
                print "Error: Undefined Digit Value: " + c
                
            """
            { '0' : self.DrawDigit(dc, self.DIGIT0, i),
              '1' : self.DrawDigit(dc, self.DIGIT1, i),
              '2' : self.DrawDigit(dc, self.DIGIT2, i),
              '3' : self.DrawDigit(dc, self.DIGIT3, i),
              '4' : self.DrawDigit(dc, self.DIGIT4, i),
              '5' : self.DrawDigit(dc, self.DIGIT5, i),
              '6' : self.DrawDigit(dc, self.DIGIT6, i),
              '7' : self.DrawDigit(dc, self.DIGIT7, i),
              '8' : self.DrawDigit(dc, self.DIGIT8, i),
              '9' : self.DrawDigit(dc, self.DIGIT9, i),
              '-' : self.DrawDigit(dc, self.DASH, i),
              '.' : self.DrawDigit(dc, self.DECIMALSIGN, (i-1))}[c]()
            """
            # case _T(' ') :   break; (skip this)
            # undefined case: error message "Unknown digit value"

        #dc.EndDrawing()
        # Blit the memory dc to screen.
        #Dc.Blit(0, 0, Width, Height, &MemDc, 0, 0, wxCOPY);
        #delete pMemoryBitmap;

    def DrawDigit(self, dc, Digit, Column):
        """

        """
        
        LineColor = self.GetForegroundColour()

        if Digit == self.DIGITALL:
            R = LineColor.Red() / 16
            G = LineColor.Green() / 16
            B = LineColor.Blue() / 16
            LineColor = wx.Colour(R, G, B)

        XPos = self._LeftStartPos + (Column * (self._LineLength + self._DigitMargin))

        # Create a pen and draw the lines.
        Pen = wx.Pen(LineColor, self._LineWidth, wx.SOLID)
        dc.SetPen(Pen)

        if Digit & self.LINE1:
            dc.DrawLine(XPos + self._LineMargin*2, self._LineMargin, 
                        XPos + self._LineLength + self._LineMargin*2, self._LineMargin)
            if self.DEBUG:
                print "Line1"

        if Digit & self.LINE2:
            dc.DrawLine(XPos + self._LineLength + self._LineMargin*3, 
                        self._LineMargin*2, XPos + self._LineLength + self._LineMargin*3, 
                        self._LineLength + (self._LineMargin*2))
            if self.DEBUG:
                print "Line2"

        if Digit & self.LINE3:
            dc.DrawLine(XPos + self._LineLength + self._LineMargin*3, self._LineLength + (self._LineMargin*4),
                        XPos + self._LineLength + self._LineMargin*3, self._LineLength*2 + (self._LineMargin*4))
            if self.DEBUG:
                print "Line3"

        if Digit & self.LINE4:
            dc.DrawLine(XPos + self._LineMargin*2, self._LineLength*2 + (self._LineMargin*5),
                        XPos + self._LineLength + self._LineMargin*2, self._LineLength*2 + (self._LineMargin*5))
            if self.DEBUG:
                print "Line4"

        if Digit & self.LINE5:
            dc.DrawLine(XPos + self._LineMargin, self._LineLength + (self._LineMargin*4),
                        XPos + self._LineMargin, self._LineLength*2 + (self._LineMargin*4))
            if self.DEBUG:
                print "Line5"

        if Digit & self.LINE6:
            dc.DrawLine(XPos + self._LineMargin, self._LineMargin*2,
                        XPos + self._LineMargin, self._LineLength + (self._LineMargin*2))
            if self.DEBUG:
                print "Line6"

        if Digit & self.LINE7:
            dc.DrawLine(XPos + self._LineMargin*2, self._LineLength + (self._LineMargin*3),
                        XPos + self._LineMargin*2 + self._LineLength, self._LineLength + (self._LineMargin*3))
            if self.DEBUG:
                print "Line7"

        if Digit & self.DECIMALSIGN:
            dc.DrawLine(XPos + self._LineLength + self._LineMargin*4, self._LineLength*2 + (self._LineMargin*5),
                        XPos + self._LineLength + self._LineMargin*4, self._LineLength*2 + (self._LineMargin*5))
            if self.DEBUG:
                print "Line DecimalSign"

        #Dc.SetPen(wxNullPen);

    def RecalcInternals(self, CurrentSize):
        """
        Dimensions of LED segments
        
        Size of character is based on the HEIGH of the widget, NOT the width.
        Segment height is calculated as follows:
        Each segment is m_LineLength pixels long.
        There is m_LineMargin pixels at the top and bottom of each line segment
        There is m_LineMargin pixels at the top and bottom of each digit
        
        Therefore, the heigth of each character is:
        m_LineMargin                            : Top digit boarder
        m_LineMargin+m_LineLength+m_LineMargin  : Top half of segment
        m_LineMargin+m_LineLength+m_LineMargin  : Bottom half of segment
        m_LineMargin                            : Bottom digit boarder
        ----------------------
        m_LineMargin*6 + m_LineLength*2 == Total height of digit.
        Therefore, (m_LineMargin*6 + m_LineLength*2) must equal Height
        
        Spacing between characters can then be calculated as follows:
        m_LineMargin                            : before the digit,
        m_LineMargin+m_LineLength+m_LineMargin  : for the digit width
        m_LineMargin                            : after the digit
        = m_LineMargin*4 + m_LineLength
        """
        Height = CurrentSize.GetHeight()

        if (Height * 0.075) < 1:
            self._LineMargin = 1
        else:
            self._LineMargin = int(Height * 0.075)

        if (Height * 0.275) < 1:
            self._LineLength = 1
        else:
            self._LineLength = int(Height * 0.275)

        self._LineWidth = self._LineMargin

        self._DigitMargin = self._LineMargin * 4

        # Count the number of characters in the string; '.' characters are not
        # included because they do not take up space in the display
        count = 0;
        for char in self._value:
            if char != '.':
                count = count + 1

        ValueWidth = (self._LineLength + self._DigitMargin) * count
        ClientWidth = CurrentSize.GetWidth()

        if self._Alignment == gizmos.LED_ALIGN_LEFT:
            self._LeftStartPos = self._LineMargin
        elif self._Alignment == gizmos.LED_ALIGN_RIGHT:
            self._LeftStartPos = ClientWidth - ValueWidth - self._LineMargin
        else:
            # self._Alignment == gizmos.LED_ALIGN_CENTER:
            # centered is the default
            self._LeftStartPos = (ClientWidth - ValueWidth) / 2

    def InitInternals(self):
        """

        """
        self._LineMargin = None
        self._LineLength = None
        self._LineWidth = None
        self._DigitMargin = None
        self._LeftStartPos = None


