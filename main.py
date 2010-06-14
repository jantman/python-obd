#! /usr/bin/env python
# TuxTruck Main Application (this is what you run!)
# Time-stamp: "2010-06-14 13:54:09 jantman"
# $LastChangedRevision$
# $HeadURL$
#
# Copyright 2010 Jason Antman. Licensed under GNU GPLv3 or latest version (at author's discretion).
# Jason Antman - jason@jasonantman.com - http://www.jasonantman.com
# Project web site at http://www.jasonantman.com/tuxtruck/

""" 
Main executable for the display program. Starts the pyOBD_Main WX App.
"""

import wx # import wx for the GUI

from pyOBD_Main import pyOBD_Main # the main app frame

if __name__ == '__main__':
    app = wx.App()

    frame = pyOBD_Main(parent=None, id=-1)

    frame.Show()
    app.MainLoop()
