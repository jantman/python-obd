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

class pyOBD_Meters_RPM():
    """
    Creates a RPM-style meter. Wrapper around SpeedMeter that sets up a meter with the right
    settings, look, etc. for a RPM gauge. Sets up the labels and handles scaling of values.
    
    Includes an LED digit display at the bottom of the meter.
    """

    _currentValue = 0

    def __init__(self, myPanel, minVal=0, maxVal=100, scaleDivisor=1, redLine=-1):
        """
        Initialize the meter, set everything up.
        
        @param myPanel: a wx.Panel that the meter will be in
        @type myPanel: L{wx.Panel}
        @param minVal: The minimum (starting) value for the scale, default=0
        @type minVal: L{int} or L{float}
        @param maxVal: The maximum (ending) value for the scale, default=100
        @type maxVal: L{int} or L{float}
        @param scaleDivisor: Scale will show values divided by this number (i.e. an RPMx1000 scale from 0-4000 RPM should have minVal=0, maxVal=4, scaleDivisor=1000)
        @type scaleDivisor: L{int} or L{float}
        @param redLine: The actual value (not including scaleDivisor calculation) of the interval mark starting the redline. Default=1. Value of -1 will yield no redline.
        @type redLine: L{int} or L{float}
        """

        self.GaugeWindow = SM.SpeedMeter(myPanel,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_BOTTOM_TEXT |
                                          SM.SM_DRAW_BOTTOM_LED
                                          )

        # todo - we should reall handle this here, NOT in SpeedMeter?
        # todo - OR we NEED to re-do this in SpeedMeter to be more logical.
        # this class (and maybe SpeedMeter too) should just take a value (or minVal, maxVal) and a scaleDivisor and figure it out.
        self.GaugeWindow.SetValueMultiplier(1000)


        self.GaugeWindow.SetLEDAlignment(gizmos.LED_ALIGN_CENTER)


        # todo - this needs to be programmatic, we should have methods (or constructor params) for intervals, colours, etc.
        # We Want To Simulate The Round Per Meter Control In A Car
        self.GaugeWindow.SetAngleRange(-pi/6, 7*pi/6)

        # todo - this needs to be programmatic, we should have methods (or constructor params) for intervals, colours, etc.
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

        self.GaugeWindow.SetBottomTextColour(CONST.M_LARGE_TEXT_COLOR)
        self.GaugeWindow.SetBottomTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.GaugeWindow.SetBottomText("RPM x1000")

        self.GaugeWindow.SetSpeedBackground(CONST.M_LARGE_BG_COLOR) 
        
        self.GaugeWindow.SetSpeedValue(.68) # DEBUG

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
        @type text: L{string}
        """
        
        if text is None:
            text = ""

        self.GaugeWindow.SetMiddleText(text)
        

    def SetValue(self, value=None):
        """
        Sets the value of the meter (where the needle points). Sets the text value display if used and enabled.

        @param value: Value for the meter.
        @type value: L{int} or L{float}
        """
        if value is None:
            return
        else:
            self._currentValue = value
            self.GaugeWindow.SetSpeedValue(value)
            
    def GetValue(self):
        """
        Gets the meter's current value.

        @return: value
        @rtype: L{float} or L{int}
        """
        return self._currentValue
