#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# $LastChangedRevision$
# $HeadURL$

"""
Module for the RPM-style meter.
"""

import wx
import SpeedMeter as SM
from math import pi, sqrt
import wx.gizmos as gizmos
from pyOBD_Meters_Constants import pyOBD_Meters_Constants as CONST


"""
@todo: need to modify speed meter for bottom and/or top text
"""

class pyOBD_Meters_RPM():
    """
    Creates a RPM-style meter. Wrapper around SpeedMeter that sets up a meter with the right
    settings, look, etc. for a RPM gauge. Sets up the labels and handles scaling of values.
    """

    staticText = "" # text shown on the meter that doesn't change - label
    led = None # variable for the LEDNumberControl
    currentValue = 0

    def __init__(self, myPanel):
        """
        Initialize the meter, set everything up.
        
        @param myPanel: a wx.Panel that the meter will be in
        @type myPanel: L{wx.Panel}
        """

        # Fifth SpeedMeter: We Use The Following Styles:
        #
        # SM_DRAW_HAND: We Want To Draw The Hand (Arrow) Indicator
        # SM_DRAW_PARTIAL_SECTORS: Partial Sectors Will Be Drawn, To Indicate Different Intervals
        # SM_DRAW_SECONDARY_TICKS: We Draw Secondary (Intermediate) Ticks Between
        #                          The Main Ticks (Intervals)
        # SM_DRAW_MIDDLE_TEXT: We Draw Some Text In The Center Of SpeedMeter
        # SM_ROTATE_TEXT: The Ticks Texts Are Rotated Accordingly To Their Angle
        
        self.GaugeWindow = SM.SpeedMeter(myPanel,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_BOTTOM_TEXT
                                          )

        # We Want To Simulate The Round Per Meter Control In A Car
        self.GaugeWindow.SetAngleRange(-pi/6, 7*pi/6)

        intervals = range(0, 5)
        self.GaugeWindow.SetIntervals(intervals)

        colours = [CONST.M_LARGE_BG_COLOR]*3
        colours.append(wx.RED)
        self.GaugeWindow.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        self.GaugeWindow.SetTicks(ticks)
        self.GaugeWindow.SetTicksColour(CONST.M_LARGE_TICK_COLOR)
        self.GaugeWindow.SetTicksFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.GaugeWindow.SetHandColour(wx.Colour(255, 50, 0))

        self.GaugeWindow.SetSpeedBackground(CONST.M_LARGE_BG_COLOR)

        """@todo: this doesn't seem to be working."""
        self.GaugeWindow.SetArcColour(CONST.M_LARGE_ARC_COLOR)
        self.GaugeWindow.DrawExternalCircle(True)

        self.GaugeWindow.SetShadowColour(wx.Colour(50, 0, 0))

        #self.GaugeWindow.SetMiddleText("rpm")
        #self.GaugeWindow.SetMiddleTextColour(wx.WHITE)
        #self.GaugeWindow.SetMiddleTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.staticText = "RPM x1000"
        self.GaugeWindow.SetBottomText(self.staticText)
        self.GaugeWindow.SetBottomTextColour(CONST.M_LARGE_TEXT_COLOR)
        self.GaugeWindow.SetBottomTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.GaugeWindow.SetSpeedBackground(CONST.M_LARGE_BG_COLOR) 
        
        self.GaugeWindow.SetSpeedValue(.68)

    def getSpeedWindow(self):
        """
        Returns the SpeedMeter instance that we created, so we can add it to a Panel, etc.
        @return: SpeedMeter
        @rtype: L{SpeedMeter}
        """
        return self.GaugeWindow

    def SetText(self, text=None):
        """
        Sets The Text To Be Drawn Near The Center Of SpeedMeter (MiddleText).
        @param text: the text to be drawn
        @type text: C{string}
        """
        
        if text is None:
            text = ""

        self.GaugeWindow._middletext = text

    def SetValue(self, value=None):
        """
        Sets the value of the meter (where the needle points). Sets the text value display if used and enabled.
        @param value: Value for the meter.
        @type value: C{int} or C{float}

        @todo: led stuff was moved here so the SpeedMeter has completed its init.
        """
        if value is None:
            return
        else:
            self.currentValue = value
            self.GaugeWindow.SetSpeedValue(value)
            
            if self.led is None:
                # LED number control
                pos = (self.GaugeWindow.GetWidth()/2 - 60, self.GaugeWindow.GetBottomTextBottom())
                size = (120, 30)
                style = gizmos.LED_ALIGN_CENTER | wx.NO_BORDER
                self.led = gizmos.LEDNumberCtrl(self.getSpeedWindow(), -1, pos, size, style)
                self.led.SetBackgroundColour(CONST.M_LARGE_BG_COLOR)
                self.led.SetForegroundColour(CONST.M_LARGE_LED_COLOR)
                print self.led.GetBorder()
                print wx.NO_BORDER

            self.led.SetValue(str(int(value*1000)))

    def GetValue(self):
        """
        Gets the meter's current value.

        @return: value
        @rtype: C{float}
        """
        return self.currentValue
