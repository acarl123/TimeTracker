import datetime
import wx
import ctypes, win32gui, wmi, win32process, os
import shelve
import time

from MainView import MainFrame

FILE_ATTRIBUTE_HIDDEN = 0x02
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
win = win32gui
c = wmi.WMI()


class MainController:
   def __init__(self):
      self.mainWindow = MainFrame(None)
      self.timer = wx.Timer(self.mainWindow)
      self.mainWindow.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
      self.mainWindow.Bind(wx.EVT_BUTTON, self.onClear, self.mainWindow.btnClear)

      self.filename = ('fileList.trc')
      self.program_buffer = shelve.open(self.filename)
      if '__tabs__' not in self.program_buffer:
         self.program_buffer['__tabs__'] = {}
      self.timer.Start(1000)

      self.mainWindow.lstPrograms.InsertColumn(0, 'Program Name', width=150)
      self.mainWindow.lstPrograms.InsertColumn(1, 'Total Time Spent')

      self.mainWindow.lstInternet.InsertColumn(0, 'Name of Tab', width=150)
      self.mainWindow.lstInternet.InsertColumn(1, 'Total Time Spent')
      self.mainWindow.SetTitle('Time Tracker!')

   def __del__(self):
      self.timer.Stop()
      self.timer.Destroy()
      self.program_buffer.sync()
      self.program_buffer.close()
      ret = ctypes.windll.kernel32.SetFileAttributesW(ur'%s' % self.filename, FILE_ATTRIBUTE_HIDDEN)
      if ret:
         print 'attribute set to Hidden'

      else:  # return code of zero indicates failure, raise Windows error
         raise ctypes.WinError()

   def show(self):
      self.mainWindow.Show()

   def grabWindows(self):
      hwnd = win.GetForegroundWindow()
      activeWindowTitle = win.GetWindowText(hwnd)

      """Get applicatin filename given hwnd."""
      try:
         _, pid = win32process.GetWindowThreadProcessId(hwnd)
         for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = str(p.Name)
            break
      except:
         return None
      else:
         if exe in self.program_buffer:
            self.program_buffer[exe] += 1

            if exe == 'chrome.exe' or exe == 'firefox.exe' or exe == 'iexplore.exe':
               currentTab = activeWindowTitle
               if currentTab in self.program_buffer['__tabs__']:
                  self.program_buffer['__tabs__'][currentTab] += 1
               else:
                  self.program_buffer['__tabs__'][currentTab] = 1
         else:
            self.program_buffer[exe] = 1

         self.mainWindow.lblProgram.SetLabel('Spent %s in active window: %s' % (datetime.timedelta(seconds=self.program_buffer[exe]), exe[:-4]))

         objs = {}
         for key, value in self.program_buffer.items():
            if key == '__tabs__': continue
            objs[len(objs)] = (key, value)

         self.mainWindow.lstPrograms.itemDataMap = objs
         self.mainWindow.lstPrograms.itemIndexMap = objs.keys()
         self.mainWindow.lstPrograms.SetItemCount(len(objs))

         self.mainWindow.lstPrograms.SortListItems(1, ascending=0)
         self.mainWindow.lstPrograms.Refresh()

         objs = {}
         print self.program_buffer
         for key, value in self.program_buffer['__tabs__'].items():
            objs[len(objs)] = (key, value)
         self.mainWindow.lstInternet.itemDataMap = objs
         self.mainWindow.lstInternet.itemIndexMap = objs.keys()
         self.mainWindow.lstInternet.SetItemCount(len(objs))

         self.mainWindow.lstInternet.SortListItems(1, ascending=0)
         self.mainWindow.lstInternet.Refresh()

   def onTimer(self, event):
      self.grabWindows()

   def onClear(self, event):
      self.program_buffer.clear()
      self.program_buffer['__tabs__'] = {}
      self.program_buffer.sync()