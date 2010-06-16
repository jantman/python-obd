#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# $LastChangedRevision: 8 $
# $HeadURL: http://svn.jasonantman.com/pyOBD/pyOBD_Meters_RPM.py $

"""
Pure Python rewrite of the wxCode.gadgets.ledctrl class
"""

import wx

class ledctrl(BufferedWindow):
    """
    Creates a LEDctrl object
    """

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

        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                bufferedstyle=bufferedstyle)

        """
        wxLEDNumberCtrl::wxLEDNumberCtrl(wxWindow *parent, wxWindowID id,
        const wxPoint& pos, const wxSize& size,
        long style)
        :   m_Alignment(wxLED_ALIGN_LEFT),
        m_LineMargin(-1),
        m_DigitMargin(-1),
        m_LineLength(-1),
        m_LineWidth(-1),
        m_DrawFaded(false),
        m_LeftStartPos(-1)
        {
        Create(parent, id, pos, size, style);
        }
        """

        """
bool wxLEDNumberCtrl::Create(wxWindow *parent, wxWindowID id,
                                 const wxPoint& pos, const wxSize& size,
                                 long style)
{
    bool RetVal = wxControl::Create(parent, id, pos, size, style);

    if ((style & wxLED_DRAW_FADED) != 0)
        SetDrawFaded(true);
    if ((style & wxLED_ALIGN_MASK) != 0)
        SetAlignment((wxLEDValueAlign)(style & wxLED_ALIGN_MASK));

    SetBackgroundColour(*wxBLACK);
    SetForegroundColour(*wxGREEN);

    return RetVal;
}

        """
        print "done init" # DEBUG

    def SetAlignment(self, Alignment, Redraw):
        """
        Sets LED digit alignment.
        
        @param Alignment
        @type Alignment: wxLEDValueAlign
        @type Redraw: C{boolean}
        """
        
        if Alignment != m_Alignment:
            m_Alignment = Alignment
            RecalcInternals(GetClientSize())
            if Redraw:
                Refresh(false)
                
    def SetDrawFaded(self, DrawFaded, Redraw):
        """
        @type DrawFaded: C{boolean}
        @type Redraw: C{boolean}
        """

        if DrawFaded != m_DrawFaded:
            m_DrawFaded = DrawFaded
            if Redraw:
                Refresh(False)
# TODO - DEBUG - LEFT OFF HERE
# open next to the SpeedMeter class, take some clues from there.

void wxLEDNumberCtrl::SetValue(wxString const &Value, bool Redraw)
{
    if (Value != m_Value)
    {
#ifdef __WXDEBUG__
        if (!Value.empty())
        {
            for(size_t i=0; i<Value.Length(); i++) {
                wxChar ch = Value[i];
                wxASSERT_MSG((ch>='0' && ch<='9') || ch=='-' || ch==' ' || ch=='.',
                             wxT("wxLEDNumberCtrl can only display numeric string values."));
            }
        }
#endif

        m_Value = Value;
        RecalcInternals(GetClientSize());

        if (Redraw)
            Refresh(false);
    }
}


BEGIN_EVENT_TABLE(wxLEDNumberCtrl, wxControl)
    EVT_ERASE_BACKGROUND(wxLEDNumberCtrl::OnEraseBackground)
    EVT_PAINT(wxLEDNumberCtrl::OnPaint)
    EVT_SIZE(wxLEDNumberCtrl::OnSize)
END_EVENT_TABLE()


void wxLEDNumberCtrl::OnEraseBackground(wxEraseEvent &WXUNUSED(event))
{
}


void wxLEDNumberCtrl::OnPaint(wxPaintEvent &WXUNUSED(event))
{
    wxPaintDC Dc(this);

    int Width, Height;
    GetClientSize(&Width, &Height);

    wxBitmap *pMemoryBitmap = new wxBitmap(Width, Height);
    wxMemoryDC MemDc;

    MemDc.SelectObject(*pMemoryBitmap);

    // Draw background.
    MemDc.SetBrush(wxBrush(GetBackgroundColour(), wxSOLID));
    MemDc.DrawRectangle(wxRect(0, 0, Width, Height));
    MemDc.SetBrush(wxNullBrush);

    // Iterate each digit in the value, and draw.
    const int DigitCount = m_Value.Len();
    for (int offset=0, i = 0; offset < DigitCount; ++offset, ++i)
    {
        wxChar c = m_Value.GetChar(offset);

        // Draw faded lines if wanted.
        if (m_DrawFaded && (c != _T('.')))
            DrawDigit(MemDc, DIGITALL, i);

        // Draw the digits.
        switch (c)
        {
            case _T('0') :
                DrawDigit(MemDc, DIGIT0, i);
                break;
            case _T('1') :
                DrawDigit(MemDc, DIGIT1, i);
                break;
            case _T('2') :
                DrawDigit(MemDc, DIGIT2, i);
                break;
            case _T('3') :
                DrawDigit(MemDc, DIGIT3, i);
                break;
            case _T('4') :
                DrawDigit(MemDc, DIGIT4, i);
                break;
            case _T('5') :
                DrawDigit(MemDc, DIGIT5, i);
                break;
            case _T('6') :
                DrawDigit(MemDc, DIGIT6, i);
                break;
            case _T('7') :
                DrawDigit(MemDc, DIGIT7, i);
                break;
            case _T('8') :
                DrawDigit(MemDc, DIGIT8, i);
                break;
            case _T('9') :
                DrawDigit(MemDc, DIGIT9, i);
                break;
            case _T('-') :
                DrawDigit(MemDc, DASH, i);
                break;
            case _T('.') :
                // Display the decimal in the previous segment
                i--;
                DrawDigit(MemDc, DECIMALSIGN, i);
                break;
            case _T(' ') :
                // just skip it
                break;
            default :
                wxFAIL_MSG(wxT("Unknown digit value"));
                break;
        }
    }

    // Blit the memory dc to screen.
    Dc.Blit(0, 0, Width, Height, &MemDc, 0, 0, wxCOPY);
    delete pMemoryBitmap;
}


void wxLEDNumberCtrl::DrawDigit(wxDC &Dc, int Digit, int Column)
{
    wxColour LineColor(GetForegroundColour());

    if (Digit == DIGITALL)
    {
        const unsigned char R = (unsigned char)(LineColor.Red() / 16);
        const unsigned char G = (unsigned char)(LineColor.Green() / 16);
        const unsigned char B = (unsigned char)(LineColor.Blue() / 16);

        LineColor.Set(R, G, B);
    }

    int XPos = m_LeftStartPos + Column * (m_LineLength + m_DigitMargin);

    // Create a pen and draw the lines.
    wxPen Pen(LineColor, m_LineWidth, wxSOLID);
    Dc.SetPen(Pen);

    if ((Digit & LINE1))
    {
        Dc.DrawLine(XPos + m_LineMargin*2, m_LineMargin,
            XPos + m_LineLength + m_LineMargin*2, m_LineMargin);
    }

    if (Digit & LINE2)
    {
        Dc.DrawLine(XPos + m_LineLength + m_LineMargin*3, m_LineMargin*2,
            XPos + m_LineLength + m_LineMargin*3, m_LineLength + (m_LineMargin*2));
    }

    if (Digit & LINE3)
    {
        Dc.DrawLine(XPos + m_LineLength + m_LineMargin*3, m_LineLength + (m_LineMargin*4),
            XPos + m_LineLength + m_LineMargin*3, m_LineLength*2 + (m_LineMargin*4));
    }

    if (Digit & LINE4)
    {
        Dc.DrawLine(XPos + m_LineMargin*2, m_LineLength*2 + (m_LineMargin*5),
            XPos + m_LineLength + m_LineMargin*2, m_LineLength*2 + (m_LineMargin*5));
    }

    if (Digit & LINE5)
    {
        Dc.DrawLine(XPos + m_LineMargin, m_LineLength + (m_LineMargin*4),
            XPos + m_LineMargin, m_LineLength*2 + (m_LineMargin*4));
    }

    if (Digit & LINE6)
    {
        Dc.DrawLine(XPos + m_LineMargin, m_LineMargin*2,
            XPos + m_LineMargin, m_LineLength + (m_LineMargin*2));
    }

    if (Digit & LINE7)
    {
        Dc.DrawLine(XPos + m_LineMargin*2, m_LineLength + (m_LineMargin*3),
            XPos + m_LineMargin*2 + m_LineLength, m_LineLength + (m_LineMargin*3));
    }

    if (Digit & DECIMALSIGN)
    {
        Dc.DrawLine(XPos + m_LineLength + m_LineMargin*4, m_LineLength*2 + (m_LineMargin*5),
            XPos + m_LineLength + m_LineMargin*4, m_LineLength*2 + (m_LineMargin*5));
    }

    Dc.SetPen(wxNullPen);
}


void wxLEDNumberCtrl::RecalcInternals(const wxSize &CurrentSize)
{
    // Dimensions of LED segments
    //
    // Size of character is based on the HEIGH of the widget, NOT the width.
    // Segment height is calculated as follows:
    // Each segment is m_LineLength pixels long.
    // There is m_LineMargin pixels at the top and bottom of each line segment
    // There is m_LineMargin pixels at the top and bottom of each digit
    //
    //  Therefore, the heigth of each character is:
    //  m_LineMargin                            : Top digit boarder
    //  m_LineMargin+m_LineLength+m_LineMargin  : Top half of segment
    //  m_LineMargin+m_LineLength+m_LineMargin  : Bottom half of segment
    //  m_LineMargin                            : Bottom digit boarder
    //  ----------------------
    //  m_LineMargin*6 + m_LineLength*2 == Total height of digit.
    //  Therefore, (m_LineMargin*6 + m_LineLength*2) must equal Height
    //
    //  Spacing between characters can then be calculated as follows:
    //  m_LineMargin                            : before the digit,
    //  m_LineMargin+m_LineLength+m_LineMargin  : for the digit width
    //  m_LineMargin                            : after the digit
    //  = m_LineMargin*4 + m_LineLength
    const int Height = CurrentSize.GetHeight();

    if ((Height * 0.075) < 1)
        m_LineMargin = 1;
    else
        m_LineMargin = (int)(Height * 0.075);

    if ((Height * 0.275) < 1)
        m_LineLength = 1;
    else
        m_LineLength = (int)(Height * 0.275);

    m_LineWidth = m_LineMargin;

    m_DigitMargin = m_LineMargin * 4;

    // Count the number of characters in the string; '.' characters are not
    // included because they do not take up space in the display
    int count = 0;
    for (unsigned int i = 0; i < m_Value.Len(); i++)
        if (m_Value.GetChar(i) != '.')
            count++;
    const int ValueWidth = (m_LineLength + m_DigitMargin) * count;
    const int ClientWidth = CurrentSize.GetWidth();

    switch (m_Alignment)
    {
        case wxLED_ALIGN_LEFT :
            m_LeftStartPos = m_LineMargin;
            break;
        case wxLED_ALIGN_RIGHT :
            m_LeftStartPos = ClientWidth - ValueWidth - m_LineMargin;
            break;
        case wxLED_ALIGN_CENTER :
            m_LeftStartPos = (ClientWidth - ValueWidth) / 2;
            break;
        default :
            wxFAIL_MSG(wxT("Unknown alignent value for wxLEDNumberCtrl."));
            break;
    }
}


void wxLEDNumberCtrl::OnSize(wxSizeEvent &Event)
{
    RecalcInternals(Event.GetSize());

    Event.Skip();
}
