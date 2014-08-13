# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from wx.lib.mixins.listctrl import ColumnSorterMixin, ListCtrlAutoWidthMixin

###########################################################################
## Class MainFrame
###########################################################################

# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import datetime

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

   def __init__( self, parent ):
      wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 348,310 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

      self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

      bSizer1 = wx.BoxSizer( wx.VERTICAL )

      self.lblProgram = wx.StaticText( self, wx.ID_ANY, u"Running Program:", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.lblProgram.Wrap( -1 )
      bSizer1.Add( self.lblProgram, 0, wx.ALL|wx.EXPAND, 5 )

      self.lstPrograms = SortListCtrl( self )
      bSizer1.Add( self.lstPrograms, 1, wx.ALL|wx.EXPAND, 5 )

      self.btnClear = wx.Button( self, wx.ID_ANY, u"Reset Times", wx.DefaultPosition, wx.DefaultSize, 0 )
      bSizer1.Add( self.btnClear, 0, wx.ALL|wx.EXPAND, 5 )


      self.SetSizer( bSizer1 )
      self.Layout()

      self.Centre( wx.BOTH )

   def __del__( self ):
      pass



	
class SortListCtrl(wx.ListCtrl, ColumnSorterMixin, ListCtrlAutoWidthMixin):
   def __init__(self, parent):
      wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL)
      ColumnSorterMixin.__init__(self, 3)
      ListCtrlAutoWidthMixin.__init__(self)
      self.itemDataMap = {}
      self.itemIndexMap = self.itemDataMap.keys()
      self.lookupDict = {}

      self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
      self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
      self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
      self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

   def OnColClick(self, event):
      event.Skip()

   def OnItemSelected(self, event):
      self.currentItem = event.m_itemIndex

   def OnItemActivated(self, event):
      self.currentItem = event.m_itemIndex

   def getColumnText(self, index, col):
      item = self.GetItem(index, col)
      return item.GetText()

   def OnItemDeselected(self, evt):
      return None

   def GetListCtrl(self):
      return self

   def OnGetItemText(self, item, col):
      index = self.itemIndexMap[item]
      s = self.itemDataMap[index][col]
      if isinstance(s, (int, long)):
         s = datetime.timedelta(seconds=s)

      if col==0:
         s = s[:-4]
      return s

   def OnGetItemAttr(self, item):
      return None

   def SortItems(self, sorter=cmp):
      items = list(self.itemDataMap.keys())
      items.sort(sorter)
      self.itemIndexMap = items

      # redraw the list
      self.Refresh()