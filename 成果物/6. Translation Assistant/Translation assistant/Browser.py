# -*- coding: utf-8 -*-
"""
This is the final curriculum design of python
StudentNumber:16130120190
StudentName:Ren XiaoLu
"""
import wx
import SplitFrame


class App(wx.App):
    def OnInit(self):
        frame = SplitFrame.SplitFrame()
        frame.Show()
        self.SetTopWindow(frame)   # 将frame这个实例框架设定为顶层框架
        return True


if __name__ == '__main__':
    app = App(redirect=False)
    app.MainLoop()