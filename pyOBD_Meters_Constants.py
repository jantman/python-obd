#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# $LastChangedRevision: 7 $
# $HeadURL: http://svn.jasonantman.com/pyOBD/pyOBD_Meters_RPM.py $

"""
Module for the constants used in the different meters
"""

import wx

class pyOBD_Meters_Constants():
    """
    Class to hold the constants used in all of the different meters.
    """

    #M_LARGE_BG_COLOR = wx.Colour(206, 220, 233)
    M_LARGE_BG_COLOR = wx.Colour(222, 222, 222)
    M_LARGE_TICK_COLOR = wx.Colour(67, 67, 67)
    M_LARGE_TEXT_COLOR = M_LARGE_TICK_COLOR
    #M_LARGE_ARC_COLOR = M_LARGE_TICK_COLOR
    M_LARGE_ARC_COLOR = wx.Colour(255, 255, 255)
    M_LARGE_LED_COLOR = wx.Colour(21, 131, 3)
