#! /usr/bin/env python
# TuxTruck Main Application (this is what you run!)
# Time-stamp: "2010-06-12 22:43:02 jantman"
# $LastChangedRevision$
# $HeadURL$
#
# Copyright 2010 Jason Antman. Licensed under GNU GPLv3 or latest version (at author's discretion).
# Jason Antman - jason@jasonantman.com - http://www.jasonantman.com
# Project web site at http://www.jasonantman.com/tuxtruck/

import wx # import wx for the GUI

from pyOBD_Main import * # the main app frame

if __name__ == '__main__':
    """ 
    main method for the whole program. This gets called when we start this application,
    and it instantiates all of the necessary classes and starts the GUI and backend code.
    """
    app = wx.App()

    frame = pyOBD_Main(parent=None, id=-1)

    frame.Show()
    app.MainLoop()
