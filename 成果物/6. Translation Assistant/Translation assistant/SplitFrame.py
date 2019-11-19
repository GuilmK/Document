# -*- coding: utf-8 -*-
import wx
import ImageProcess
import FileHandler
import RightPanel
import os


class SplitFrame(wx.Frame):
    # 从子块中提取出来的
    # curPicList为目前文件夹内的jpg图片列表，在更改工作路径后由Splitter调用
    # curPicIndex为目前文件展示的第N张图片，同时也方便得到名称
    everything = {}
    curPicList = []

    def __init__(self, title="Translation Assistant"):
        wx.Frame.__init__(self, None, -1, title=title, size=(1080, 730))


        # 初始化
        self.InitFileHander()
        self.InitSplit()
        self.InitMenu()


        # 位置操作和显示操作
        self.Centre()
        self.Show()

        pass

    def InitFileHander(self):
        self.fileHander = FileHandler.FileHandler(self.everything)  # 初始化一个FileHander的实例
        pass

    def InitSplit(self):
        # 分割界面
        self.splitter =wx.SplitterWindow(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.SP_3DBORDER|wx.SP_LIVE_UPDATE)
        self.rightPanel = RightPanel.MyPanel(self.everything, self.curPicList, self.splitter)
        self.imagePanel = ImageProcess.MyImage(self.everything, self.curPicList, self.rightPanel, self.splitter)
        self.rightPanel.everything = self.imagePanel.everything  # 绑定字典
        self.splitter.SplitVertically(self.imagePanel, self.rightPanel, 730)
        # 设置最小窗格大小，左右布局指左边窗口大小
        self.splitter.SetMinimumPaneSize(330)
        pass

    def InitMenu(self):
        # Menu长条
        self.m_menubar = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"新建翻译", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem1)

        self.m_menuItem2 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"打开翻译", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem2)

        self.m_menuItem3 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"保存翻译", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem3)

        self.m_menuItem4 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"另存为", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem4)

        self.m_menubar.Append(self.m_menu1, u"文件(F)")

        self.m_menu2 = wx.Menu()
        self.m_menuItem5 = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"音乐路径", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuItem5)

        self.m_menuItem7 = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"百度翻译账号", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuItem7)

        self.m_menubar.Append(self.m_menu2, u"管理(I)")

        self.m_menu3 = wx.Menu()
        self.m_menuItem6 = wx.MenuItem(self.m_menu3, wx.ID_ANY, u"作者", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_menuItem6)

        self.m_menubar.Append(self.m_menu3, u"关于(A)")

        self.SetMenuBar(self.m_menubar)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.OnCreateTranslation, id=self.m_menuItem1.GetId())
        self.Bind(wx.EVT_MENU, self.OnOpenTranslation, id=self.m_menuItem2.GetId())
        self.Bind(wx.EVT_MENU, self.OnSaveTranslation, id=self.m_menuItem3.GetId())
        self.Bind(wx.EVT_MENU, self.OnSaveAsTranslation, id=self.m_menuItem4.GetId())
        self.Bind(wx.EVT_MENU, self.OnChangeMusicFile, id=self.m_menuItem5.GetId())
        self.Bind(wx.EVT_MENU, self.OnMe, id=self.m_menuItem6.GetId())
        self.Bind(wx.EVT_MENU, self.OnTranslationCode, id=self.m_menuItem7.GetId())
        pass

    def OnCreateTranslation(self, event):
        self.fileHander.CreateTranslation(self.splitter.GetWindow1())
        pass

    def OnOpenTranslation(self, event):
        self.fileHander.OpenTranslation(self.splitter.GetWindow1())
        self.rightPanel.ChangeListBox(0)
        pass

    def OnSaveTranslation(self, event):
        self.fileHander.SaveTranslation()
        pass

    def OnSaveAsTranslation(self, event):
        self.fileHander.SaveAsTranslation()
        pass

    def OnChangeMusicFile(self, event):
        self.rightPanel.musicPlayer.ChangeMusicFilePath()
        pass

    def OnMe(self,event):
        wx.MessageBox("代码写的一塌糊涂的罪梦", "作者", wx.ICON_INFORMATION)
        pass

    def OnTranslationCode(self,event):
        dlg = wx.TextEntryDialog(None, u"请输入账号密码，用空格分隔:", u"百度翻译账号密码", u"账号 密码")
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue()
            tmp = message.split()
            self.rightPanel.onLineTrans.Init(tmp[0], tmp[1])
        dlg.Destroy()
        pass