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

"""
@todo: need to modify speed meter for bottom and/or top text
"""

class pyOBD_Meters_RPM():
    """
    Creates a RPM-style meter. Wrapper around SpeedMeter that sets up a meter with the right
    settings, look, etc. for a RPM gauge. Sets up the labels and handles scaling of values.
    """

    staticText = "" # text shown on the meter that doesn't change - label

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
        
        self.SpeedWindow5 = SM.SpeedMeter(myPanel,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_PARTIAL_SECTORS |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_BOTTOM_TEXT
                                          )

        # We Want To Simulate The Round Per Meter Control In A Car
        self.SpeedWindow5.SetAngleRange(-pi/6, 7*pi/6)

        intervals = range(0, 5)
        self.SpeedWindow5.SetIntervals(intervals)

        colours = [wx.BLACK]*2
        colours.append(wx.Colour(255, 255, 0))
        colours.append(wx.RED)
        print len(intervals)
        print len(colours)
        self.SpeedWindow5.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        self.SpeedWindow5.SetTicks(ticks)
        self.SpeedWindow5.SetTicksColour(wx.WHITE)
        self.SpeedWindow5.SetTicksFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.SpeedWindow5.SetHandColour(wx.Colour(255, 50, 0))

        self.SpeedWindow5.SetSpeedBackground(wx.SystemSettings_GetColour(0))        

        self.SpeedWindow5.DrawExternalArc(False)

        self.SpeedWindow5.SetShadowColour(wx.Colour(50, 50, 50))

        #self.SpeedWindow5.SetMiddleText("rpm")
        #self.SpeedWindow5.SetMiddleTextColour(wx.WHITE)
        #self.SpeedWindow5.SetMiddleTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.staticText = "RPM x1000"
        self.SpeedWindow5.SetBottomText(self.staticText)
        self.SpeedWindow5.SetBottomTextColour(wx.WHITE)
        self.SpeedWindow5.SetBottomTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.SpeedWindow5.SetSpeedBackground(wx.Colour(160, 160, 160)) 
        
        self.SpeedWindow5.SetSpeedValue(.68)

    def getSpeedWindow(self):
        """
        Returns the SpeedMeter instance that we created, so we can add it to a Panel, etc.
        @return: SpeedMeter
        @rtype: L{SpeedMeter}
        """
        return self.SpeedWindow5

    def SetText(self, text=None):
        """
        Sets The Text To Be Drawn Near The Center Of SpeedMeter (MiddleText).
        @param text: the text to be drawn
        @type text: C{string}
        """
        
        if text is None:
            text = ""

        self.SpeedWindow5._middletext = text

    def SetValue(self, value=None):
        """
        Sets the value of the meter (where the needle points). Sets the text value display if used and enabled.
        @param value: Value for the meter.
        """
        if value is None:
            return
        else:
            self.SpeedWindow5.SetSpeedValue(value)
            #self.SpeedWindow5.SetBottomText(self.staticText + "\n" + (str)((int)(value * 1000)))
