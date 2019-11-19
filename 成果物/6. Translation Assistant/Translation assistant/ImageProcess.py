# -*- coding: utf-8 -*-
"""
这个类要能够将图像展示
更重要的是要能够动态插入和删除数字
数字还要与图片一起动态移动！！
"""
import wx
import os
import LabItem


class MyImage(wx.Window):
    # 是否要移动图片的标志
    bmoved = False
    CtrlDown = False
    # 默认大小的图片，最好和上层panel匹配
    max_width = 1080
    max_height = 720
    # curPicList为目前文件夹内的jpg图片列表，在更改工作路径后由Splitter调用
    # curPicIndex为目前文件展示的第N张图片，同时也方便得到名称
    curPicIndex = 0
    curPicList = []
    # 用来保存所有标记的字典里嵌列表
    everything = {}
    # 我们要在下面的代码里创建全局Buffer
    # image 原始的图像,没有转bitmap
    # pic  StaticBitmap 负责展示图片，动态调整大小，有点像框架，但无法改变，需要用buffer改变后导入
    # buffer 缩放后的Bitmap,可以导入pic
    # Lbuffer 打过标记的Bitmap
    # 用来保存Label数量
    labelNum = 0

    def __init__(self, OutEverything, curPicList, RightPanel, parent=None,):
        wx.Window.__init__(self, parent)

        self.everything = OutEverything
        self.rightPanel = RightPanel
        self.curPicList = curPicList
        # 先创建一个默认位图
        self.pic = wx.StaticBitmap(self, 0, wx.NullBitmap, (0, 0), (400, 400))
        # 然后将默认位图改为文件里有的默认图片
        self.ChangeDir()
        # 一些其他设置
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.Center()

        # 接下来是事件
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnChangeImageSize)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.pic.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.pic.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.pic.Bind(wx.EVT_MOTION, self.OnMotion)
        self.pic.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


    # 改变当前工作路径的函数
    def ChangeDir(self):
        # 先要初始化
        self.everything.clear()
        self.curPicList.clear()
        self.curPicIndex = 0
        path = os.getcwd()

        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                pass
            elif os.path.splitext(file_path)[1] == '.jpg' or os.path.splitext(file_path)[1] == '.png':
                self.curPicList.append(file)
                # 在这里开始循环将所有的文件名添加进去，每个文件名还有一个空列表
                newList = []
                # 添加一个键值对
                self.everything[file] = newList
        self.curPicIndex = 0
        self.rightPanel.ChangeListBox(self.curPicIndex)
        self.image = wx.Image(self.curPicList[self.curPicIndex], wx.BITMAP_TYPE_ANY)
        self.ShowImage()

    def ShowImage(self):
        self.image = wx.Image(self.curPicList[self.curPicIndex], wx.BITMAP_TYPE_ANY)
        self.buffer = self.image.ConvertToBitmap()
        size = self.MyGetSize(self.buffer)
        self.buffer = self.image.Scale(size[0], size[1]).ConvertToBitmap()
        self.pic.SetSize(size)
        #绘制图形的关键操作
        self.pic.SetBitmap(self.buffer)
        self.Show()

    # 这个只有在鼠标左键抬起来的时候，同时按下Ctrl才有效,每次重新绘制一次
    def LabelAll(self):
        tempList = self.everything[self.curPicList[self.curPicIndex]]
        # 在buffer中画好带标记的图像，然后转换为pic图像
        for i in range(0, len(tempList)):
            x = tempList[i].X_percent * self.pic.GetSize()[0]
            y = tempList[i].Y_percent * self.pic.GetSize()[1]

            dc = wx.MemoryDC(self.buffer)
            dc.SetTextForeground("red")
            tmpsize = dc.GetTextExtent(str(self.labelNum))
            xtmp = x - tmpsize[0] / 2
            ytmp = y - tmpsize[1] / 2

            dc.DrawText(str(i + 1), xtmp, ytmp)
            dc.SelectObject(wx.NullBitmap)
            self.pic.SetBitmap(self.buffer)
        pass

    # 打一个label的函数，减少闪烁
    def Label(self, x, y):
        dc = wx.MemoryDC(self.buffer)
        dc.SetTextForeground("red")
        self.labelNum += 1
        tmpsize = dc.GetTextExtent(str(self.labelNum))
        xtmp = x - tmpsize[0] / 2
        ytmp = y - tmpsize[1] / 2

        tempList = self.everything[self.curPicList[self.curPicIndex]]
        tempLabel = LabItem.LabelItem(x / self.pic.GetSize()[0], y / self.pic.GetSize()[1], "")
        tempList.append(tempLabel)

        self.everything[self.curPicList[self.curPicIndex]] = tempList
        self.rightPanel.ChangeListBox(self.curPicIndex)
        dc.DrawText(str(self.labelNum), xtmp, ytmp)
        dc.SelectObject(wx.NullBitmap)
        self.pic.SetBitmap(self.buffer)

    # 删除一个label必须要重新画图了
    def deLabel(self, x, y):
        tempList = self.everything[self.curPicList[self.curPicIndex]]
        changed = False
        for i in range(0, len(tempList)):
            if abs(x - tempList[i].X_percent*self.pic.GetSize()[0]) < 15 and \
                    abs(y - tempList[i].Y_percent*self.pic.GetSize()[1]) < 15:
                del tempList[i]
                changed = True
                self.everything[self.curPicList[self.curPicIndex]] = tempList
                self.labelNum -= 1
                self.rightPanel.ChangeListBox(self.curPicIndex)
                break
        if changed:
            self.rightPanel.ChangeListBox(self.curPicIndex)
            self.ShowImage()
            self.LabelAll()
        pass

    # 得到图片大小并初期缩放的函数
    def MyGetSize(self, pic):
        width = pic.GetWidth()
        height = pic.GetHeight()
        if width > self.max_width:
            height = height * self.max_width / width
            width = self.max_width
        if height > self.max_height:
            width = width * self.max_height / height
            height = self.max_height
        size = width, height
        return size

    # 改变图像大小
    def OnChangeImageSize(self, event):
        rotation = event.GetWheelRotation()
        if rotation > 0:
            self.SizeUp()
        else:
            self.SizeDown()
        event.Skip()  # 这个貌似很重要，要同时触发app上的快捷键

    # 图像变大
    def SizeUp(self):
        self.max_width += 120
        self.max_height += 180
        self.ShowImage()
        self.LabelAll()

    # 图像变小
    def SizeDown(self):
        if self.max_width > 400 and self.max_height > 300:
            self.max_width -= 120
            self.max_height -= 180
        self.ShowImage()
        self.LabelAll()

    # 鼠标左键按下
    def OnLeftDown(self, event):
        self.SetFocus()
        self.pos = event.GetX(), event.GetY()
        self.bmoved = True

    # 鼠标左键抬起
    def OnLeftUp(self, event):
        self.bmoved = False
        # 这个if负责将label存入字典中
        if self.CtrlDown:
            x = event.GetX()
            y = event.GetY()
            self.Label(x, y)

    # 负责右键删除的操作
    def OnRightUp(self, event):
        if self.CtrlDown:
            x = event.GetX()
            y = event.GetY()
            self.deLabel(x, y)
        pass

    # 鼠标移动
    def OnMotion(self, event):
        if not self.bmoved:
            return
        pos = event.GetX(), event.GetY()
        dx = pos[0] - self.pos[0]
        dy = pos[1] - self.pos[1]
        pos = self.pic.GetPosition()
        pos = pos[0] + dx, pos[1] + dy
        self.pic.SetPosition(pos)

    # 按键按下，只检测1、2和Ctrl
    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_CONTROL:
            self.CtrlDown = True
        if keycode == 49:
            self.beforePic()
        if keycode == 50:
            self.nextPic()

    # 按键抬起，只检测Ctrl
    def OnKeyUp(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_CONTROL:
            self.CtrlDown = False
        pass

    # 下一页
    def nextPic(self):
        if self.curPicIndex < self.curPicList.__len__() - 1:
            self.curPicIndex += 1
            self.labelNum = 0
            self.ShowImage()
            self.rightPanel.ChangeListBox(self.curPicIndex)
            if len(self.rightPanel.tempList) != 0:
                self.rightPanel.m_listBox.SetSelection(0)
                self.rightPanel.DeafultPage()
                self.LabelAll()
            else:
                self.rightPanel.textCtrl.Clear()
        else:
            pass

    # 上一页
    def beforePic(self):
        if self.curPicIndex > 0:
            self.curPicIndex -= 1
            self.labelNum = 0
            self.ShowImage()
            self.rightPanel.ChangeListBox(self.curPicIndex)
            if len(self.rightPanel.tempList) != 0:
                self.rightPanel.m_listBox.SetSelection(0)
                self.rightPanel.DeafultPage()
                self.LabelAll()
            else:
                self.rightPanel.textCtrl.Clear()
        else:
            pass