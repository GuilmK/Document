# -*- coding: utf-8 -*-

import wx
import wx.xrc
import MusicPanel
import os
import OnLineTranslation


class MyPanel(wx.Panel):
    everything = {}
    curPicList = []
    tempList = []

    def __init__(self, OutEverything, curPicList, parent):
        self.everything = OutEverything
        self.curPicList = curPicList
        # 音乐控制器实例
        self.musicPlayer = MusicPanel.MusicControl()
        #在线翻译实例
        self.onLineTrans = OnLineTranslation.Baidu()

        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(330, 720),
                          style=wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.SetMaxSize(wx.Size(-1, 1080))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"预览"), wx.VERTICAL)

        m_listBoxChoices = []
        self.m_listBox = wx.ListBox(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1),
                                    m_listBoxChoices, 0)
        self.m_listBox.SetMinSize(wx.Size(300, 320))

        sbSizer1.Add(self.m_listBox, 1, wx.ALIGN_RIGHT | wx.ALIGN_TOP | wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        bSizer1.Add(sbSizer1, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"翻译"), wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.textCtrl = wx.TextCtrl(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                    wx.Size(-1, -1), wx.TE_CHARWRAP|wx.TE_MULTILINE)
        self.textCtrl.SetMinSize(wx.Size(300, 135))

        bSizer2.Add(self.textCtrl, 1, wx.ALIGN_RIGHT | wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        sbSizer2.Add(bSizer2, 1, wx.ALIGN_RIGHT | wx.ALIGN_TOP | wx.EXPAND, 5)

        bSizer1.Add(sbSizer2, 2, wx.ALIGN_RIGHT | wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"在线翻译"), wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl1 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                     wx.Size(-1, -1), style=wx.TE_PROCESS_ENTER)
        self.textCtrl1.SetMinSize(wx.Size(125, 25))

        bSizer3.Add(self.textCtrl1, 1, wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        self.staticText = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"-->", wx.DefaultPosition, wx.DefaultSize,
                                        0)
        self.staticText.Wrap(-1)
        bSizer3.Add(self.staticText, 0, wx.ALIGN_CENTER, 10)

        self.textCtrl2 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TE_READONLY)
        self.textCtrl2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
        self.textCtrl2.SetMinSize(wx.Size(125, 25))

        bSizer3.Add(self.textCtrl2, 1, wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        sbSizer3.Add(bSizer3, 1, wx.ALIGN_CENTER | wx.ALIGN_TOP | wx.EXPAND, 5)

        bSizer1.Add(sbSizer3, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.LEFT, 5)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"音乐"), wx.HORIZONTAL)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_textCtrl4 = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.m_textCtrl4.Enable(False)

        bSizer5.Add(self.m_textCtrl4, 1, wx.ALIGN_CENTER, 5)

        self.m_slider1 = wx.Slider(sbSizer4.GetStaticBox(), wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.DefaultSize,
                                   wx.SL_HORIZONTAL)
        bSizer5.Add(self.m_slider1, 0, wx.ALL, 5)

        bSizer4.Add(bSizer5, 1, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bpButton1 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.Bitmap(
            u"pic\\1.png", wx.BITMAP_TYPE_ANY),
                                           wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer6.Add(self.m_bpButton1, 1, wx.ALL | wx.EXPAND, 5)

        self.m_bpButton2 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.Bitmap(
            u"pic\\2.png", wx.BITMAP_TYPE_ANY),
                                           wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer6.Add(self.m_bpButton2, 1, wx.ALL | wx.EXPAND, 5)

        self.m_bpButton3 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.Bitmap(
            u"pic\\3.png", wx.BITMAP_TYPE_ANY),
                                           wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer6.Add(self.m_bpButton3, 1, wx.ALL | wx.EXPAND, 5)

        self.m_bpButton4 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.Bitmap(
            u"pic\\4.png", wx.BITMAP_TYPE_ANY),
                                           wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer6.Add(self.m_bpButton4, 1, wx.ALL | wx.EXPAND, 5)

        self.m_bpButton5 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.Bitmap(
            u"pic\\5.png", wx.BITMAP_TYPE_ANY),
                                           wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer6.Add(self.m_bpButton5, 1, wx.ALL | wx.EXPAND, 5)

        bSizer4.Add(bSizer6, 1, wx.EXPAND, 5)

        sbSizer4.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer4, 1, wx.EXPAND | wx.TOP | wx.LEFT, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.Bind(wx.EVT_TEXT_ENTER, self.OnOnlineTrans, self.textCtrl1)

        self.m_listBox.Bind(wx.EVT_LISTBOX, self.OnListBoxSelected)

        # 这个不知道为什么阻止了文字输入
        self.textCtrl.Bind(wx.EVT_KEY_DOWN, self.OnTextKeyDown)

        self.textCtrl1.Bind(wx.EVT_TEXT, self.OnChangeTransText)
        # self.textCtrl1.Bind(wx.EVT_TEXT_ENTER, self.OnOnlineTrans) 　　这个绑定方法并不能触发回车事件
        self.m_slider1.Bind(wx.EVT_SCROLL, self.OnChangeVolume)

        self.m_bpButton1.Bind(wx.EVT_BUTTON, self.OnPreviousMusic)
        self.m_bpButton2.Bind(wx.EVT_BUTTON, self.OnStopMusic)
        self.m_bpButton3.Bind(wx.EVT_BUTTON, self.OnPlayMusic)
        self.m_bpButton4.Bind(wx.EVT_BUTTON, self.OnPauseMusic)
        self.m_bpButton5.Bind(wx.EVT_BUTTON, self.OnNextMusic)

    # 图片变化时修改ListBox
    def ChangeListBox(self, curPicIndex):
        self.tempList = self.everything[self.curPicList[curPicIndex]]
        self.m_listBox.Clear()
        for i in range(0, len(self.tempList)):
            tmp = '%2d' % (i+1)
            self.m_listBox.Append(tmp + ": " + self.tempList[i].text)
        pass

    # 当被选中某一项时的状态
    def OnListBoxSelected(self, event):
        i = self.m_listBox.GetSelection()
        self.textCtrl.Clear()
        self.textCtrl.write(self.tempList[i].text)
        pass

    def DeafultPage(self):
        i = 0
        tmp = '%2d' % 1
        self.textCtrl.Clear()
        self.textCtrl.write(self.tempList[i].text)

    # 当开始键入翻译内容，想换下一个
    def OnTextKeyDown(self, event):
        if event.AltDown() and event.CmdDown():
            i = self.m_listBox.GetSelection()
            if i == len(self.tempList) - 1:
                i = 0
                tmp = '%2d' % len(self.tempList)
                self.m_listBox.SetSelection(i)
                self.tempList[len(self.tempList) - 1].text = self.textCtrl.GetValue()
                self.m_listBox.SetString(len(self.tempList) - 1,tmp + ": " + self.tempList[len(self.tempList) - 1].text)
                self.textCtrl.Clear()
                self.textCtrl.write(self.tempList[i].text)
            else:
                tmp = '%2d' % (i + 1)
                self.m_listBox.SetSelection(i + 1)
                self.tempList[i].text = self.textCtrl.GetValue()
                self.textCtrl.Clear()
                self.textCtrl.write(self.tempList[i + 1].text)
                self.m_listBox.SetString(i, tmp + ": " + self.tempList[i].text)
        # 没有这一句的话就没有办法输入文字了
        event.Skip()
        pass

    # 当改变了在线翻译文本里的内容时
    def OnChangeTransText(self, event):
        self.textCtrl2.Clear()
        pass

    # 在线翻译
    def OnOnlineTrans(self, event):
        strings = self.onLineTrans.Translation(self.textCtrl1.GetValue())
        self.textCtrl2.write(strings)
        pass

    # 改变音量
    def OnChangeVolume(self, event):
        self.musicPlayer.ChangeVolume(self.m_slider1.GetValue()/100)
        pass

    # 上一首歌
    def OnPreviousMusic(self, event):
        tmptext = self.musicPlayer.PreviousMusic()
        self.m_textCtrl4.Clear()
        self.m_textCtrl4.write(os.path.split(tmptext)[1])
        pass

    # 下一首歌
    def OnNextMusic(self, event):
        tmptext = self.musicPlayer.NextMusic()
        self.m_textCtrl4.Clear()
        self.m_textCtrl4.write(os.path.split(tmptext)[1])
        pass

    # 停止歌曲
    def OnStopMusic(self, event):
        self.musicPlayer.StopMusic()
        self.m_textCtrl4.Clear()
        self.m_textCtrl4.write("Stop")
        pass

    # 播放歌曲
    def OnPlayMusic(self, event):
        tmptext = self.musicPlayer.PlayMusic()
        self.m_textCtrl4.Clear()
        self.m_textCtrl4.write(os.path.split(tmptext)[1])
        pass

    # 暂停歌曲
    def OnPauseMusic(self, event):
        self.musicPlayer.PauseMusic()
        pass

