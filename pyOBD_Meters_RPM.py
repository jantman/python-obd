#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# TuxTruck Main Frame - This is the root of everything, called from the App in main.py
# Time-stamp: "2010-06-13 00:39:04 jantman"
# $LastChangedRevision$
# $HeadURL$
#
# Copyright 2008 Jason Antman. Licensed under GNU GPLv3 or latest version (at author's discretion).
# Jason Antman - jason@jasonantman.com - http://www.jasonantman.com
# Project web site at http://www.jasonantman.com/tuxtruck/

import wx
import SpeedMeter as SM
from math import pi, sqrt

# todo - need to modify speed meter for bottom and/or top text

class pyOBD_Meters_RPM():
    """

    """

    def __init__(self, myPanel):
        """

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
                                          SM.SM_DRAW_MIDDLE_TEXT
                                          )

        # We Want To Simulate The Round Per Meter Control In A Car
        self.SpeedWindow5.SetAngleRange(-pi/6, 7*pi/6)

        intervals = range(0, 9)
        self.SpeedWindow5.SetIntervals(intervals)

        colours = [wx.BLACK]*6
        colours.append(wx.Colour(255, 255, 0))
        colours.append(wx.RED)
        self.SpeedWindow5.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        self.SpeedWindow5.SetTicks(ticks)
        self.SpeedWindow5.SetTicksColour(wx.WHITE)
        self.SpeedWindow5.SetTicksFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.SpeedWindow5.SetHandColour(wx.Colour(255, 50, 0))

        self.SpeedWindow5.SetSpeedBackground(wx.SystemSettings_GetColour(0))        

        self.SpeedWindow5.DrawExternalArc(False)

        self.SpeedWindow5.SetShadowColour(wx.Colour(50, 50, 50))

        self.SpeedWindow5.SetMiddleText("rpm")
        self.SpeedWindow5.SetBottomText("hello")
        self.SpeedWindow5.SetMiddleTextColour(wx.WHITE)
        self.SpeedWindow5.SetMiddleTextFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.SpeedWindow5.SetSpeedBackground(wx.Colour(160, 160, 160)) 
        
        self.SpeedWindow5.SetSpeedValue(5.6)

    def getSpeedWindow(self):
        return self.SpeedWindow5

